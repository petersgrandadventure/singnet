from typing import List

import aiohttp
from jsonrpcclient.aiohttp_client import aiohttpClient

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.service_adapter.base import ServiceAdapterABC


class JsonRpcServiceAdapter(ServiceAdapterABC):
    type_name = "JSON-RPC"

    def __init__(self, app, service: ServiceDescriptor, required_services: List[ServiceDescriptor], url):
        super().__init__(app, service, required_services)

        self.url = url
        self.loop = app.loop

    async def can_perform(self) -> bool:

        if not self.requirements_met:
            return False

        if not self.available:
            return False

        if not self.all_required_agents_can_perform():
            return False

        async with aiohttp.ClientSession(loop=self.loop) as session:
            client = aiohttpClient(session, self.url)
            response = await client.request('can_perform')
            return response

    async def perform(self, job: JobDescriptor):
        async with aiohttp.ClientSession(loop=self.loop) as session:
            client = aiohttpClient(session, self.url)
            response = await client.request('perform', (), job)
            return response
