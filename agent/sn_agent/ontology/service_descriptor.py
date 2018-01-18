#
# service_descriptor.py - implementation of abstract class defining API for service specs.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

# Duration constants - durations are in milliseconds

import logging
from abc import ABC
from datetime import timedelta

from sn_agent.ontology import Ontology

logger = logging.getLogger(__name__)

ONE_SECOND = timedelta(seconds=1)
ONE_MINUTE = ONE_SECOND * 60
ONE_HOUR = ONE_MINUTE * 60


class ServiceDescriptor(ABC):
    def __init__(self, ontology_node_id):
        ontology = Ontology.get_global_ontology()
        self.ontology = ontology
        self.ontology_node_id = ontology_node_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def name(self):
        if self.ontology is None:
            raise RuntimeError('ServiceDescriptor missing ontology!')
        name = self.ontology.get_service_name(self.ontology_node_id)
        return name

    def __str__(self):
        name = self.name()
        return "<Service: %s - %s at %d>" % (self.ontology_node_id, name, id(self))
