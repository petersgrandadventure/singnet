from sn_agent_web import SettingsBase, Required


class WebSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self.ETH_CLIENT = 'http://geth:8545'
        self._ENV_PREFIX = 'SN_WEB_'
        self.COOKIE_SECRET = Required(str)
        super().__init__(**custom_settings)
