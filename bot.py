import logging
import logging.config

# Logging Config
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media, Media2, choose_mediaDB, db as clientDB
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL, SECONDDB_URI
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script 
from datetime import date, datetime 
import pytz
from sample_info import tempDict

from aiohttp import web

async def health(request):
    return web.Response(text="OK")

def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)
    web.run_app(app, port=8000)

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=10,
        )

    async def start(self):
        # Load banned users/chats
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats

        await super().start()

        await Media.ensure_indexes()
        await Media2.ensure_indexes()

        # DB Space check
        stats = await clientDB.command('dbStats')
        free_dbSize = round(512 - ((stats['dataSize']/(1024*1024)) + (stats['indexSize']/(1024*1024))), 2)

        if SECONDDB_URI and free_dbSize < 10:
            tempDict["indexDB"] = SECONDDB_URI
            logging.info(f"Primary DB has only {free_dbSize} MB, using Secondary DB.")
        elif SECONDDB_URI is None:
            logging.error("Missing SECONDDB_URI. Exiting!")
            exit()
        else:
            logging.info(f"Primary DB has enough space ({free_dbSize}MB).")

        await choose_mediaDB()

        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username

        logging.info(f"{me.first_name} running Pyrogram v{__version__} (Layer {layer}).")
        logging.info(LOG_STR)
        logging.info(script.LOGO)

        # Prepare Restart Message
        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")

        # Safe Logging to Log Channel
        try:
            log_channel_id = int(LOG_CHANNEL)
            await self.send_message(
                chat_id=log_channel_id,
                text=script.RESTART_TXT.format(today, time)
            )
        except Exception as e:
            logging.error(f"❌ Log Channel Error: {e}")
            logging.warning("Bot is running, but unable to send log to LOG_CHANNEL.")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1

import threading
from app import start_web_server

threading.Thread(target=start_web_server).start()

app = Bot()
app.run()