from datetime import date

from documents import (
    add_document, find_documents, get_status, format_notification,
    get_expiring_documents, sort_documents_by_expiry, get_statistics,
)
from users import add_user
from notifications import create_notification, add_notification
from storage import (
    load_documents, save_documents,
    load_users, save_users,
    load_notifications, save_notifications,
)
from utils import input_int, input_date, input_str


USER_NAME = "Иван Петров"


def show_documents(documents: list[dict]) -> None:
    if not documents:
        print("Список документов пуст.")
        return
    today = date.today()
    for doc in documents:
        expiry = date.fromisoformat(doc["expiry"])
        days_left = (expiry - today).days
        status = get_status(days_left)
        print(f"[{doc['id']}] {doc['title']} ({doc['number']}) — "
              f"до {doc['expiry']} — {status}")


def show_expiring(documents: list[dict]) -> None:
    expiring = get_expiring_documents(documents, threshold=30)
    if not expiring:
        print("Нет документов с ближайшими сроками.")
        return
    for doc in expiring:
        print(f"  {doc['title']}: осталось {doc['days_left']} дн.")


def show_statistics(documents: list[dict]) -> None:
    stats = get_statistics(documents)
    print(f"Всего: {stats['total']}")
    print(f"Просрочено: {stats['expired']}")
    print(f"Истекает скоро: {stats['expiring']}")
    print(f"Действительно: {stats['valid']}")


def menu() -> None:
    documents = load_documents()
    users = load_users()
    notifications = load_notifications()

    while True:
        print("\n=== Сервис напоминаний о сроках документов ===")
        print("1. Показать все документы")
        print("2. Добавить документ")
        print("3. Найти документ по названию")
        print("4. Показать ближайшие сроки")
        print("5. Показать статистику")
        print("6. Показать напоминания")
        print("7. Добавить пользователя")
        print("0. Выход")
        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_documents(sort_documents_by_expiry(documents))
        elif choice == 2:
            title = input_str("Название документа: ")
            number = input_str("Номер документа: ")
            expiry = input_date("Дата окончания (ДД.ММ.ГГГГ): ")
            add_document(documents, title, number, expiry)
            save_documents(documents)
            print("Документ добавлен.")
        elif choice == 3:
            query = input_str("Поиск: ")
            found = find_documents(documents, query)
            show_documents(found)
        elif choice == 4:
            show_expiring(documents)
        elif choice == 5:
            show_statistics(documents)
        elif choice == 6:
            for doc in get_expiring_documents(documents, threshold=30):
                message = format_notification(USER_NAME, doc["title"],
                                              doc["days_left"])
                print(message)
                note = create_notification(1, doc["id"], message)
                add_notification(notifications, note)
            save_notifications(notifications)
        elif choice == 7:
            name = input_str("Имя пользователя: ")
            email = input_str("Email: ")
            add_user(users, name, email)
            save_users(users)
            print("Пользователь добавлен.")
        elif choice == 0:
            save_documents(documents)
            save_users(users)
            save_notifications(notifications)
            print("До свидания.")
            break
        else:
            print("Нет такого пункта.")


if __name__ == "__main__":
    menu()
