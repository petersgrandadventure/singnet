from sn_agent.service_adapter.base import ServiceAdapterABC

from sn_agent.ontology.service_descriptor import ServiceDescriptor
from sn_agent.ontology.job_descriptor import JobDescriptor

from typing import List

class OpenCogServiceAdapter(ServiceAdapterABC):
    type_name = "OpenCog"

    def __init__(self, app, service: ServiceDescriptor, required_services: List[ServiceDescriptor], host, port):
        super().__init__(app, service, required_services)
        self.host = host
        self.port = port

    def perform(self, job: JobDescriptor):
        pass
