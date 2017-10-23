import logging
import os

from aiohttp import web, WSMsgType
from aiohttp.web_response import Response
from jsonrpcserver.aio import methods

from sn_agent import ontology
from sn_agent.api.job import can_perform_service, perform_job
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.ontology.service_descriptor import ServiceDescriptor

logger = logging.getLogger(__name__)

WS_FILE = os.path.join(os.path.dirname(__file__), 'websocket.html')


@methods.add
async def can_perform(service_node_id=None, context=None):
    # figure out what we are being asked to perform and answer
    service = ServiceDescriptor(service_node_id)
    app = context
    return await can_perform_service(app, service)


@methods.add
async def perform(service_node_id=None, job_params=None, context=None):
    service_descriptor = ServiceDescriptor(service_node_id)

    job = JobDescriptor(service_descriptor, job_params)
    app = context

    result = await perform_job(app, job)
    logging.debug('Result of perform was %s', result)
    return result


async def http_handler(request):
    app = request.app
    request_text = await request.text()

    response = await methods.dispatch(request_text, app)
    if response.is_notification:
        return web.Response()
    else:
        return web.json_response(response, status=response.http_status)


async def ws_handler(request):
    logger.debug('WebSocket Handler started')

    app = request.app

    resp = web.WebSocketResponse()

    ok, protocol = resp.can_prepare(request)
    if not ok:
        with open(WS_FILE, 'rb') as fp:
            return Response(body=fp.read(), content_type='text/html')

    await resp.prepare(request)

    logger.debug('WebSocket data received')

    try:

        request.app['sockets'].append(resp)

        async for msg in resp:

            logger.debug('Processing WebSocket message: %s', msg.type)

            if msg.type == WSMsgType.TEXT:

                response = await methods.dispatch(msg.data, app)
                if not response.is_notification:
                    await resp.send_str(str(response))

            elif msg.type == WSMsgType.ERROR:
                logger.debug('ws connection closed with exception %s' % resp.exception())

            else:
                logger.debug("Unhandled message type")
                return resp
        return resp

    finally:
        request.app['sockets'].remove(resp)
        logger.debug('Someone disconnected.')


async def on_shutdown(app):
    for ws in app['sockets']:
        await ws.close()


def setup_api(app):
    app['sockets'] = []
    app.router.add_post('/api', http_handler)
    app.router.add_get('/api/ws', ws_handler)
    app.on_shutdown.append(on_shutdown)
