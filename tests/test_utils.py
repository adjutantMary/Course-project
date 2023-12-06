import os.path

import pandas
import pandas as pd
import pytest

from src.utils import get_data_for_analytic, get_dict, get_operation_file


@pytest.fixture
def path_to_exel():
    current_dir = os.path.dirname(os.path.dirname(__file__))  # пути к файлу эксель
    xls_path = os.path.join(current_dir, "data", "operations_example.xls")
    return xls_path


@pytest.fixture
def data_frame():
    operations = [
        {"amount": -200, "category": "Category 2", "date": "02.11.2023", "description": "Transaction 2"},
        {"amount": -150, "category": "Category 1", "date": "03.11.2023", "description": "Transaction 3"},
        {"amount": -100, "category": "Category 1", "date": "01.11.2023", "description": "Transaction 1"},
        {"amount": -50, "category": "Category 3", "date": "04.11.2023", "description": "Transaction 4"},
    ]
    df = pd.DataFrame(operations)
    return df


@pytest.fixture
def transactions():
    return [
        {
            "Дата операции": "03.01.2018 14:55:21",
            "Номер карты": "1234567890123456",
            "Сумма операции": -100,
            "Бонусы (включая кэшбэк)": 1,
            "Категория": "Category 1",
            "Описание": "Transaction 1",
            "Статус": "OK",
        },
        {
            "Дата операции": "01.01.2018 20:27:51",
            "Номер карты": "1234567890123456",
            "Сумма операции": -200,
            "Бонусы (включая кэшбэк)": 2,
            "Категория": "Category 2",
            "Описание": "Transaction 2",
            "Статус": "OK",
        },
        {
            "Дата операции": "02.01.2018 20:27:51",
            "Номер карты": "9876543210987654",
            "Сумма операции": -150,
            "Бонусы (включая кэшбэк)": 3,
            "Категория": "Category 1",
            "Описание": "Transaction 3",
            "Статус": "OK",
        },
        {
            "Дата операции": "04.11.2018 17:27:51",
            "Номер карты": "9876543210987654",
            "Сумма операции": -50,
            "Бонусы (включая кэшбэк)": 1,
            "Категория": "Category 3",
            "Описание": "Transaction 4",
            "Статус": "OK",
        },
    ]


def test_get_operation_file(path_to_exel):
    assert type(get_operation_file(path_to_exel)) == pandas.DataFrame


def test_get_dict(data_frame):
    assert type(get_dict(data_frame)) == list


def test_data_for_analytic(transactions):
    date = "03.01.2018"
    assert (get_data_for_analytic(transactions, date)) == [
        {
            "Бонусы (включая кэшбэк)": 1,
            "Дата операции": "03.01.2018 14:55:21",
            "Категория": "Category 1",
            "Номер карты": "1234567890123456",
            "Описание": "Transaction 1",
            "Статус": "OK",
            "Сумма операции": -100,
        },
        {
            "Бонусы (включая кэшбэк)": 2,
            "Дата операции": "01.01.2018 20:27:51",
            "Категория": "Category 2",
            "Номер карты": "1234567890123456",
            "Описание": "Transaction 2",
            "Статус": "OK",
            "Сумма операции": -200,
        },
        {
            "Бонусы (включая кэшбэк)": 3,
            "Дата операции": "02.01.2018 20:27:51",
            "Категория": "Category 1",
            "Номер карты": "9876543210987654",
            "Описание": "Transaction 3",
            "Статус": "OK",
            "Сумма операции": -150,
        },
    ]
