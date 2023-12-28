import os

from dotenv import load_dotenv


bot_version = 0.2
debug = True

load_dotenv()
token = os.getenv("DISCORD_TOKEN", None)
openai_api_key = os.getenv("OPENAI_API_KEY", None)
