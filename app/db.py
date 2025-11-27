import sqlite3
from pathlib import Path

DATA_DIR = Path("DATA")
DATA_PATH = DATA_DIR / "intelligence_platform.db"

conn = sqlite3.connect(DATA_PATH)  

