import asyncio
import logging

import uvloop
from aiohttp import web

from sn_agent_web.jinja import setup_jinja
from sn_agent_web.log import setup_logging
from sn_agent_web.middleware import setup_middleware
from sn_agent_web.routes import setup_routes
from sn_agent_web.session import setup_session

logger = logging.getLogger(__file__)


def create_app():
    # Significant performance improvement: https://github.com/MagicStack/uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    app = web.Application()
    setup_logging()
    setup_session(app)
    setup_middleware(app)
    setup_jinja(app)
    setup_routes(app)

    app['name'] = 'SingularityNET Agent Web'

    return app
