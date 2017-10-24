import logging

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology.service_descriptor import ServiceDescriptor

logger = logging.getLogger(__name__)


async def can_perform_service(app, service_descriptor: ServiceDescriptor):
    logger.debug("get_can_perform: %s", service_descriptor)

    service_manager = app['service_manager']
    service_adapter = service_manager.get_service_adapter_for_id(service_descriptor.ontology_node_id)

    if service_adapter is None:
        raise Exception('Service not available')

    return service_adapter.can_perform()


async def perform_job(app, job_descriptor: JobDescriptor):
    logger.debug("perform_job: %s", job_descriptor)

    service_manager = app['service_manager']

    service_descriptor = job_descriptor.service

    service_adapter = service_manager.get_service_adapter_for_id(service_descriptor.ontology_node_id)

    if service_adapter is None:
        raise Exception('Service not available')

    return service_adapter.perform(job_descriptor)

