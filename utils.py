from datetime import date, datetime


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_date(prompt: str) -> date:
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ.")


def input_str(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: строка не может быть пустой.")