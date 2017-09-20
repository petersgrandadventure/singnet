#
# service_descriptor.py - implementation of abstract class defining API for service specs.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

# Duration constants - durations are in milliseconds
from abc import ABC
from datetime import timedelta
from sn_agent.ontology.base import Ontology

ONE_SECOND = timedelta(seconds=1)
ONE_MINUTE = ONE_SECOND * 60
ONE_HOUR = ONE_MINUTE * 60


class ServiceDescriptor(ABC):
    def __init__(self, ontology_node_id):
        self.ontology = Ontology.get_global_ontology()
        self.ontology_node_id = ontology_node_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def name(self):
        name = self.ontology.get_service_name(self.ontology_node_id)
        return name

    def __str__(self):
        name = self.name()
        return "<Service: %i, %s>" % (self.ontology_node_id, name)
