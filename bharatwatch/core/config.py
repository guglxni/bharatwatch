from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

BRIGHT_DATA_API_TOKEN = os.getenv("BRIGHT_DATA_API_TOKEN", "")
BRIGHT_DATA_COLLECTOR_BASE_URL = os.getenv(
    "BRIGHT_DATA_COLLECTOR_BASE_URL",
    "https://api.brightdata.com/dca/trigger"
)
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/storage.db")
