import os
from pathlib import Path

from sn_agent import SettingsBase

DEMO_PARENT_DIR = Path(__file__).parent.parent.parent


class DocumentSummarizerSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self._ENV_PREFIX = 'SN_DS_'
        self.TEST_OUTPUT_DIRECTORY = os.path.join(DEMO_PARENT_DIR, "tests", "output")

        super().__init__(**custom_settings)
