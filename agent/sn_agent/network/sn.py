import json
import logging
import os
from pathlib import Path

from web3 import Web3, HTTPProvider

from sn_agent.agent.base import AgentABC
from sn_agent.network import NetworkSettings
from sn_agent.network.base import NetworkABC
from sn_agent.network.enum import NetworkStatus
from sn_agent.ontology.service_descriptor import ServiceDescriptor

logger = logging.getLogger(__name__)


class SNNetwork(NetworkABC):
    def __init__(self, app):
        super().__init__(app)
        self.settings = NetworkSettings()
        self.client_connection = Web3(HTTPProvider(self.settings.CLIENT_URL))
        self.addresses = self.load_json('addresses.json')
        self.agent = None
        self.payload = {
            # 'from': self.client_connection.eth.coinbase,
            'gas': 1500000,
            'gasPrice': 30000000000000
        }

    async def startup(self):
        logger.debug('Registering agent on DHT')

        self.agent = self.app['agent']

        # current_block = self.client_connection.eth.blockNumber
        # logger.debug('Current client blocknumber: %s', current_block)

        self.join_network()

    # Implemented methods
    def join_network(self):
        logger.debug('Joining Network')
        contract = self.get_agent_factory_contract()
        contract.transact(self.payload).create()
        logger.debug('Joined network')

    def advertise_service(self, service: ServiceDescriptor):
        logger.debug('Advertising service: %s', service)
        agent = self.app['agent']
        contract = self.get_agent_registry_contract()
        contract.transact(self.payload).addAgent(service, agent)
        logger.debug('Advertised service: %s', service)

    def find_service_providers(self, service: ServiceDescriptor) -> list:
        logger.debug('Finding service providers for: %s', service)
        contract = self.get_agent_registry_contract()
        result = contract.call(self.payload).getAgentsWithService(service)
        logger.debug('%s service provider(s) found for: %s', len(result), service)
        return result

    def get_url_for_agent(self, agent_id):

        filename = self.settings.AGENT_URL_LOOKUP_FILE
        with open(filename, encoding='UTF-8').read() as file_contents:
            agent_urls = json.loads(file_contents)

        url = agent_urls.get(agent_id)

        if url is None:
            # Fallback to blockchain if none specified in the lookup file
            blockchain_result = None
            # TODO implement grabbing from blockchain

        return url

    # TODO: Unimplemented methods

    def logoff_network(self) -> bool:
        return super().logoff_network()

    def update_ontology(self):
        super().update_ontology()

    def remove_service_advertisement(self, service: ServiceDescriptor):
        super().remove_service_advertisement(service)

    def is_agent_a_member(self, agent: AgentABC) -> bool:
        return super().is_agent_a_member(agent)

    def logon_network(self) -> bool:
        return super().logon_network()

    def get_network_status(self) -> NetworkStatus:
        return super().get_network_status()

    def leave_network(self) -> bool:
        return super().leave_network()

    ### These are here because they were in the original code, not sure how to use them
    def getAgentsById(self, id):
        """
        I have no idea what this does - what do you pass in here?
        :param id:
        :return:
        """
        contract = self.get_agent_registry_contract()
        return contract.call(self.payload).getAgent(id)

    def createMarketJob(self, agents, amounts, payer, firstService, lastService):
        contract = self.get_market_job_contract()
        return contract.deploy(
            transaction={
                'from': self.client_connection.eth.accounts[8],
                'value': self.client_connection.toWei(1, 'ether')},
            args=(
                agents,
                amounts,
                payer,
                firstService,
                lastService
            )
        )

    def setJobCompleted(self):
        contract = self.get_market_job_contract()
        return contract.call(self.payload).setJobCompleted()

    def payAgent(self, agentAccounts):
        contract = self.get_market_job_contract()
        return contract.call({'from': agentAccounts[0]}).withdraw()

    # Utility Functions

    def getABI(self, param):
        filename = '%s.json' % param
        data = self.load_json(filename)
        abi = data['abi']
        return abi

    def load_json(self, filename):
        filepath = os.path.join(Path(__file__).parent, 'data', filename)
        with open(filepath, encoding='utf-8') as data_file:
            return json.loads(data_file.read())

    def getAddress(self, param):
        return self.addresses[param]

    def get_agent_registry_contract(self):
        return self.get_contract('AgentRegistry')

    def get_market_job_contract(self):
        return self.get_contract('MarketJob')

    def get_agent_factory_contract(self):
        return self.get_contract('AgentFactory')

    def get_contract(self, type_name):
        abi = self.getABI(type_name)
        address = self.getAddress(type_name)
        contract = self.client_connection.eth.contract(abi=abi, address=address)
        return contract
