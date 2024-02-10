import telebot
from telebot import types
from pycbrf.toolbox import ExchangeRates

TOKEN = '6640592682:AAGZqCIfKmQ3sFuLGaVy2hA_ecM4V8R1w14'
bot = telebot.TeleBot(TOKEN)


def get_currency_rate(currency_code):
    rates = ExchangeRates()
    try:
        rate = rates[currency_code]
        return rate.rate
    except KeyError:
        return None


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    usd_button = types.KeyboardButton('Курс доллара')
    cny_button = types.KeyboardButton('Курс юаня')
    markup.add(usd_button, cny_button)

    bot.reply_to(message, "Привет! Я конвертирую валюты специально для кейса от ТМК. А пока я считаю, можешь выпить вечерний кофий. 😉", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text == 'Курс доллара':
        usd_rate = get_currency_rate('USD')
        if usd_rate is not None:
            bot.reply_to(message, f"Курс доллара (USD): {usd_rate}")
        else:
            bot.reply_to(message, "Не удалось получить курс доллара.")
    elif message.text == 'Курс юаня':
        cny_rate = get_currency_rate('CNY')
        if cny_rate is not None:
            bot.reply_to(message, f"Курс юаня (CNY): {cny_rate}")
        else:
            bot.reply_to(message, "Не удалось получить курс юаня.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
