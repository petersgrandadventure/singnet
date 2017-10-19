import logging

from sn_agent.network.settings import NetworkSettings
from sn_agent.utils import import_string

logger = logging.getLogger(__name__)


def setup_network(app):
    settings = NetworkSettings()
    klass = import_string(settings.CLASS)
    logger.debug('Loading network class: %s', klass)
    app['network'] = klass(app)


def join_network(app):
    app['network'].join_network()
