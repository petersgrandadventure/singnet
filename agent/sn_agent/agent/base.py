#
# sn_agent/base.py - implementation of abstract class defining API for Network
# communication with block-chain implementations through connections with
# smart contracts and block-chain messaging systems.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#
import logging
from abc import abstractmethod, ABC

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology.service_descriptor import ServiceDescriptor

logger = logging.getLogger(__name__)


class AgentABC(ABC):
    def __init__(self, app, agent_id):
        self.app = app
        self.agent_id = agent_id

    @abstractmethod
    def can_perform(self, service: ServiceDescriptor) -> bool:
        """
        :param service: the service to perform
        :result: can this agent perform the described service?
        """
        pass

    @abstractmethod
    def perform(self, job: JobDescriptor):
        """
        :param job: the service to perform
        """
        pass
