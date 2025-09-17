import json

from emsoft.common.emsoft_config import EMSoftConfig

def load_default_config(config_class: EMSoftConfig):
    with open("dummy", "r") as f:
        data = json.load(f)

