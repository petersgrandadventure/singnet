from aiohttp import web

from sn_agent.agent import AgentSettings
from sn_agent.app import create_app
import ssl

import logging

logger = logging.getLogger(__name__)

app = create_app()

# sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
# sslcontext.load_cert_chain('server.crt', 'server.key')

# TODO Make the port configurable from the ENV
# web.run_app(app, port=8000, ssl_context=sslcontext)

settings = AgentSettings()

logger.info('Host setting: %s', settings.WEB_HOST)

web.run_app(app, port=settings.WEB_PORT)
