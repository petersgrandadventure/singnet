
from abc import abstractmethod
from sn_agent.network.base import NetworkABC
from sn_agent.network.enum import NetworkStatus
from sn_agent.network.geth.poller import setup_poller
from sn_agent.ontology.service_descriptor import ServiceDescriptor


class GethNetwork(NetworkABC):
    def remove_service_advertisement(self, service: ServiceDescriptor):
        pass

    def update_ontology(self):
        pass

    def get_network_status(self) -> NetworkStatus:
        pass

    def logoff_network(self) -> bool:
        pass

    def advertise_service(self, service: ServiceDescriptor):
        pass

    def leave_network(self) -> bool:
        pass

    def logon_network(self) -> bool:
        pass

    def find_service_providers(self, service: ServiceDescriptor) -> list:
        pass

    def join_network(self) -> bool:
        pass

    def __init__(self, app):
        super().__init__(app)
        setup_poller(app)

    @abstractmethod
    def join(self) -> bool:
        """
        Agent calls this the first time to connect to the network. An Private and Public key should be returned
        """
        pass

    @abstractmethod
    def leave(self) -> bool:
        """
        Should this do something in the blockchain or just delete the public and private keys?
        """
        pass

    @abstractmethod
    def status(self) -> bool:
        """
        Determine what the current network status is (joined or not joined)
        :return:
        """
        pass

    @abstractmethod
    def get_ontology(self):
        """
        Asks for the latest ontology from wherever it is stored.
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def advertise(self, agent_id: str, service: ServiceDescriptor) -> bool:
        """
        Given an ontology, advertise it as a service that the agent provides
        :param agent_id:
        :param service:
        :return:
        """
        pass

    @abstractmethod
    def deadvertise(self, agent_id: str, service: ServiceDescriptor) -> bool:
        """
        Remove the advertisement of the service for a given agent
        :param agent_id:
        :param service:
        :return:
        """
        pass

    @abstractmethod
    def find_providers(self, service: ServiceDescriptor) -> list:
        """
        Called by the UI as well as find_provider - should return a list that contains information about all the providers that have indicated that they can proved the designated service
        :param service:
        :return:
        """
        pass

    @abstractmethod
    def ask_agent_if_can_perform(self, agent_id, service: ServiceDescriptor) -> bool:
        """
        :param agent_id:
        :param service:
        :return:
        """
        pass

    @abstractmethod
    def ask_agent_to_perform(self, agent_id, service: ServiceDescriptor, json_content) -> bool:
        """

        :return:
        """
        pass

    @abstractmethod
    def ask_agent_for_their_providers(self, agent_id, service: ServiceDescriptor) -> list:
        """
        This is used for creating the tree of services behind a given ontology

        :param agent_id:
        :param service:
        :return:
        """
        pass

    def can_i_perform(self, service: ServiceDescriptor) -> bool:
        """
        This is a request coming from the network asking if I can actually do the service

        :param service:
        :return:
        """
        pass

    def perform(self, service: ServiceDescriptor, json_content) -> bool:
        """
        This will instruct the worker to do the task requested

        :param service:
        :param json_content:
        :return:
        """
        pass
