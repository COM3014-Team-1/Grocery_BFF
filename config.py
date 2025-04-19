import json
import os

def load_config():
    env = os.getenv('FLASK_ENV', 'development').lower()
    config_file = f'config/appsettings.{env}.config'

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file) as f:
        config = json.load(f)

    return config


appsettings = load_config()  # Load configuration into a variable

