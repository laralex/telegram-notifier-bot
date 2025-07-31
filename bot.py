#!/usr/bin/env python

from load_globals import *
import os
import telegram
import utils

if telegram.__version_info__ < (20, 0, 0, "alpha", 1):
  raise RuntimeError(f"This example is not compatible with your current PTB version {telegram.__version__}")

from telegram import ForceReply, Update, Chat
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, CallbackContext, JobQueue
)

async def get_channel_members(context: ContextTypes.DEFAULT_TYPE, channel_id: str):
    chat: Chat = await context.bot.get_chat(channel_id)
    members_count = await context.bot.get_chat_member_count(chat.id)
    return members_count

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("We. Are. Ready.")

async def members_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        members_count = await get_channel_members(context, CHANNEL_ID)
        await update.message.reply_text(
            f"{EMOJIS['stats']} Members info:\n Channel: {CHANNEL_ID}\nCount: {members_count}")
    except Exception as e:
        await update.message.reply_text(f"Error {utils.get_caller_function_name()}: {e}")

async def members_periodic_callback(context: CallbackContext):
    global MEMBERS_COUNT
    try:
        new_members_count = await get_channel_members(context, CHANNEL_ID)
        if new_members_count == MEMBERS_COUNT:
            return

        emoji = EMOJIS['good'] if MEMBERS_COUNT is None or new_members_count > MEMBERS_COUNT else EMOJIS['bad']

        await context.bot.send_message(
            chat_id=NOTIFICATION_SINK_CHAT_ID,
            text=f"{emoji} Members update\nChannel: {CHANNEL_ID}\nCount: {MEMBERS_COUNT} -> {new_members_count}")

        MEMBERS_COUNT = new_members_count

    except Exception as e:
        await context.bot.send_message(
            chat_id=NOTIFICATION_SINK_CHAT_ID,
            text=f"Error {utils.get_caller_function_name()}: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_callback))
    app.add_handler(CommandHandler("members", members_callback))

    # Schedule the periodic jobs
    job_queue = app.job_queue
    job_queue.run_repeating(members_periodic_callback, interval=3600, first=1)  # Every hour

    app.run_polling()
