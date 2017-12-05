#
# sn_agent/accounting/__init__.py - manages AGI token payment processing,
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from abc import ABC
from sn_agent.accounting.settings import AccountingSettings
from sn_agent.job.job_descriptor import JobDescriptor

class Accounting(ABC):
    def __init__(self, app):
        self.app = app
        self.settings = AccountingSettings()

    def job_is_contracted(self, job: JobDescriptor):
        if not job is None:
            return True
        else:
            return False

def setup_accounting(app):
    app['accounting'] = Accounting(app)
