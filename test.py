import requests
from bs4 import BeautifulSoup

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
                # Извлекаем информацию о котировках Steel
                if "Steel" in cells[0].text:
                    steel_price = cells[1].text.strip()
                    print("Котировки Стали:", steel_price)

                # Извлекаем информацию о котировках Iron Ore
                if "Iron Ore" in cells[0].text:
                    iron_ore_price = cells[1].text.strip()
                    print("Котировки Чугуна:", iron_ore_price)
else:
    print("Ошибка при запросе страницы. Код ошибки:", response.status_code)
