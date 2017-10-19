import uuid

from sn_agent import SettingsBase, Required


class AgentSettings(SettingsBase):
    def __init__(self, **custom_settings):
        self._ENV_PREFIX = 'SN_AGENT_'
        self.CLASS = 'sn_agent.agent.test.TestAgent'
        self.ID = Required(uuid.UUID)
        self.WEB_HOST = "0.0.0.0"
        self.WEB_PORT = 8000
        super().__init__(**custom_settings)
