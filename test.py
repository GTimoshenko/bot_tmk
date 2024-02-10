import requests
from bs4 import BeautifulSoup

url = "https://www.lme.com/Metals/Ferrous/LME-Steel-Scrap-CFR-Turkey-Platts"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.lme.com/Metals/Ferrous/LME-Steel-Scrap-CFR-Turkey-Platts",
}

try:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Найдем элемент <div> с классом "hero-metal-data"
        hero_metal_data_div = soup.find("div", class_="hero-metal-data")

        if hero_metal_data_div:
            # Выведем текстовое содержимое найденного элемента
            print(hero_metal_data_div.get_text(strip=True))
        else:
            print("Не удалось найти элемент с классом 'hero-metal-data'.")
    else:
        print(f"Ошибка при запросе страницы. Код ошибки: {response.status_code}")
except Exception as e:
    print(f"Произошла ошибка: {str(e)}")

