from sn_agent.ui.handlers import index


def setup_routes(app):
    app.router.add_get('/', index)
