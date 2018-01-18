import os
from pathlib import Path

from sn_agent import SettingsBase

THIS_DIR = Path(__file__).parent


class OntologySettings(SettingsBase):
    def __init__(self, **custom_settings):
        self._ENV_PREFIX = 'SN_ONTOLOGY_'
        self.CONFIG_FILE = os.path.join(THIS_DIR, 'ontology.yml')
        super().__init__(**custom_settings)
