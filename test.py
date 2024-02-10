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

# Пример использования в твоем боте
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text == 'Steel':
        steel_rate = get_commodity_prices("Steel")
        if steel_rate is not None:
            bot.reply_to(message, f"Курс стали (Steel): {steel_rate}")
        else:
            bot.reply_to(message, "Не удалось получить курс стали.")
