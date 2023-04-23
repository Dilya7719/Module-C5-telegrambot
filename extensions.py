from config import API_KEY, currency_dict
import requests
import json

class APIException(Exception):
    pass

class ParsingPrice:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        '''принимает три аргумента и возвращает нужную сумму в валюте:
        - имя валюты, цену на которую надо узнать, — base;
        - имя валюты, цену в которой надо узнать, — quote;
        - количество переводимой валюты — amount.'''
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Нет возможности обработать количество {amount}')

        if base not in currency_dict.keys():
            raise APIException(f'Нет возможности обработать валюту {base}'
                               f'\n список доступных валют: /values')

        if quote not in currency_dict.keys():
            raise APIException(f'Нет возможности обработать валюту {quote}'
                               f'\n список доступных валют: /values')

        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты')

        base_kode = currency_dict[base]['kode']
        quote_kode = currency_dict[quote]['kode']
        r = requests.get(f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{base_kode}/{quote_kode}')

        return round(json.loads(r.content)['conversion_rate'] * amount, 2)
