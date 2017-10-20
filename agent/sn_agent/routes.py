from sn_agent import api
from sn_agent.ui.handlers import index, do_job


def setup_routes(app):
    app.router.add_get('', index)
    app.router.add_post('', do_job)
