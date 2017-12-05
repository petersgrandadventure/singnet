import asyncio
import logging

import uvloop
from aiohttp import web

from sn_agent.accounting import setup_accounting
from sn_agent.agent import setup_agent
from sn_agent.api import setup_api
from sn_agent.log import setup_logging
from sn_agent.network import setup_network
from sn_agent.ontology import setup_ontology
from sn_agent.routes import setup_routes

from sn_agent.service_adapter import setup_service_manager
from sn_agent.ui import setup_ui

logger = logging.getLogger(__name__)


async def startup(app):
    await app['network'].startup()


def create_app():
    # Significant performance improvement: https://github.com/MagicStack/uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    app = web.Application()
    setup_logging()

    setup_ontology(app)
    setup_network(app)
    setup_service_manager(app)
    setup_accounting(app)
    setup_api(app)
    setup_agent(app)
    setup_routes(app)
    setup_ui(app)

    app['name'] = 'SingularityNET Agent'

    app.on_startup.append(startup)

    return app
