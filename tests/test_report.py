import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def data_frame():
    operations = [
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
    df = pd.DataFrame(operations)
    return df


def test_spending_by_category(data_frame):
    new_df = pd.DataFrame(data_frame)
    result = spending_by_category(new_df, "Category 3").to_dict(orient="records")
    assert [x["Категория"] for x in result] == ["Category 3"]
