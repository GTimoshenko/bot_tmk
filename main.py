import telebot
from telebot import types
from bs4 import BeautifulSoup
from pycbrf.toolbox import ExchangeRates

TOKEN = '6640592682:AAGZqCIfKmQ3sFuLGaVy2hA_ecM4V8R1w14'
bot = telebot.TeleBot(TOKEN)

import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup


def get_commodity_prices(commodity_name):
    url = "https://tradingeconomics.com/commodity/iron-ore"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find("table", class_="table-heatmap")

        if table:
            rows = table.find_all("tr")

            for row in rows:
                cells = row.find_all("td")

                # Если есть ячейки и их достаточно для обработки
                if len(cells) > 1:
                    # Извлекаем информацию о котировках для заданного товара
                    if commodity_name.lower() in cells[0].text.lower():
                        commodity_price = cells[1].text.strip()
                        return commodity_price

            # Если товар не найден
            return None
        else:
            return None
    else:
        return None


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
    iron_button = types.KeyboardButton('Курс чугуна')
    steel_button= types.KeyboardButton('Курс стали')
    markup.add(usd_button, cny_button, iron_button, steel_button)

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
    elif message.text == 'Курс чугуна':
        iron_rate = get_commodity_prices("Iron Ore")
        if iron_rate is not None:
            bot.reply_to(message, f"Курс чугуна (Iron Ore): {iron_rate}")
        else:
            bot.reply_to(message, "Не удалось получить курс чугуна.")
    elif message.text == 'Курс стали':
        steel_rate = get_commodity_prices("Steel")
        if steel_rate is not None:
            bot.reply_to(message, f"Курс стали (Iron Ore): {steel_rate}")
        else:
            bot.reply_to(message, "Не удалось получить курс стали.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
