from sn_agent import SettingsBase, Required


class WebSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self.STATIC_ROOT_URL = '/static'
        self.ETH_CLIENT = 'http://geth:8545'
        self._ENV_PREFIX = 'SN_WEB_'
        self.COOKIE_SECRET = 'S^L/<cJUd$"p$5kH' # Required(str)
        super().__init__(**custom_settings)
