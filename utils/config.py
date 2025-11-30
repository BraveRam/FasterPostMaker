import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Database Configuration
DB_NAME = "FastPostMakerBot"
COLLECTION_NAME = "promo"

# Bot Configuration
SHARE251_BOT = "@share251bot"
