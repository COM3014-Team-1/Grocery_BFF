import json
import os

def load_config():
    env = os.getenv('FLASK_ENV', 'development').lower()  # Get the current environment
    config_file = f'config/appsettings.{env}.config'  # Load the respective config file
    
    with open(config_file) as f:
        config = json.load(f)
    return config

appsettings = load_config()  # Load configuration into a variable
