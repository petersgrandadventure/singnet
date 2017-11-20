import os
from pathlib import Path

from sn_agent import SettingsBase

DEMO_PARENT_DIR = Path(__file__).parent.parent.parent


class AigentsSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self._ENV_PREFIX = 'SN_AIGENTS_'
        self.AIGENTS_PATH = 'https://aigents.com/al/'
        self.AIGENTS_LOGIN_EMAIL = 'aigents@singularitynet.io'
        self.AIGENTS_SECRET_QUESTION = '2+2*2'
        self.AIGENTS_SECRET_ANSWER = 'six'

        super().__init__(**custom_settings)
