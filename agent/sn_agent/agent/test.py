#
# sn_agent/base.py - implementation of abstract class defining API for Network
# communication with block-chain implementations through connections with
# smart contracts and block-chain messaging systems.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from sn_agent.agent.base import AgentABC
from sn_agent.network.enum import NetworkStatus
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from enum import Enum

import logging

from sn_agent.agent.base import AgentABC

logger = logging.getLogger(__name__)


class TestAgent(AgentABC):

    def __init__(self, app, agent_id):
        super().__init__(app, agent_id)
        logger.debug('Test Agent Started')

    def can_perform(self, service: ServiceDescriptor) -> bool:
        pass

    def perform(self, service: ServiceDescriptor) -> bool:
        pass
