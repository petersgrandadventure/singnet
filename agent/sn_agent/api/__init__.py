import logging
import os
import aiohttp_cors

from aiohttp import web, WSMsgType
from aiohttp.web_response import Response
from jsonrpcserver.aio import methods

from sn_agent.api.job import internal_perform_job, internal_offer, internal_can_perform

logger = logging.getLogger(__name__)

WS_FILE = os.path.join(os.path.dirname(__file__), 'websocket.html')


@methods.add
async def can_perform(service_node_id=None, context=None):
    logging.debug('Starting can perform for %s with params of %s', service_node_id)
    result = await internal_can_perform(context, service_node_id)
    logging.debug('Result of perform was %s', result)
    return result


@methods.add
async def perform(service_node_id=None, job_params=None, context=None):
    logging.debug('Starting perform for %s with params of %s', service_node_id, job_params)
    result = await internal_perform_job(context, service_node_id, job_params)
    logging.debug('Result of perform was %s', result)
    return result


@methods.add
async def offer(service_node_id=None, job_params=None, context=None):
    price = job_params
    logging.debug('Starting offer for %s with price of %s', service_node_id, price)
    result = await internal_offer(context, service_node_id, price)
    logging.debug('Result of offer was %s', result)
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
    # app.router.add_post('/api', http_handler)
    # app.router.add_get('/api/ws', ws_handler)

    # Setup CORS - cross domain support
    cors = aiohttp_cors.setup(app)
    resource = cors.add(app.router.add_resource("/api"))
    cors.add(
        resource.add_route("POST", http_handler), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers=("X-Custom-Server-Header",),
                allow_headers=("X-Requested-With", "Content-Type"),
                max_age=3600,
            )
        })

    resource = cors.add(app.router.add_resource("/api/ws"))
    cors.add(
        resource.add_route("GET", http_handler), {
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers=("X-Custom-Server-Header",),
                allow_headers=("X-Requested-With", "Content-Type"),
                max_age=3600,
            )
        })

    app.on_shutdown.append(on_shutdown)
