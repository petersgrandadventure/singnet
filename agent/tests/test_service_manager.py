#
# tests/test_service_manager.py - unit test for the service manager.
#
# Copyright (c) 2017 SingularityNET
#
# Distributed under the MIT software license, see LICENSE file.
#

import asyncio
from aiohttp import web

import logging
import pytest

from sn_agent.log import setup_logging
from sn_agent.service_adapter import setup_service_manager
from sn_agent import ontology
import demo


log = logging.getLogger(__name__)



class MockApp(dict):

    def __init__(self):
        self['log'] = log
        self.loop = self.wait_loop
        pass

    def wait_loop(self):
        pass


@pytest.fixture
def app():
    app = MockApp()
    ontology.setup_ontology(app)
    return app

def test_service_manager(app):
    print()
    setup_logging()
    log.debug("--- test_service_manager ---")
    setup_service_manager(app)

    # Excercise the service manager methods.
    assert(not app['service_manager'] is None)
    service_manager = app['service_manager']
    service_adapter = service_manager.get_service_adapter_for_id(demo.DOCUMENT_SUMMARIZER_ID)
    assert(not service_adapter is None)
    assert(isinstance(service_adapter, demo.document_summarizer.DocumentSummarizer))
    service_adapter = service_manager.get_service_adapter_for_id(demo.ENTITY_EXTRACTER_ID)
    assert(not service_adapter is None)
    assert (isinstance(service_adapter, demo.entity_extracter.EntityExtracter))
    service_adapter = service_manager.get_service_adapter_for_id(demo.FACE_RECOGNIZER_ID)
    assert(not service_adapter is None)
    assert (isinstance(service_adapter, demo.face_recognizer.FaceRecognizer))
    service_adapter = service_manager.get_service_adapter_for_id(demo.TEXT_SUMMARIZER_ID)
    assert(not service_adapter is None)
    assert (isinstance(service_adapter, demo.text_summarizer.TextSummarizer))
    service_adapter = service_manager.get_service_adapter_for_id(demo.VIDEO_SUMMARIZER_ID)
    assert(not service_adapter is None)
    assert (isinstance(service_adapter, demo.video_summarizer.VideoSummarizer))
    service_adapter = service_manager.get_service_adapter_for_id(demo.WORD_SENSE_DISAMBIGUATER_ID)
    assert(not service_adapter is None)
    assert(isinstance(service_adapter, demo.word_sense_disambiguater.WordSenseDisambiguater))

def test_start_stop_services(app):
    print()
    setup_logging()
    log.debug("--- test_start_stop_services ---")
    setup_service_manager(app)

    # Start and stop some services.
    assert(not app['service_manager'] is None)
    service_manager = app['service_manager']
    service_manager.start(demo.DOCUMENT_SUMMARIZER_ID)
    service_manager.start(demo.WORD_SENSE_DISAMBIGUATER_ID)
    service_manager.start(demo.ENTITY_EXTRACTER_ID)

    service_manager.stop(demo.ENTITY_EXTRACTER_ID)
    service_manager.stop(demo.WORD_SENSE_DISAMBIGUATER_ID)
    service_manager.stop(demo.DOCUMENT_SUMMARIZER_ID)

