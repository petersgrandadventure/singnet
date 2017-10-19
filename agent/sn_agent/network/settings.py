from urllib3.util import Url

from sn_agent import SettingsBase, Required


class NetworkSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self.CLIENT_URL = 'http://192.168.16.17:8545'
        self._ENV_PREFIX = 'SN_NETWORK_'

        self.WEB_PORT = 8000
        self.WEB_HOST = '0.0.0.0'

        self.CLASS = 'sn_agent.network.sn.SNNetwork'

        self.BOOT_HOST = 'bootstrap.ring.cx'
        self.BOOT_PORT = "4222"

        # self.BLOCKCHAIN_CLIENT = Required(Url)

        super().__init__(**custom_settings)
