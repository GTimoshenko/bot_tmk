import requests
from bs4 import BeautifulSoup
from pycbrf.toolbox import ExchangeRates
from bot_tmk import consts


class Parser:
    def __init__(self):
        self.url = consts.PRICE_URL
        self.headers = consts.PARSER_HEADERS

    def get_commodity_prices(self, commodity_name):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find("table", class_="table-heatmap")

            if table:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) > 1:
                        if commodity_name.lower() in cells[0].text.lower():
                            commodity_price = cells[1].text.strip()
                            return commodity_price

                return None

            else:
                return None

        else:
            return None

    def get_currency_rate(self, currency_code):
        rates = ExchangeRates()
        try:
            rate = rates[currency_code]
            return rate.rate
        except KeyError:
            return None