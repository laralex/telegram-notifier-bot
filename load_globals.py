import logging

with open("token.txt") as f:
    BOT_TOKEN = f.read().strip()

# Your channel username and your Telegram user ID for notifications
with open("channel_id.txt") as f:
    CHANNEL_ID = f.read().strip()

with open("notification_sink_chat_id.txt") as f:
    NOTIFICATION_SINK_CHAT_ID = f.read().strip()

MEMBERS_COUNT = None

EMOJIS = dict(
    good="🟢",
    bad="🔴",
    stats="📊",
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
