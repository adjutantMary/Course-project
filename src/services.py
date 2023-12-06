import json
import re
from typing import Any


def get_search(transactions: list[dict], searching: str) -> Any:
    """
    Пользователь передает строку для поиска,
    возвращается json-ответ со всеми транзакциями,
    содержащими запрос в описании или категории.
    :param transactions: list[dict] список транзакций
    :param searching:str строка, по которой будет реализовываться поиск
    :return:
    """
    user_operations = []
    for transaction in transactions:
        if re.search(searching, transaction["Описание"]):
            user_data = {
                "date": transaction["Дата операции"],
                "amount": transaction["Сумма операции"],
                "description": transaction["Описание"],
            }

            user_operations.append(user_data)

    return json.dumps(user_operations, ensure_ascii=False, indent=2)
