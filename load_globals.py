import logging
import yaml

# Load configuration from a YAML file
with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

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
