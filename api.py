import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
import aiohttp
from config import BOT_TOKEN

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def get_ll_spn(toponym):
    toponym_coodrinates = toponym["Point"]["pos"]

    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    ll = ",".join([toponym_longitude, toponym_lattitude])

    envelope = toponym["boundedBy"]["Envelope"]

    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")

    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0

    span = f"{dx},{dy}"

    return ll, span


async def geocoder(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = await get_response(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": update.message.text
    })

    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    ll, spn = get_ll_spn(toponym)

    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map"
    await context.bot.send_photo(
        update.message.chat_id,
        static_api_request,
        caption="Нашёл:"
    )


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()

def main():
    app = Application.builder().token(token=BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, geocoder)
    app.add_handler(text_handler)
    app.run_polling()


if __name__ == "__main__":
    main()