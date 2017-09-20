#
# sn_agent/base.py - implementation of the ontology of services
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging

from abc import abstractmethod, ABC
from sn_agent.ontology import Service

TEST_SERVICE_NODE_1 = 'deadbeef-aaaa-bbbb-cccc-000000000001'
TEST_SERVICE_NODE_2 = 'deadbeef-aaaa-bbbb-cccc-000000000002'
TEST_SERVICE_NODE_3 = 'deadbeef-aaaa-bbbb-cccc-000000000003'
TEST_SERVICE_NODE_4 = 'deadbeef-aaaa-bbbb-cccc-000000000004'
TEST_SERVICE_NODE_5 = 'deadbeef-aaaa-bbbb-cccc-000000000005'

logger = logging.getLogger('test')

class OntologyABC(ABC):

    def __init__(self, app):
        self.app = app
        self.version = None

    @abstractmethod
    def get_service_description(self, node_id) -> str:
        """
        This is used for creating the tree of services behind a given ontology

        :param node_id: the node whose description should be returned
        :return: the description of that node
        """
        pass


class Ontology(OntologyABC):

    # Note: We are not going to rely solely on the app['ontology'] access mechanism because the
    # ontology is currently a mock of our eventual implementation which will be global and
    # accessed through updates driven by the blockchain. Since there will only be one implementation
    # there will be many objects that don't need 'app' access that will want access to the
    # ontology for id to text conversions, etc. So having a global_ontology here provides a means
    # to get the ontology without our having to pass app into lighter-weight objects like
    # ServiceDescriptor and JobDescriptor.

    global_ontology = None

    def __init__(self, app):
        logger.debug('Starting Ontology')
        super().__init__(app)
        self.services =  {}
        Ontology.register_global_ontology(self)
        logger.debug('  created Ontology')

    @classmethod
    def register_global_ontology(cls, ontology):
        cls.global_ontology = ontology

    @classmethod
    def get_global_ontology(cls) -> OntologyABC:
        return cls.global_ontology

    def add_service(self, node_id, service: Service):
        self.services[node_id] = service

    def get_service_name(self, node_id) -> str:
        service = self.services[node_id]
        return service['name']

    def get_service_description(self, node_id) -> str:
        description = self.services[node_id]['description']
        if description == None:
            description = '';
        return description

