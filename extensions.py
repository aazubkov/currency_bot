import requests
import json
from config import *


class BotError(Exception):
    pass


class Convertor:
    @staticmethod
    def convert_currency(cur_from, cur_to, amount):
        try:
            from_key = currencies[cur_from.lower()]
        except KeyError:
            raise BotError(f"Валюта {cur_from} не найдена!")

        try:
            to_key = currencies[cur_to.lower()]
        except KeyError:
            raise BotError(f"Валюта {cur_to} не найдена!")

        if from_key == to_key:
            raise BotError(f'Невозможно перевести одинаковые валюты {cur_from}!')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise BotError(f'Не удалось обработать количество {amount}!')

        url = f'https://api.exchangerate.host/latest?base={from_key }&symbols={to_key}&places={10}'
        r = requests.get(url)
        resp = json.loads(r.content)
        round_value = round(float(resp['rates'][to_key]) * amount, 2)
        return f"Стоимость {amount} {from_key} по текущему курсу составляет <b>{round_value} {to_key}</b>."

