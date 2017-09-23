import logging


class MockApp(dict):

    def __init__(self):
        self.loop = self.wait_loop
        pass

    def wait_loop(self):
        pass

