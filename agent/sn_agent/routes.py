from pathlib import Path

import sn_agent.ui.handlers as handlers
from sn_agent.ui.handlers import index

THIS_DIR = Path(__file__).parent

def setup_routes(app):
    app.router.add_get('/', index)

    for adapter in app['service_manager'].service_adapters:
        route_name = adapter.service.name.replace(' ', '').lower()
        handler = getattr(handlers, route_name)
        app.router.add_get('/' + route_name, handler)

    app.router.add_static('/static/', path=str(THIS_DIR / 'static'), name='static')
