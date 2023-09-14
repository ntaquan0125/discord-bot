import os

from dotenv import load_dotenv


BOT_VERSION = 0.1


# ffmpeg tool's path
FFMPEG_PATH = "C:/Program Files/ffmpeg/bin/ffmpeg.exe"


def get_env_data(env: str):
    load_dotenv()

    return os.getenv(env, None)


def print_debug(instance, info):
    message = instance.__class__.__name__
    message += ": "
    message += info
    print(message)
