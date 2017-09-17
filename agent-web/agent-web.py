from aiohttp import web

from sn_agent_web.app import create_app

app = create_app()
web.run_app(app, port=8080)
