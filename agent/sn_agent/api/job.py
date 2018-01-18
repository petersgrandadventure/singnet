import logging

from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology.service_descriptor import ServiceDescriptor

logger = logging.getLogger(__name__)


async def internal_can_perform(app, service_node_id):
    # figure out what we are being asked to perform and answer
    service = ServiceDescriptor(service_node_id)
    return await can_perform_service(app, service)


async def internal_offer(app, service_node_id, price):
    service_descriptor = ServiceDescriptor(service_node_id)
    result = app['accounting'].incoming_offer(service_descriptor, price)
    return result


async def internal_perform_job(app, service_node_id, job_params):
    service_descriptor = ServiceDescriptor(service_node_id)
    job = JobDescriptor(service_descriptor, job_params)
    result = await perform_job(app, job)
    return result


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
    accounting = app['accounting']

    if accounting.job_is_contracted(job_descriptor):

        # Get the adapter for this job's service.
        service_descriptor = job_descriptor.service
        service_adapter = service_manager.get_service_adapter_for_id(service_descriptor.ontology_node_id)
        if service_adapter is None:
            raise Exception('Service not available')

        results = service_adapter.perform(job_descriptor)

    else:
        results = [{
            'error': "Job {0} has no valid contract".format(job_descriptor.error_description())
        }]

    return results
