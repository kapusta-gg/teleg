import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


async def echo(update, context):
    await update.message.reply_text(update.message.text)


def main():
    app = Application.builder().token(token=BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT, echo)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(text_handler)
    app.run_polling()


if __name__ == "__main__":
    main()