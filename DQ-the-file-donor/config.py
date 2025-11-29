import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URL = os.getenv("MONGO_URL")

# --- LOG CHANNEL FIX ---
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import handlers
from database.mongo import connect_mongo

bot = Client(
    "DQ-Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Connect DB
connect_mongo()

handlers.load(bot)

print("🚀 Bot Started on Koyeb!")
bot.run()