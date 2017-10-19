import json
import logging

from sn_agent.agent.base import AgentABC
from sn_agent.network import NetworkSettings
from sn_agent.network.base import NetworkABC
from sn_agent.network.blockchain import BlockChain
from sn_agent.network.dht import DHT
from sn_agent.network.enum import NetworkStatus
from sn_agent.ontology.service_descriptor import ServiceDescriptor

logger = logging.getLogger(__name__)


class SNNetwork(NetworkABC):
    def __init__(self, app):
        super().__init__(app)
        self.settings = NetworkSettings()
        self.blockchain = BlockChain(self.settings.CLIENT_URL)
        self.dht = DHT(self.settings.BOOT_HOST, self.settings.BOOT_PORT)

    async def startup(self):
        logger.debug('Registering agent on DHT')

        agent = self.app['agent']
        agent_id = agent.agent_id
        agent_id_str = str(agent_id)

        self.dht.put(agent_id_str, {'url': "%s://%s:%s/api/ws" % ('http', self.settings.WEB_HOST, self.settings.WEB_PORT)}, 1)

    def find_service_providers(self, service: ServiceDescriptor) -> list:
        return self.blockchain.get_agents_for_ontology(service.ontology_node_id)

    def logoff_network(self) -> bool:
        return super().logoff_network()

    def update_ontology(self):
        super().update_ontology()

    def join_network(self) -> bool:
        def getAddressByName(addresses, name):
            for key, value in addresses.items():
                if key == name:
                    return value

        def parseAbi(data):
            for key, value in data.items():
                if key == 'abi':
                    return value

        payload = {'from': web3.eth.coinbase, 'gas': 1500000, 'gasPrice': 30000000000000}
        agentFactoryAbi = parseAbi(json.loads(open('../build/contracts/AgentFactory.json', 'r').read()))
        agentFactoryAddress = getAddressByName(json.loads(open('../addresses.json', 'r').read()), 'AgentFactory')
        agentFactoryContract = web3.eth.contract(abi=agentFactoryAbi, address=agentFactoryAddress)

        return agentFactoryContract.transact(payload).create()

    def remove_service_advertisement(self, service: ServiceDescriptor):
        super().remove_service_advertisement(service)

    def advertise_service(self, service: ServiceDescriptor):
        super().advertise_service(service)

    def is_agent_a_member(self, agent: AgentABC) -> bool:
        return super().is_agent_a_member(agent)

    def logon_network(self) -> bool:
        return super().logon_network()

    def get_network_status(self) -> NetworkStatus:
        return super().get_network_status()

    def leave_network(self) -> bool:
        return super().leave_network()

