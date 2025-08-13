from dotenv import load_dotenv
import os
import yaml

load_dotenv()  # Must be at the very top

def load_config(path="config/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    def replace_env_vars(obj):
        if isinstance(obj, dict):
            return {k: replace_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_env_vars(i) for i in obj]
        elif isinstance(obj, str) and obj.startswith("${") and obj.endswith("}"):
            return os.getenv(obj[2:-1], "")
        return obj

    return replace_env_vars(config)

config = load_config()
