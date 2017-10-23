#
# sn_agent/provider.py - implementation of wrapper for  external service provider agents.
# ExternalServiceProviders use the network to connect with other Agents to have them
# perform service sub-services required for this agent to implement a service.
#
# For example, a machine learning agent that processes large amounts of data might
# use an AWS-centered service provider to store input and output files. So one of
# the services required to perform a service is to obtain input and output URLs
# which can be used for performing this agent's service. The Singnet agent
# will keep a reference to this external provider
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import jsonrpcclient

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology import Service
from sn_agent.service_adapter.base import ServiceAdapterABC


class ExternalServiceAdapter(ServiceAdapterABC):
    def __init__(self, app, agent_id, service: Service):
        super().__init__(app, service)
        self.app = app
        self.agent_id = agent_id

        # go to the DHT and get the URL for the agent
        network = self.app['network']
        # This is a hack, we should never really get more than 1 URL per agent
        agent_urls = network.dht.get(agent_id)
        self.agent_url = agent_urls[0]['url']

    def has_all_requirements(self):
        return True

    def can_perform(self) -> bool:
        result = jsonrpcclient.request(
            self.agent_url, 'can_perform',
            {
                "service_node_id": self.service.node_id
            }
        )
        return result

    def perform(self, job: JobDescriptor):
        result = jsonrpcclient.request(
            self.agent_url, 'perform',
            {
                "service_node_id": self.service.node_id,
                "job_params": job.job_parameters
            }
        )
        return result
