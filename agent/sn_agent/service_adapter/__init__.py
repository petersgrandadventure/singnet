import yaml

from sn_agent.utils import import_string
from sn_agent.service_adapter.jsonrpc import JsonRpcServiceAdapter
from sn_agent.service_adapter.opencog import OpenCogServiceAdapter
from sn_agent.service_adapter.settings import ServiceAdapterSettings
from sn_agent.service_adapter.manager import ServiceManager

import logging

log = logging.getLogger(__name__)

def setup_service_manager(app):
    settings = ServiceAdapterSettings()
    config_file = settings.CONFIG_FILE
    ontology = app['ontology']

    log.debug("reading configuration file {0}".format(config_file))

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
    service_manager.post_load_initialize()
    app['service_manager'] = service_manager
