import logging

import aiohttp_jinja2 as aiohttp_jinja2
import jsonrpcclient
from aiohttp.web_exceptions import HTTPFound

logger = logging.getLogger(__name__)


@aiohttp_jinja2.template('index.jinja2')
def index(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


def do_job(request):
    response = jsonrpcclient.request('http://localhost:8000/api', 'can_perform')
    logger.debug(response)
    return HTTPFound("/")
