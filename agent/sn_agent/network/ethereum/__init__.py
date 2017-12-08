import json
import logging
import os
from pathlib import Path

from web3 import Web3, HTTPProvider

from sn_agent.agent.base import AgentABC
from sn_agent.network import NetworkSettings
from sn_agent.network.base import NetworkABC, ResolverABC
from sn_agent.network.enum import NetworkStatus
from sn_agent.ontology.service_descriptor import ServiceDescriptor

logger = logging.getLogger(__name__)


class MarketJob(object):
    UNKNOWN = None
    PENDING = 'pending'
    COMPLETED = 'completed'

    def __init__(self):
        self.state = self.UNKNOWN


class UnresolvedAgentException(Exception):
    pass

class AccountNotUnlockedException(Exception):
    pass


class FileResolver(ResolverABC):
    def __init__(self, lookup_file):
        self.lookup_file = lookup_file

    def resolve(self, agent_id):
        filename = self.lookup_file

        with open(filename, encoding='utf-8') as data_file:
            agent_urls = json.loads(data_file.read())

        return agent_urls.get(agent_id)



class SNNetwork(NetworkABC):
    def __init__(self, app):
        super().__init__(app)
        self.settings = NetworkSettings()
        self.client_connection = Web3(HTTPProvider(self.settings.CLIENT_URL))
        self.addresses = self.load_json('addresses.json')
        self.payload = None
        self.agent = None

        self.resolvers = []
        self.resolvers.append(FileResolver(self.settings.AGENT_URL_LOOKUP_FILE))

    async def startup(self):
        logger.debug('Starting up the network')

        self.agent = self.app['agent']

        try:
            account_address = self.client_connection.eth.coinbase

            logger.debug('Using account: %s', account_address)

            self.payload = {
                'from': account_address,
                'gas': 1500000,
                'gasPrice': 30000000
            }
            current_block = self.client_connection.eth.blockNumber
            logger.debug('Current client blocknumber: %s', current_block)

            self.join_network()

        except ConnectionError:
            logger.error('Unable to connect to the Ethereum client')

    # Implemented methods
    def join_network(self):
        logger.debug('Joining Network')
        # contract = self.get_agent_factory_contract()
        # contract.transact(self.payload).create()
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

        for resolver in self.resolvers:
            agent_url = resolver.resolve(agent_id)
            if agent_url:
                return agent_url

        raise UnresolvedAgentException(agent_id)

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

    def create_market_job(self, agents, amounts, payer, firstService, lastService):

        self.ensure_unlocked()

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

    def set_market_job_completed(self):
        contract = self.get_market_job_contract()

        self.ensure_unlocked()

        return contract.call(self.payload).setJobCompleted()

    def payAgent(self, agentAccounts):

        contract = self.get_market_job_contract()

        self.ensure_unlocked()

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

    def ensure_unlocked(self):
        unlock_state = self.client_connection.personal.unlockAccount(self.account, self.settings.ACCOUNT_PASSWORD, duration=30)

        if not unlock_state:
            raise AccountNotUnlockedException()
