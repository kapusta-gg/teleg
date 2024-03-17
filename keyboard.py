import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import BOT_TOKEN

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

reply_keyboard = [['/address', '/phone'],
                  ['/site', '/work_time']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
        reply_markup=markup
    )


async def echo(update, context):
    await update.message.reply_text(update.message.text)


async def help(update, context):
    await update.message.reply_text(
        "Я бот справочник.")


async def address(update, context):
    await update.message.reply_text(
        "Адрес: г. Москва, ул. Льва Толстого, 16")


async def phone(update, context):
    await update.message.reply_text("Телефон: +7(495)776-3030")


async def site(update, context):
    await update.message.reply_text(
        "Сайт: http://www.yandex.ru/company")


async def work_time(update, context):
    await update.message.reply_text(
        "Время работы: круглосуточно.")


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )

def main():
    app = Application.builder().token(token=BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT, echo)
    app.add_handler(CommandHandler("address", address))
    app.add_handler(CommandHandler("phone", phone))
    app.add_handler(CommandHandler("site", site))
    app.add_handler(CommandHandler("work_time", work_time))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("close", close_keyboard))

    app.add_handler(text_handler)
    app.run_polling()




if __name__ == "__main__":
    main()