#
# tests/test_app.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import logging

from sn_agent.test.mocks import MockApp
from sn_agent.utils import import_string

log = logging.getLogger(__name__)


def test_utils():
    klass = import_string("sn_agent.network.test.TestNetwork")
    app = MockApp()
    network = klass(app)

    network.join_network()
    network.logon_network()
    network.logoff_network()
    network.leave_network()
