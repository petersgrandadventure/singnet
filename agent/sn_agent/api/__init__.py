import logging

from aiohttp import web
from jsonrpcserver.aio import methods

from sn_agent import ontology
from sn_agent.api.job import can_perform_service, perform_job
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology.service_descriptor import ServiceDescriptor

logger = logging.getLogger(__name__)


@methods.add
async def can_perform(request, context):
    # figure out what we are being asked to perform and answer
    service = ServiceDescriptor(ontology.DOCUMENT_SUMMARIZER_ID)
    app = context
    return await can_perform_service(app, service)


@methods.add
async def perform(request, context):
    job = JobDescriptor()
    app = context
    return await perform_job(app, job)


async def http_handler(request):
    request = await request.text()
    response = await methods.dispatch(request)
    if response.is_notification:
        return web.Response()
    else:
        return web.json_response(response, status=response.http_status)


def setup_api(app):
    app.router.add_post('/api', http_handler)
