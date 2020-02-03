# start_bot.py
import os
from dotenv import load_dotenv

from Bot import Bot
from MyLogging import init_logger

init_logger()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = Bot(TOKEN, GUILD)
