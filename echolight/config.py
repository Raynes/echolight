import json
from phue import Bridge


class EcholightConfig:
    def __init__(self, conf="config.json"):
        self._conf_file = conf
        self._bridge = None
        self._groups = None
        self.load_config()

    def load_config(self):
        with open(self._conf_file, 'r') as f:
            self._conf = json.load(f)

    @property
    def username(self):
        return self._conf['username']

    @property
    def bridgeIp(self):
        return self._conf['ip']

    @property
    def bridge(self):
        if self._bridge:
            return self._bridge
        else:
            self._bridge = Bridge(self.bridgeIp, username=self.username)
            return self._bridge

    @property
    def lights(self):
        """Map of light names to Light objects"""
        return self.bridge.get_light_objects('name')

    @property
    def presets(self):
        """Map of presets to the relevant data to set it."""
        return self._conf["presets"]

    @property
    def groups(self):
        """Map of group names to group objects."""
        groups = {}
        for group in self.bridge.groups:
            groups[group.name] = group
        return groups
