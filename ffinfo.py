import logging
import requests
import datetime  
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot Token
TOKEN = "7667715767:AAH7rLq-Yb0__jaNjPFg2R3pnUB94DjBavQ"

# Allowed Group ID (Replace this with your actual group ID)
GROUP_ID = -1002641047546  # Replace with your group ID

# Free Fire API URL
FF_API_URL = "https://wlx-demon-info.vercel.app/profile_info?uid={}&region=ind&key=FFwlx"

def format_time(timestamp):
    """Convert Unix timestamp to human-readable format."""
    try:
        if not timestamp or timestamp == "N/A":
            return "N/A"
        timestamp = int(timestamp)  
        dt = datetime.datetime.fromtimestamp(timestamp)  
        return dt.strftime("%d %b %Y, %I:%M %p")  
    except:
        return "Invalid Date"

async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command with group authentication."""
    if update.message.chat_id != GROUP_ID:
        await update.message.reply_text("❌ You are not authorized to use this bot! Telegram Channel : https://t.me/+cideLIy_zUkxMDU1")
        return

    await update.message.reply_text(
        "🔥 Welcome to Free Fire Info Bot!\n"
        "Use /get <UID> to get player stats.", 
        parse_mode="Markdown"
    )

async def get(update: Update, context: CallbackContext) -> None:
    """Handles the /get command with group authentication."""
    if update.message.chat_id != GROUP_ID:
        await update.message.reply_text("❌ You are not authorized to use this bot!")
        return

    if len(context.args) == 0:
        await update.message.reply_text(
            "⚠️ Please provide a Free Fire UID. Example: /get 123456789",
            parse_mode="Markdown"
        )
        return

    uid = context.args[0]
    try:
        response = requests.get(FF_API_URL.format(uid), timeout=10)  
        data = response.json()

        if data.get("error"):
            await update.message.reply_text("❌ Invalid UID or Player Not Found!")
            return

        account_info = data.get("AccountInfo", {})
        account_creation = format_time(account_info.get("AccountCreateTime", "N/A"))
        last_login = format_time(account_info.get("AccountLastLogin", "N/A"))

        stats = (
            f"🎮 *Free Fire Player Stats* 🎮\n"
            f"👤 *Player Name:* {account_info.get('AccountName', 'N/A')}\n"
            f"🔥 *Level:* {account_info.get('AccountLevel', 'N/A')}\n"
            f"🏆 *BR Max Rank:* {account_info.get('BrMaxRank', 'N/A')}\n"
            f"⚡ *CS Max Rank:* {account_info.get('CsMaxRank', 'N/A')}\n"
            f"💀 *Total Likes:* {account_info.get('AccountLikes', 'N/A')}\n"
            f"🔄 *Last Login:* {last_login}\n"
            f"🌍 *Region:* {account_info.get('AccountRegion', 'N/A')}\n"
            f"🕰️ *Account Created On:* {account_creation}\n"
            f"\n🔗 *Subscribe Our Youtube Channel And Play FF Tournaments:*\n"
            f"🔹 *Khelo Jito:* [Telegram Channel](https://t.me/+olIpVWpClaxhMzE1)\n"
            f"🔹 *Khelo Jito Youtube:* [Youtube](http://www.youtube.com/@Khelojito_)\n"
            f"🔹 *Owner Instagram:* [Instagram](https://www.instagram.com/developerkrn?igsh=MXZqZWd5amV1b2djbA==)\n"
        )

        await update.message.reply_text(stats, parse_mode="Markdown")

    except requests.exceptions.Timeout:
        await update.message.reply_text("⏳ Request timed out! Please try again later.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching stats: {e}")
        await update.message.reply_text("❌ Failed to fetch player stats. Try again later!")

def main():
    """Main function to run the bot."""
    app = Application.builder().token(TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get", get))

    # Start polling
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
