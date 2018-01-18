import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

import jsonrpcclient
import yaml

from sn_agent import SettingsBase, Required
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology import Service
from sn_agent.utils import import_string

logger = logging.getLogger(__name__)


class ServiceAdapterSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self._ENV_PREFIX = 'SN_SERVICE_ADAPTER_'

        # This is a yaml config file
        self.CONFIG_FILE = Required(Path)

        super().__init__(**custom_settings)


class ServiceManager:
    def __init__(self, app, service_adapters):
        self.app = app
        self.services_by_id = {}
        self.service_adapters = service_adapters
        for service_adapter in service_adapters:
            service = service_adapter.service
            self.services_by_id[service.node_id] = service_adapter

    def post_load_initialize(self):
        logger.debug("Starting post load initialization phase")
        for service_adapter in self.service_adapters:
            logger.debug("Calling post load initialization for %s", service_adapter)
            service_adapter.post_load_initialize(self)
            service_adapter.start()

    def start(self, service_node_id):
        # Find the service adapters for a given service descriptor and enable them
        service_adapter = self.get_service_adapter_for_id(service_node_id)
        service_adapter.start()

    def stop(self, service_node_id):
        # Find the service adapters for a given service descriptor and disable them
        service_adapter = self.get_service_adapter_for_id(service_node_id)
        service_adapter.stop()

    def get_service_adapter_for_id(self, service_id):
        service_adapter = self.services_by_id.get(service_id)
        return service_adapter


class ServiceAdapterABC(ABC):
    """
    This is the service adapter base, all other service adapters are based on it.
    """

    type_name = "Base"

    def __init__(self, app, service: Service, required_services: List[Service] = None) -> None:
        self.app = app
        self.service = service
        self.required_services = required_services
        self.required_service_adapters = []
        self.requirements_met = False
        self.available = False

    def __str__(self):
        return self.service.name

    def example_job_json(self):
        return json.dumps(self.example_job())

    def post_load_initialize(self, service_manager: ServiceManager):
        """
        This will hunt out all the agents required to fulfill the required ontology ids

        We should periodically call this if it is false - an agent might come alive that can support this
        :return:
        """
        if not self.required_services is None:
            for required_service in self.required_services:
                service_adapter = service_manager.get_service_adapter_for_id(required_service.node_id)
                self.required_service_adapters.append(service_adapter)
        self.requirements_met = self.has_all_requirements()

        logger.info('Service Adapter: %s initialized. Requirements met: %s', self.type_name, self.requirements_met)
        # print('Service Adapter: %s initialized. Requirements met: %s' % (self.type_name, self.requirements_met))

    def has_all_requirements(self):
        """
        Check to see if our all required services are available
        :return:
        """
        for required_service_adapter in self.required_service_adapters:
            if not required_service_adapter.has_all_requirements():
                return False
        return True

    def start(self):
        """
        If init sets up all the connections, start is here to ensure that the worker is actually alive and can process
        :return:
        """
        self.available = True

    def stop(self):
        """
        This will take the worker offline but does not need to be re-initialized
        :return:
        """
        self.available = False

    def can_perform(self) -> bool:
        """
        This is a boolean flag indicating if this worker can do whatever work it says it can.

        An answer of no can be because it is offline, or perhaps it is too busy.
        :return:
        """
        return self.requirements_met and self.available and self.all_required_agents_can_perform()

    def all_required_agents_can_perform(self):

        if self.required_services is None:
            return True

        for required_service_adapter in self.required_service_adapters:
            if not required_service_adapter.can_perform():
                return False
        return True

    @abstractmethod
    def perform(self, job: JobDescriptor):
        """
        This is where the work gets done, the worker will block here until the work itself is done
        :param args:
        :param kwargs:
        :return:
        """
        pass


class ExternalServiceAdapter(ServiceAdapterABC):
    def __init__(self, app, service: Service, agent_ids: list):
        super().__init__(app, service)
        self.app = app
        self.agent_ids = agent_ids
        self.urls = {}

    def post_load_initialize(self, service_manager: ServiceManager):

        network = self.app['network']

        for agent_id in self.agent_ids:
            url = network.get_url_for_agent(agent_id)

            if url is None:
                raise RuntimeError('Invalid agent specified: %s' % agent_id)

            self.urls[agent_id] = url

        super().post_load_initialize(service_manager)

    def has_all_requirements(self):
        return True

    def can_perform(self) -> bool:

        for agent_id in self.agent_ids:

            url = self.urls[agent_id]

            try:
                result = jsonrpcclient.request(
                    url,
                    'can_perform',
                    {
                        "service_node_id": self.service.node_id
                    }
                )

                return result

            except:
                logger.error('error requesting %s for agent %s', url, agent_id)

    def perform(self, job: JobDescriptor):

        for agent_id in self.agent_ids:

            url = self.urls[agent_id]

            try:
                result = jsonrpcclient.request(
                    url,
                    'perform',
                    {
                        "service_node_id": self.service.node_id,
                        "job_params": job.job_parameters
                    }
                )

                return result

            except:
                logger.error('error requesting %s for agent %s', url, agent_id)


def setup_service_manager(app, service_adapters: List[ServiceAdapterABC] = None) -> ServiceManager:
    settings = ServiceAdapterSettings()
    config_file = settings.CONFIG_FILE
    ontology = app['ontology']

    logger.debug("reading configuration file {0}".format(config_file))

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    if service_adapters is None:
        service_adapters = []

    # Load service adapters from the config file.
    for section, data in cfg.items():
        if section == 'services':
            for service_object in data:

                service_id = service_object.get('service')
                if service_id is None:
                    raise RuntimeError('You must supply a service id for each service adapter')

                service = ontology.get_service(service_id)

                name = service_object['module']
                module_klass = import_string(name)

                required_services_object = service_object.get('required_services')

                required_services = []

                # Get the required / dependent service adapters corresponding to require service ids.
                if required_services_object is not None:
                    for required_service_object in required_services_object:

                        required_service_id = required_service_object.get('id')
                        if required_service_id is None:
                            raise RuntimeError('You must supply a service id for each required service')

                        required_service = ontology.get_service(required_service_id)
                        required_services.append(required_service)

                        required_agents = required_service_object.get('agents')

                        if required_agents is not None:
                            external_service_adapter = ExternalServiceAdapter(app, required_service, required_agents)
                            service_adapters.append(external_service_adapter)

                service.required_services = required_services

                service_adapter = module_klass(app, service, required_services)
                service_adapters.append(service_adapter)
        else:
            raise RuntimeError('Unknown service adapter type specified: %s' % section)

    service_manager = ServiceManager(app, service_adapters)
    service_manager.post_load_initialize()
    app['service_manager'] = service_manager
    return service_manager
