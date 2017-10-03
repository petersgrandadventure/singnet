import logging

from sn_agent.agent.base import AgentABC
from sn_agent.network.base import NetworkABC
from sn_agent.network.dht.dht import DHT
from sn_agent.network.enum import NetworkStatus
from sn_agent.ontology.service_descriptor import ServiceDescriptor

logger = logging.getLogger(__name__)


class DHTNetwork(NetworkABC):
    def __init__(self, app):
        super().__init__(app)

        self.dht = DHT()

    def update_ontology(self):
        super().update_ontology()

    def is_agent_a_member(self, agent: AgentABC) -> bool:
        return super().is_agent_a_member(agent)

    def leave_network(self) -> bool:
        return super().leave_network()

    def join_network(self) -> bool:
        agent = self.app['agent']
        agent_id = str(agent.agent_id)
        self.dht[agent_id] = self.dht.my_id

    def get_network_status(self) -> NetworkStatus:
        return super().get_network_status()

    def advertise_service(self, service: ServiceDescriptor):
        super().advertise_service(service)

    def logon_network(self) -> bool:
        return super().logon_network()

    def find_service_providers(self, service: ServiceDescriptor) -> list:
        return super().find_service_providers(service)

    def remove_service_advertisement(self, service: ServiceDescriptor):
        super().remove_service_advertisement(service)

    def logoff_network(self) -> bool:
        return super().logoff_network()
