from datetime import date

user_name = "Иван Петров"
document_title = "Паспорт РФ"
expiry_date = date(2026, 5, 20)
current_date = date(2026, 4, 25)
days_before_notify = 30


def days_until_expiry(expiry, current):
    return (expiry - current).days


def get_status(days_left):
    if days_left < 0:
        return "ПРОСРОЧЕН"
    elif days_left == 0:
        return "ИСТЕКАЕТ СЕГОДНЯ"
    elif days_left <= 30:
        return "ИСТЕКАЕТ СКОРО"
    else:
        return "ДЕЙСТВИТЕЛЕН"


def format_notification(user, title, days_left):
    if days_left < 0:
        return f"{user}, документ «{title}» просрочен на {abs(days_left)} дн."
    return f"{user}, до окончания «{title}» осталось {days_left} дн."


days_left = days_until_expiry(expiry_date, current_date)
status = get_status(days_left)

print(f"Пользователь: {user_name}")
print(f"Документ:     {document_title}")
print(f"До окончания: {days_left} дн.")
print(f"Статус:       {status}")

if days_left <= days_before_notify:
    print(format_notification(user_name, document_title, days_left))
else:
    print("Напоминание не требуется.")