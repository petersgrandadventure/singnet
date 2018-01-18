#
# sn_agent/accounting/__init__.py - manages AGI token payment processing,
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from abc import ABC

from sn_agent.accounting.settings import AccountingSettings
from sn_agent.api import internal_perform_job
from sn_agent.job.job_descriptor import JobDescriptor
from sn_agent.network.ethereum.__init__ import MarketJob


class PriceTooLowException(Exception):
    pass


class IncorrectContractState(Exception):
    pass



class Accounting(ABC):
    def __init__(self, app):
        self.app = app
        self.settings = AccountingSettings()
        self.network = app['network']

    def job_is_contracted(self, job: JobDescriptor):
        if not job is None:
            return True
        else:
            return False

    def incoming_offer(self, service_id, price):

        if price < 0:
            raise PriceTooLowException()

        market_job = self.network.create_market_job(service_id, price)

        return market_job.address

    def perform_job(self, market_job_address, service_id, job_params):

        market_job = self.network.get_market_job(market_job_address)

        if market_job.state != MarketJob.PENDING:
            raise IncorrectContractState()

        result = internal_perform_job(self.app, service_id, job_params)

        market_job.set_state = MarketJob.COMPLETED
        return result


def setup_accounting(app):
    app['accounting'] = Accounting(app)
