import yaml

from sn_agent.service_adapter.jsonrpc import JsonRpcServiceAdapter
from sn_agent.service_adapter.opencog import OpenCogServiceAdapter
from sn_agent.service_adapter.settings import ServiceAdapterSettings
from sn_agent.utils import import_string


class ServiceManager:
    def __init__(self, service_adapters):
        self.services_by_id = {}
        self.service_adapters = service_adapters
        for service_adapter in service_adapters:
            service_adapter.init()
            service = service_adapter.service
            self.services_by_id[service.node_id] = service_adapter

    def init_all(self):
        for service_adapter in self.service_adapters:
            service_adapter.init()

    def start(self, service_node_id):
        # Find the service adapters for a given service descriptor and disable them
        service_adapter = self.get_service_adapter_for_id(service_node_id)
        service_adapter.start()

    def stop(self, service_node_id):
        # Find the service adapters for a given service descriptor and disable them
        service_adapter = self.get_service_adapter_for_id(service_node_id)
        service_adapter.stop()

    def get_service_adapter_for_id(self, service_node_id):
        service_adapter = self.services_by_id.get(service_node_id)
        return service_adapter

def setup_service_manager(app):
    settings = ServiceAdapterSettings()
    config_file = settings.CONFIG_FILE
    ontology = app['ontology']

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    service_adapters = []

    for section, data in cfg.items():
        if section == 'opencogs':
            for opencog_data in data:
                ontology_node_id = opencog_data.get('ontology_node_id')
                if ontology_node_id is None:
                    raise RuntimeError('You must supply a ontology_node_id for each service adapter')

                required_ontology_node_ids = opencog_data.get('required_ontology_node_ids')

                host = opencog_data['host']
                port = opencog_data['port']
                service = ontology.get_service(ontology_node_id)
                service_adapter = OpenCogServiceAdapter(app, service, required_ontology_node_ids, host, port)
                service_adapters.append(service_adapter)

        elif section == 'jsonrpcs':
            for jsonrpc_data in data:
                ontology_node_id = jsonrpc_data.get('ontology_node_id')
                if ontology_node_id is None:
                    raise RuntimeError('You must supply a ontology_node_id for each service adapter')

                required_ontology_node_ids = jsonrpc_data.get('required_ontology_node_ids')

                url = jsonrpc_data['url']
                service = ontology.get_service(ontology_node_id)
                service_adapter = JsonRpcServiceAdapter(app, service, required_ontology_node_ids, url)
                service_adapters.append(service_adapter)

        elif section == 'modules':
            for module_data in data:
                ontology_node_id = module_data.get('ontology_node_id')
                if ontology_node_id is None:
                    raise RuntimeError('You must supply a ontology_node_id for each service adapter')

                required_ontology_node_ids = module_data.get('required_ontology_node_ids')
                if required_ontology_node_ids is None:
                    required_ontology_node_ids = []

                name = module_data['name']
                module_klass = import_string(name)
                service = ontology.get_service(ontology_node_id)
                service_adapter = module_klass(app, service, required_ontology_node_ids, name)
                service_adapters.append(service_adapter)
        else:
            raise RuntimeError('Unknown service adapter type specified: %s' % section)

    service_manager = ServiceManager(service_adapters)
    service_manager.init_all()

    app['service_manager'] = service_manager
