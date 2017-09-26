import logging
from abc import ABC, abstractmethod
from typing import List

from sn_agent.ontology import Ontology, Service
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.service_adapter.manager import ServiceManager

logger = logging.getLogger(__name__)


class ServiceAdapterABC(ABC):
    """
    This is the service adapter base, all other service adapters are based on it.
    """

    type_name = "Base"

    def __init__(self, app, service: Service, required_service_node_ids) -> None:
        self.app = app
        self.service = service
        self.required_service_node_ids = required_service_node_ids
        self.required_service_adapters = []
        self.requirements_met = False
        self.available = False

    def post_load_initialize(self, service_manager : ServiceManager):
        """
        This will hunt out all the agents required to fulfill the required ontology ids

        We should periodically call this if it is false - an agent might come alive that can support this
        :return:
        """
        if not self.required_service_node_ids is None:
            for node_id in self.required_service_node_ids:
                service_adapter = service_manager.get_service_adapter_for_id(node_id)
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
        return self.requirements_met and self.available and all_required_agents_can_perform()

    def all_required_agents_can_perform(self):

        if self.required_ontology_node_ids is None:
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

class ModuleServiceAdapterABC(ServiceAdapterABC):
    """
    This is the service adapter base, all other service adapters are based on it.
    """

    type_name = "ModuleServiceAdapter"

    def __init__(self, app, service: Service, required_services: List[Service], name: str) -> None:
        super().__init__(app, service, required_services)
        self.name = name
