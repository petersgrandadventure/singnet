import logging

import pytest
from sn_agent import ontology
from sn_agent.test.mocks import MockApp

logger = logging.getLogger(__name__)

@pytest.fixture
def app():
    app = MockApp()
    ontology.setup_ontology(app)
    return app

def test_ontology(app):
    # Test that there is an ontology assigned to the app.
    app_ontology = app['ontology']
    assert not app_ontology is None

    # Test the standard services for the demo services.
    service_name = app_ontology.get_service_name(ontology.DOCUMENT_SUMMARIZER_ID)
    assert(service_name == 'Document Summarizer')
    service_name = app_ontology.get_service_name(ontology.WORD_SENSE_DISAMBIGUATER_ID)
    assert(service_name == 'Word Sense Disamnbiguater')
    service_name = app_ontology.get_service_name(ontology.FACE_RECOGNIZER_ID)
    assert(service_name == 'Face Recognizer')
    service_name = app_ontology.get_service_name(ontology.TEXT_SUMMARIZER_ID)
    assert(service_name == 'Text Summarizer')
    service_name = app_ontology.get_service_name(ontology.VIDEO_SUMMARIZER_ID)
    assert(service_name == 'Video Summarizer')
    service_name = app_ontology.get_service_name(ontology.ENTITY_EXTRACTER_ID)
    assert(service_name == 'Entity Extracter')
