import os
from pathlib import Path

from urllib3.util import Url

from sn_agent import SettingsBase

THIS_DIR = Path(__file__).parent


class NetworkSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self._ENV_PREFIX = 'SN_NETWORK_'

        self.GATEWAY = '0.0.0.0'

        self.CLIENT_URL = 'http://testrpc:8545'

        self.CLASS = 'sn_agent.network.sn.SNNetwork'

        self.WEB_HOST = "0.0.0.0"
        self.WEB_PORT = 8000

        self.AGENT_URL_LOOKUP_FILE = os.path.join(THIS_DIR, 'data', 'agent_to_url_lookup.json')
        self.COINBASE = '0x633a490e1d3022a90e49cfb79ff8789d264ae753'

        super().__init__(**custom_settings)

        # Must place after the init so as to pick up the proper gateway value
        self.WEB_URL = Url(scheme='http', host=self.GATEWAY, port=self.WEB_PORT, path='/api').url
