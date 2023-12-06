import json

import pytest

from src.views import final_json, get_card, get_greetings, top_five_operations


@pytest.fixture
def user_settings():
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}


@pytest.fixture
def operations_pattern():
    return [
        {
            "Дата операции": "01.11.2023",
            "Номер карты": "1234567890123456",
            "Сумма операции": -100,
            "Бонусы (включая кэшбэк)": 1,
            "Категория": "Category 1",
            "Описание": "Transaction 1",
        },
        {
            "Дата операции": "02.11.2023",
            "Номер карты": "1234567890123456",
            "Сумма операции": -200,
            "Бонусы (включая кэшбэк)": 2,
            "Категория": "Category 2",
            "Описание": "Transaction 2",
        },
        {
            "Дата операции": "03.11.2023",
            "Номер карты": "9876543210987654",
            "Сумма операции": -150,
            "Бонусы (включая кэшбэк)": 3,
            "Категория": "Category 1",
            "Описание": "Transaction 3",
        },
        {
            "Дата операции": "04.11.2023",
            "Номер карты": "9876543210987654",
            "Сумма операции": -50,
            "Бонусы (включая кэшбэк)": 1,
            "Категория": "Category 3",
            "Описание": "Transaction 4",
        },
    ]


def test_get_greetings():
    assert get_greetings() in [
        "Доброе утро",
        "Добрый день",
        "Добрый вечер",
        "Доброй ночи",
    ]


def test_get_card(operations_pattern):
    assert type(get_card(operations_pattern)) == list


def test_top_five(operations_pattern):
    assert top_five_operations(operations_pattern) == [
        {"amount": -200, "category": "Category 2", "date": "02.11.2023", "description": "Transaction 2"},
        {"amount": -150, "category": "Category 1", "date": "03.11.2023", "description": "Transaction 3"},
        {"amount": -100, "category": "Category 1", "date": "01.11.2023", "description": "Transaction 1"},
        {"amount": -50, "category": "Category 3", "date": "04.11.2023", "description": "Transaction 4"},
    ]


def test_final_json(operations_pattern, user_settings):
    result = final_json(operations_pattern, user_settings)
    json_file = json.dumps(result, ensure_ascii=False, indent=2)
    assert "greeting" in json_file
    assert "cards" in json_file
    assert "top_transactions" in json_file
    assert "currency_rates" in json_file
    assert "stock_prices" in json_file
