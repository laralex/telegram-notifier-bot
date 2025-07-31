#!/usr/bin/env python

USE_TELETHON = False

from load_globals import *
import os
import telegram
import utils

if telegram.__version_info__ < (20, 0, 0, "alpha", 1):
  raise RuntimeError(f"This example is not compatible with your current Telegram bot API version {telegram.__version__}")

from telegram import ForceReply, Update, Chat
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, CallbackContext, JobQueue
)

if USE_TELETHON:
    from telethon.sync import TelegramClient
    from telethon.sessions import StringSession
    from telethon.errors import SessionPasswordNeededError

def run_in_telethon(func):
    client = TelegramClient(StringSession(CONFIG["telethon_session"]), CONFIG["api_id"], CONFIG["api_hash"])
    with client:
        return func(client)

def get_members_list(telethon_client):
    channel = telethon_client.get_entity(channel_username)

    offset = 0
    limit = 100
    all_participants = []

    while True:
        participants = telethon_client(GetParticipants(
            channel,
            ChannelParticipantsSearch(''),
            offset,
            limit,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    out = f"Total members fetched: {len(all_participants)}\n"
    for user in all_participants:
        out += f"\n{user.id} | {user.username} | {user.first_name} {user.last_name or ''}"
    return out

async def get_channel_members_count(context: ContextTypes.DEFAULT_TYPE, channel_id: str):
    chat: Chat = await context.bot.get_chat(channel_id)
    members_count = await context.bot.get_chat_member_count(chat.id)
    return members_count

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("We. Are. Ready.")

async def members_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        channel_name = CONFIG["channel_name"]
        members_count = await get_channel_members_count(context, channel_name)
        await update.message.reply_text(
            f"{EMOJIS['stats']} Members info:\n Channel: {channel_name}\nCount: {members_count}")
    except Exception as e:
        await update.message.reply_text(f"Error {utils.get_caller_function_name()}: {e}")

async def members_periodic_callback(context: CallbackContext):
    global MEMBERS_COUNT
    try:
        channel_name = CONFIG["channel_name"]
        new_members_count = await get_channel_members_count(context, channel_name)
        if new_members_count == MEMBERS_COUNT:
            return

        emoji = EMOJIS['good'] if MEMBERS_COUNT is None or new_members_count > MEMBERS_COUNT else EMOJIS['bad']

        await context.bot.send_message(
            chat_id=CONFIG["notification_chat_id"],
            text=f"{emoji} Members update\nChannel: {channel_name}\nCount: {MEMBERS_COUNT} -> {new_members_count}")

        MEMBERS_COUNT = new_members_count

        if not USE_TELETHON:
            return

        members_list = run_in_telethon(get_members_list)
        await context.bot.send_message(
            chat_id=CONFIG["notification_chat_id"],
            text=f"Members list \nChannel: {channel_name}\n{members_list}")

    except Exception as e:
        await context.bot.send_message(
            chat_id=CONFIG["notification_chat_id"],
            text=f"Error {utils.get_caller_function_name()}: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(CONFIG["bot_token"]).build()
    app.add_handler(CommandHandler("start", start_callback))
    app.add_handler(CommandHandler("members", members_callback))

    # Schedule the periodic jobs
    job_queue = app.job_queue
    job_queue.run_repeating(members_periodic_callback, interval=3600, first=1)  # Every hour

    app.run_polling()
