from urllib3.util import Url

from sn_agent import SettingsBase


class NetworkSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self._ENV_PREFIX = 'SN_NETWORK_'

        self.GATEWAY = '0.0.0.0'

        self.CLIENT_URL = 'http://testrpc:8545'

        self.CLASS = 'sn_agent.network.sn.SNNetwork'

        self.BOOT_HOST = 'bootstrap.ring.cx'
        self.BOOT_PORT = "4222"
        self.WEB_HOST = "0.0.0.0"
        self.WEB_PORT = 8000

        super().__init__(**custom_settings)

        # Must place after the init so as to pick up the proper gateway value
        self.WEB_URL = Url(scheme='http', host=self.GATEWAY, port=self.WEB_PORT, path='/api').url
