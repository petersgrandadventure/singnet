import logging

from sn_agent.job.job_descriptor import init_test_jobs
from sn_agent.ontology import setup_ontology
from sn_agent.ontology.test import test_ontology
from tests.test_service_adapter import test_perform_services

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

format = logging.Formatter('%(filename)-30sL:%(lineno)3d %(asctime)s %(levelname)-8s: %(message)s', datefmt = '%d-%m-%Y %H:%M:%S')
log_handler = logging.StreamHandler()
log_handler.setLevel(logging.DEBUG)
log_handler.setFormatter(format)
log.addHandler(log_handler)

log.debug('Starting test')


class MockApp(dict):
    def __init__(self):
        self['log'] = log
        pass


def create_mock_app():
    app = MockApp()
    setup_ontology(app)
    return app


# Create the app which tested components will need to interact with.
app = create_mock_app()

# Initialize tests
init_test_jobs()

# Run subsystem tests.
test_ontology(app)
test_perform_services(app)

