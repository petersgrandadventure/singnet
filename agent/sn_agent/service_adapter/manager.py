#
# service_adapter/manager.py - manager for service adapters.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging


logger = logging.getLogger(__name__)


class ServiceManager:
    def __init__(self, app, service_adapters):
        self.app = app
        self.services_by_id = {}
        self.service_adapters = service_adapters
        for service_adapter in service_adapters:
            service = service_adapter.service
            self.services_by_id[service.node_id] = service_adapter

    def post_load_initialize(self):
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

    def get_service_adapter_for_id(self, service_node_id):
        service_adapter = self.services_by_id.get(service_node_id)
        if service_adapter is None:
            from sn_agent.service_adapter.external_adapter import ExternalServiceAdapter

            # go to the blockchain and get the agent
            agent_id = 'c545478a-971a-48ec-bc56-aaaaaaaaaaaa'
            service = self.app['ontology'].get_service(service_node_id)
            service_adapter = ExternalServiceAdapter(self.app, agent_id, service)
            self.services_by_id[service_node_id] = service_adapter
        return service_adapter
