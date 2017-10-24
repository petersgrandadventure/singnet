import logging

import aiohttp_jinja2 as aiohttp_jinja2

logger = logging.getLogger(__name__)


@aiohttp_jinja2.template('index.jinja2')
def index(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}
