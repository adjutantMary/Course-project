from unittest.mock import patch

import requests

from src.check_api import get_currency, get_stocks


def get_api(stock, api):
    response = requests.get(f"https://finnhub.io/api/v1/quote?symbol={stock}&token={api}")
    return response.json()


@patch("requests.get")
def test_get_stocks(mock_get):
    mock_get.return_value.json.return_value = {"c": 127.88}
    assert get_stocks(["AAPL"]) == [{"stock": "AAPL", "price": 127.88}]


@patch("requests.get")
def test_get_currency(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"USD": 0.01}}
    assert get_currency(["USD"]) == [{"currency": "USD", "rate": 100}]
