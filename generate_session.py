from load_globals import *

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

with TelegramClient(StringSession(), CONFIG["api_id"], CONFIG["api_hash"]) as client:
    print("Logged in as:", client.get_me().username)
    print("Your session string:\n")
    print(client.session.save())