import logging

from sn_agent.ontology.base import Ontology
from sn_agent.ontology.job_descriptor import JobDescriptor
from sn_agent.ontology.base import Ontology

logger = logging.getLogger(__name__)

logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class TestOntology(Ontology):
    def __init__(self, app):
        super().__init__(app)

    def test_job_execution(self):
        test_jobs = JobDescriptor.get_test_jobs()
        logger.debug('Testing jobs')
        for job in test_jobs:
            logger.debug('    job %s' % job)

