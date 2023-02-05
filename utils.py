import os

# from dotenv import load_dotenv


BOT_VERSION = 0.1

# load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", None)
GUILD = os.getenv("DISCORD_GUILD", None)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN", None)

# ffmpeg tool's path
FFMPEG_PATH = "C:/Program Files/ffmpeg/bin/ffmpeg.exe"


def print_debug(instance, info):
    message = instance.__class__.__name__
    message += ": "
    message += info
    print(message)
