from pathlib import Path

from sn_agent.ui.handlers import IndexHandler, ServiceHandler

THIS_DIR = Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/', IndexHandler)
    app.router.add_route('*', '/service/{service_id}', ServiceHandler, name='service')
    app.router.add_static('/static/', path=str(THIS_DIR.joinpath('ui', 'static')), name='static')
