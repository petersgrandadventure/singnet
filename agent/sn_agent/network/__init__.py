import logging

from sn_agent.network.settings import NetworkSettings
from sn_agent.utils import import_string

logger = logging.getLogger(__name__)


def setup_network(app):
    settings = NetworkSettings()
    logger.debug('Loading network class: %s', settings.CLASS)
    klass = import_string(settings.CLASS)
    app['network'] = klass(app)
