import yaml

import logging

from sn_agent.ontology.settings import OntologySettings
from sn_agent.utils import import_string

logger = logging.getLogger('test')

class Service(dict):
    def __init__(self, node_id, name, description):
        self.node_id = node_id
        self.name = name
        self.description = description


def setup_ontology(app):
    settings = OntologySettings()
    ontology_klass = import_string(settings.ONTOLOGY_CLASS)
    ontology = ontology_klass(app)
    app['ontology'] = ontology

    config_file = settings.CONFIG_FILE

    with open(config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    # jobs = []

    for section, section_items in cfg.items():
        logger.debug('parsing section: {0}'.format(section))
        if section == 'services':
            for service_data in section_items:
                ontology_node_id = service_data['ontology_node_id']
                # ontology_node_id = data.get('ontology_node_id')
                if ontology_node_id is None:
                    raise RuntimeError('You must supply a ontology_node_id for each service')

                name = service_data['name']
                if name is None:
                    raise RuntimeError('You must supply a name for each service')

                description = service_data['name']

                # Add the rest of the items to the service.
                logger.debug('adding service {0} - {1}'.format(ontology_node_id, name))
                service = Service(ontology_node_id, name, description)
                service.update(service_data)

                ontology.add_service(ontology_node_id, service)

        else:
            raise RuntimeError('Unknown ontology section type specified: %s' % section)

