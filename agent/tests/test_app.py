#
# tests/test_app.py - unit test for the app.
#
# Copyright (c) 2018 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from sn_agent.app import create_app


def test_aop():
    app = create_app()
    assert (not app is None)
