import os
from pathlib import Path

from sn_agent import SettingsBase

THIS_DIR = Path(__file__).parent


class DocumentSummarizerSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self._ENV_PREFIX = 'SN_DS_'
        self.TEST_OUTPUT_DIRECTORY = os.path.join(THIS_DIR, "tests", "output")

        super().__init__(**custom_settings)
