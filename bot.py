from bot_tmk import consts
from bot_tmk.parser import Parser
import telebot
from telebot import types


class Bot:
    def __init__(self):
        self.parser = Parser()
        self.bot = telebot.TeleBot(consts.TOKEN)

    def start(self, none_stop):
        self.bot.polling(none_stop=none_stop)

    def initialize_bot(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(self, message):
            markup = types.ReplyKeyboardMarkup(row_width=2)
            usd_button = types.KeyboardButton('Курс доллара')
            cny_button = types.KeyboardButton('Курс юаня')
            iron_button = types.KeyboardButton('Курс чугуна')
            steel_button = types.KeyboardButton('Курс стали')
            home_button = types.KeyboardButton('В начало')
            about_button = types.KeyboardButton('О боте')
            markup.add(about_button, home_button, usd_button, cny_button, iron_button, steel_button)

            self.bot.reply_to(message,
                         "Привет! Я конвертирую валюты специально для кейса от ТМК. А пока я считаю, можешь выпить вечерний кофий. 😉",
                         reply_markup=markup)

        def about(message):
            self.bot.reply_to(message,
                         "Немного обо мне: \n- Я конвертирую валюты для компании ТМК. \n- Я очень люблю свою работу \n- Курс Юаня и Доллара США выдается по отношеию к Рублю\n- Единицы котировок стали и чугуна соответствуют выдаваемым в сообщениях.")

        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(self, message):
            match message:
                case 'Курс доллара':
                    usd_rate = self.parser.get_currency_rate('USD')
                    if usd_rate is not None:
                        self.bot.reply_to(message, f"Курс доллара (USD): {usd_rate}")
                    else:
                        self.bot.reply_to(message, "Не удалось получить курс доллара.")

                case 'Курс юаня':
                    cny_rate = self.parser.get_currency_rate('CNY')
                    if cny_rate is not None:
                        self.bot.reply_to(message, f"Курс юаня (CNY): {cny_rate}")
                    else:
                        self.bot.reply_to(message, "Не удалось получить курс юаня.")

                case 'Курс чугуна':
                    iron_rate = self.parser.get_commodity_prices("Iron Ore")
                    if iron_rate is not None:
                        self.bot.reply_to(message, f"Курс чугуна (Iron Ore): {iron_rate} Долларов США за метрическую тонну")
                    else:
                        self.bot.reply_to(message, "Не удалось получить курс чугуна.")

                case 'Курс стали':
                    steel_rate = self.parser.get_commodity_prices("Steel")
                    if steel_rate is not None:
                        self.bot.reply_to(message, f"Курс стали (Steel): {steel_rate} Юаней за тонну")
                    else:
                        self.bot.reply_to(message, "Не удалось получить курс стали.")

                case 'В начало':
                    send_welcome(message)
                case 'О боте':
                    about(message)

        @self.bot.message_handler(commands=['about'])
        def about_command(message):
            about_text = "Этот бот предоставляет информацию о котировках чермета. "
            about_text += "Если у вас есть вопросы или предложения, свяжитесь с нами."
            self.bot.reply_to(message, about_text)