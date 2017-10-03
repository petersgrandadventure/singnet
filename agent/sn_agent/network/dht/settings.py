from sn_agent import SettingsBase


class DHTSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self.ITERATION_SLEEP = 1
        self.ID_BITS = 128
        self.ALPHA = 3
        self.K = 20
        self._ENV_PREFIX = 'SN_DHT_'

        self.USE_UPNP = True

        self.NEEDS_BOOTING = True
        self.BOOT_HOST = 'sn.jensenbox.com'
        self.BOOT_PORT = 6881

        super().__init__(**custom_settings)
