import logging

import yaml

from sn_agent.ontology.settings import OntologySettings

logger = logging.getLogger(__name__)


class Service(dict):
    def __init__(self, node_id, name, description):
        super().__init__()
        self.node_id = node_id
        self.name = name
        self.description = description


class Ontology(object):
    # Note: We are not going to rely solely on the app['ontology'] access mechanism because the
    # ontology is currently a mock of our eventual implementation which will be global and
    # accessed through updates driven by the blockchain. Since there will only be one implementation
    # there will be many objects that don't need 'app' access that will want access to the
    # ontology for id to text conversions, etc. So having a global_ontology here provides a means
    # to get the ontology without our having to pass app into lighter-weight objects like
    # ServiceDescriptor and JobDescriptor.

    global_ontology = None

    def __init__(self, app):
        super().__init__()
        self.services = {}
        Ontology.register_global_ontology(self)

    @classmethod
    def register_global_ontology(cls, ontology):
        cls.global_ontology = ontology

    @classmethod
    def get_global_ontology(cls):
        return cls.global_ontology

    def add_service(self, node_id, service: Service):
        self.services[node_id] = service

    def get_service(self, node_id) -> Service:
        service = self.services[node_id]
        return service

    def get_service_name(self, node_id) -> str:
        service = self.services[node_id]
        return service['name']

    def get_service_description(self, node_id) -> str:
        service = self.services[node_id]
        return service['description']


def setup_ontology(app):
    settings = OntologySettings()
    ontology = Ontology(app)
    app['ontology'] = ontology

    config_file = settings.CONFIG_FILE

    logger.debug("Loading config file: %s", config_file)
    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    for section, section_items in cfg.items():
        logger.debug('parsing section: {0}'.format(section))
        if section == 'services':
            for service_data in section_items:
                ontology_node_id = service_data.get('ontology_node_id')
                if ontology_node_id is None:
                    raise RuntimeError('You must supply a ontology_node_id for each service')

                name = service_data.get('name')
                if name is None:
                    raise RuntimeError('You must supply a name for each service')

                description = service_data.get('description')
                if description is None:
                    description = name

                # Add the rest of the items to the service.
                logger.debug("adding Service to ontology %s - %s", ontology_node_id, name)
                # print("adding Service to ontology {0} - {1}".format(ontology_node_id, name))
                service = Service(ontology_node_id, name, description)
                service.update(service_data)

                ontology.add_service(ontology_node_id, service)

        else:
            raise RuntimeError('Unknown ontology section type specified: %s' % section)
