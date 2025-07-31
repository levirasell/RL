import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3
from utils import fetch_all_data

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("Привет! Напиши /latest, чтобы увидеть лучшие предложения.")

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = fetch_all_data()
    msg = "📊 *Актуальные инвестиционные предложения:*\n\n"
    for block in data:
        msg += f"*{block['title']}*\n"
        for item in block['items']:
            msg += f"– {item['name']} ({item['rate']}) [Подробнее]({item['url']})\n"
        msg += "\n"
    await update.message.reply_text(msg, parse_mode="Markdown", disable_web_page_preview=True)

def main():
    app = ApplicationBuilder().token("PASTE_YOUR_BOT_TOKEN_HERE").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("latest", latest))
    app.run_polling()

if name == "main":
    main()