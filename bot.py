import os
import logging
import threading
from pyrogram import Client, filters
from app import start_web_server
start_web_server()  
# health check server

# --------------------
# Logging Setup
# --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger("bot")

# --------------------
# ENV VARIABLES
# --------------------
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))

# --------------------
# Bot Setup
# --------------------
bot = Client(
    "DQ-Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --------------------
# START HANDLER
# --------------------
@bot.on_message(filters.command("start"))
async def start_cmd(_, message):
    user = message.from_user.id
    await message.reply("Bot is working fine! 🚀")

    # Send log
    if LOG_CHANNEL:
        try:
            await bot.send_message(LOG_CHANNEL, f"✨ User started: `{user}`")
        except Exception as e:
            log.error(f"❌ Log Channel Error: {e}")

# --------------------
# Start Web Server Thread
# --------------------
threading.Thread(target=start_web_server, daemon=True).start()
log.info("🌐 WebServer running on port 8000.")

# --------------------
# Run Bot
# --------------------
log.info("🤖 Bot Started Successfully!")
bot.run()