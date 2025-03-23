import yaml
import os


def load_config(config_file = 'config_saved.yaml'):
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"{config_file} not found.")
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)