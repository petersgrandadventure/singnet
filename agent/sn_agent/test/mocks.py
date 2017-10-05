import logging
import asyncio


class MockApp(dict):

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        pass


