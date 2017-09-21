#
# tests/test_service_manager.py - unit test for the service manager.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import asyncio
from aiohttp import web

import logging
import pytest

from sn_agent.log import setup_logging
from sn_agent.service_adapter import setup_service_manager
from sn_agent import ontology


log = logging.getLogger(__name__)



class MockApp(dict):

    def __init__(self):
        self['log'] = log
        self.loop = self.wait_loop
        pass

    def wait_loop(self):
        pass


@pytest.fixture
def app():
    app = MockApp()
    ontology.setup_ontology(app)
    return app

def test_service_manager(app):
    print()
    setup_logging()
    setup_service_manager(app)
