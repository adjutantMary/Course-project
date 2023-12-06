import logging
import os

import requests
from dotenv import load_dotenv

# Добавить логгеры к ошибкам
logger = logging.getLogger(__name__)
if os.path.exists("check_api.log"):
    os.unlink("check_api.log")

file_handler = logging.FileHandler("check_api.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

file_logger = logging.getLogger(__name__)


def get_currency(value: list) -> list[dict]:
    """
    Функция возвращает по API адресу курсы валют в соотношении к рублю, получив на вход список валют
    :param value: список валют list
    :return: list[dict] список со словарем, содержащим данные о курсе валюты
    """
    load_dotenv()
    api = os.getenv("API_ADDRESS")
    if api is None:
        file_logger.info("ValueError: API не действителен")
        raise ValueError
    try:
        url = "https://api.apilayer.com/exchangerates_data/latest?base=RUB"
        response = requests.get(url, headers={"apikey": api})
        new_response = response.json()
        values = []
        for v in value:
            rate = round(1 / new_response["rates"][v], 2)
            currency = {"currency": v, "rate": rate}
            values.append(currency)
        file_logger.info(f"Курс валют к рублю имеет следующие значения: {values}")
        return values

    except Exception:
        raise ValueError


def get_stocks(stocks: list) -> list[dict]:
    """
    Функция возвращает по API адрессу стоимости акций, получив на вход список акций
    :param stocks: list акций
    :return: list[dict] список стоимости акций
    """
    load_dotenv()
    api = os.getenv("API_STOCKS")
    if api is None:
        file_logger.info("ValueError: API не действителен")
        raise ValueError
    try:
        values = []
        for stock in stocks:
            url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={api}"
            response = requests.get(url, headers={"apikey": api})
            new_response = response.json()
            price = new_response["c"]
            stock_dict = {"stock": stock, "price": price}
            values.append(stock_dict)
        file_logger.info(f"Стоимость акций следующие: {values}")
        return values
    except Exception:
        raise ValueError
