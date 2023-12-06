import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

PATH_TO_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "report.xlsx")


def report(filename: str = PATH_TO_FILE) -> Callable:
    """
    Записывает в файл результат, который возвращает функция, формирующая отчет
    """

    def wrapper(function: Callable) -> Callable:
        @wraps(function)
        def inner(*args: Optional[Any], **kwargs: Optional[Any]) -> Optional[Any]:
            result = function(*args, **kwargs)
            if not result.empty:
                if filename.endswith(".xlsx"):
                    result.to_excel(filename, index=False)
                else:
                    raise ValueError("Файл некорректно назван")
            else:
                raise ValueError("Данные введены некорректно")

            return result

        return inner

    return wrapper


@report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние 3 месяца (от переданной даты).
    :param transactions: DataFrame с транзакциями
    :param category: str с выбранной категорией
    :param date: опциональная дата
    :return: DataFrame с тратами по заданной категории
    """
    if not date:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y")
    start_date = end_date - timedelta(days=90)

    transactions_by_data = transactions[
        (pd.to_datetime(transactions["Дата операции"], dayfirst=True) <= end_date)
        & (pd.to_datetime(transactions["Дата операции"], dayfirst=True) >= start_date)
    ]
    transactions_by_category = transactions_by_data[
        (transactions_by_data["Категория"] == category) & (transactions_by_data["Сумма операции"] < 0)
    ]

    return transactions_by_category
