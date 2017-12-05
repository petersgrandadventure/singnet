#
# sn_agent/accounting/__init__.py - manages AGI token payment processing,
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from abc import ABC
from sn_agent.accounting.settings import AccountingSettings

class Accounting(ABC):
    def __init__(self, app):
        self.app = app
        self.settings = AccountingSettings()
