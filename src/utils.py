import os
import json

from dotenv import load_dotenv


BOT_VERSION = 0.1


# ffmpeg tool's path
FFMPEG_PATH = "C:/Program Files/ffmpeg/bin/ffmpeg.exe"

STATUS_FILE_PATH = "./config/bot_status.json"
BIRTHDAY_WISH_PATH = "./config/birthday_wishes/"

DEFAULT_CONFIG_FILE_PATH = "./config/default/default_config.json"


def get_env_data(env: str):
    load_dotenv()

    return os.getenv(env, None)


def get_config_value(config: str):
    with open(DEFAULT_CONFIG_FILE_PATH) as default_config_file:
        default_config_file_contents = json.loads(default_config_file.read())

    return default_config_file_contents["default_config"][config]


def print_debug(instance, info):
    message = instance.__class__.__name__
    message += ": "
    message += info
    print(message)
