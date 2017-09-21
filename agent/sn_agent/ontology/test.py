import logging

from sn_agent.ontology import DOCUMENT_SUMMARIZER_ID, IMAGE_RECOGNIZER_ID, FACE_RECOGNIZER_ID, \
    TEXT_SUMMARIZER_ID, VIDEO_SUMMARIZER_ID

logger = logging.getLogger('test')


def test_ontology(app):
    # Test that there is an ontology assigned to the app.
    ontology = app['ontology']
    assert not ontology is None

    # Test the standard services for the demo services.
    service_name = ontology.get_service_name(DOCUMENT_SUMMARIZER_ID)
    assert(service_name == 'Document Summarizer')
    service_name = ontology.get_service_name(IMAGE_RECOGNIZER_ID)
    assert(service_name == 'Image Recognizer')
    service_name = ontology.get_service_name(FACE_RECOGNIZER_ID)
    assert(service_name == 'Face Recognizer')
    service_name = ontology.get_service_name(TEXT_SUMMARIZER_ID)
    assert(service_name == 'Text Summarizer')
    service_name = ontology.get_service_name(VIDEO_SUMMARIZER_ID)
    assert(service_name == 'Video Summarizer')
