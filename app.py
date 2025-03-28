import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN

proxy_url = "socks5://127.0.0.1:8000"

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(update.message.text)


def main():
    app = Application.builder().token(token=BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT, echo)
    app.add_handler(text_handler)
    app.run_polling()


if __name__ == "__main__":
    main()