import logging
from urllib.parse import urlparse

import aiohttp

from sn_agent import ontology

logger = logging.getLogger(__name__)


async def submit_job(context=None):
    process_job(context)

    return 'pong'


async def process_job(app):
    logger.debug("Job submission")

    blockchain = app['blockchain']
    dht = app['dht']

    ontology_id = ontology.DOCUMENT_SUMMARIZER_ID
    agent_ids = blockchain.get_agents_for_ontology(ontology_id)

    available_agents = []
    for agent_id in agent_ids:

        connection_info = dht.get(agent_id)

        for value in connection_info:
            logger.debug('received value: %s', value)

            if isinstance(value, dict):
                if 'url' in value.keys():
                    url = urlparse(value['url'])
                    url_str = url.geturl()

                    logger.debug('Connection URL: %s', url_str)
                    # if url.scheme == 'ws' or url.scheme == 'wss':

                    try:
                        session = aiohttp.ClientSession()
                        async with session.ws_connect(url_str, heartbeat=10000) as ws:

                            logger.debug("************** Successfully connected to %s", url)
                            async for msg in ws:
                                if msg.type == aiohttp.WSMsgType.TEXT:
                                    if msg.data == 'close cmd':
                                        await ws.close()
                                        break
                                    else:
                                        await ws.send_str(msg.data + '/answer')
                                elif msg.type == aiohttp.WSMsgType.CLOSED:
                                    break
                                elif msg.type == aiohttp.WSMsgType.ERROR:
                                    break

                    except aiohttp.ClientConnectorError:
                        logger.error('Client Connector error for: %s', url_str)
                        pass

                    except aiohttp.ServerDisconnectedError:
                        logger.error('Server disconnected error for: %s', url_str)
                        pass

                    except aiohttp.WSServerHandshakeError:
                        logger.error('Incorrect WS handshake for: %s', url_str)
                        pass

                    except aiohttp.ClientOSError:
                        logger.error('Client OS error for: %s', url_str)
                        pass

                    finally:
                        session.close()
