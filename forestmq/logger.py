import logging

logging.basicConfig(level=logging.INFO)
# Resets
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
