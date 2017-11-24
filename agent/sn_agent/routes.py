from pathlib import Path

from sn_agent.ui.handlers import index

THIS_DIR = Path(__file__).parent

def setup_routes(app):
    app.router.add_get('/', index)

    app.router.add_static('/static/', path=str(THIS_DIR / 'static'), name='static')
