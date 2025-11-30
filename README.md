# FasterPostMaker Telegram Bot

A Telegram bot that helps users create promotional posts with custom inline buttons for Telegram channels and groups.

## Features

- **📝 Create Posts** - Create promotional posts with text or photos
- **🔘 Normal Buttons** - Add custom URL buttons to your posts
- **🔐 Login Buttons** - Add Telegram login buttons (Premium feature)
- **User Management** - Search, ban, and unban users
- **📢 Broadcasting** - Send messages to all bot users
- **� Share251 Integration** - Extract links from @share251bot posts

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB database
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/BraveRam/FasterPostMaker.git
   cd FasterPostMaker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root with the following variables:
   ```env
   BOT_TOKEN=your_bot_token_here
   MONGODB_URI=your_mongodb_connection_string
   OWNER_ID=your_telegram_user_id
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

### Docker Support

You can also run the bot using Docker:
```bash
docker build -t fasterpostmaker .
docker run -d --env-file .env fasterpostmaker
```
