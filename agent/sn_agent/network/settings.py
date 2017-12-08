import os
from pathlib import Path

from urllib3.util import Url

from sn_agent import SettingsBase, Required

THIS_DIR = Path(__file__).parent


class NetworkSettings(SettingsBase):
    def __init__(self, **custom_settings):


        self._ENV_PREFIX = 'SN_NETWORK_'

        self.GATEWAY = '0.0.0.0'

        self.CLIENT_URL = 'http://testrpc:8545'
        self.ACCOUNT_PASSWORD = Required(str)

        self.CLASS = 'sn_agent.network.ethereum.SNNetwork'

        self.WEB_HOST = "0.0.0.0"
        self.WEB_PORT = 8000

        self.SSL_CERTIFICATE_FILE = None
        self.SSL_KEYFILE = None

        self.AGENT_URL_LOOKUP_FILE = os.path.join(THIS_DIR, 'data', 'agent_to_url_lookup.json')

        super().__init__(**custom_settings)

        # Must place after the init so as to pick up the proper gateway value
        self.WEB_URL = Url(scheme='http', host=self.GATEWAY, port=self.WEB_PORT, path='/api').url
