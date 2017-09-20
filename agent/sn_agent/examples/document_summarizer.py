#
# sn_agent/document_summarizer.py - a toy example document summaraizer.
#
# The examples in the sn_agent/examples are here to illustrate how a complex set
# of agents can interact together to deilver a service through SingulartyNET.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

from sn_agent.service_adapter.base import ServiceAdapterABC

class DocumentSummarizer(ServiceAdapterABC):
    type_name = "DocumentSummarizer"

    def __init__(self, app):
        super().__init__(app)
        self.host = host
        self.port = port

    def perform(self, *args, **kwargs):
        pass
