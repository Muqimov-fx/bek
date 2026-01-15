import os
from dotenv import load_dotenv
from dataclasses import dataclass, field

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: list[int] = field(default_factory=lambda: [int(id.strip()) for id in os.getenv("ADMIN_ID", "0").split(",")])
    DB_NAME: str = "bot_database.db"

config = Config()
