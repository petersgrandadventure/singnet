from typing import List

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.service_adapter.base import ServiceAdapterABC


class OpenCogServiceAdapter(ServiceAdapterABC):
    type_name = "OpenCog"

    def __init__(self, app, service: ServiceDescriptor, required_services: List[ServiceDescriptor], host, port):
        super().__init__(app, service, required_services)
        self.host = host
        self.port = port

    def perform(self, job: JobDescriptor):
        pass
