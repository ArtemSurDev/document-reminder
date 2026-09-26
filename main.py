from datetime import date

from models import User, Document, Notification
from models.users import add_user, find_user_by_id, show_users
from models.documents import (
    add_document, find_documents, get_expiring_documents,
    sort_documents_by_expiry, get_statistics, show_documents,
)
from models.notifications import (
    create_notification, add_notification, show_notifications,
)
from storage import (
    load_users, save_users,
    load_documents, save_documents,
    load_notifications, save_notifications,
)
from utils import input_int, input_date, input_str


def show_expiring(documents: list[Document]) -> None:
    expiring = get_expiring_documents(documents, threshold=30)
    if not expiring:
        print("Нет документов с ближайшими сроками.")
        return
    today = date.today()
    for doc in expiring:
        print(f"  {doc.title}: осталось {doc.days_until_expiry(today)} дн.")


def show_statistics(documents: list[Document]) -> None:
    stats = get_statistics(documents)
    print(f"Всего: {stats['total']}")
    print(f"Просрочено: {stats['expired']}")
    print(f"Истекает скоро: {stats['expiring']}")
    print(f"Действительно: {stats['valid']}")


def create_new_user(users: list[User]) -> None:
    name = input_str("Имя пользователя: ")
    email = input_str("Email: ")
    add_user(users, name, email)
    save_users(users)
    print("Пользователь добавлен.")


def create_new_document(documents: list[Document],
                        users: list[User]) -> None:
    if not users:
        print("Сначала добавьте хотя бы одного пользователя.")
        return
    show_users(users)
    owner_id = input_int("ID владельца: ")
    owner = find_user_by_id(users, owner_id)
    if owner is None:
        print("Пользователь с таким ID не найден.")
        return
    title = input_str("Название документа: ")
    number = input_str("Номер документа: ")
    expiry = input_date("Дата окончания (ДД.ММ.ГГГГ): ")
    add_document(documents, title, number, expiry, owner)
    save_documents(documents)
    print("Документ добавлен.")


def create_notifications_for_expiring(
        documents: list[Document],
        notifications: list[Notification]) -> None:
    expiring = get_expiring_documents(documents, threshold=30)
    if not expiring:
        print("Нет документов с ближайшими сроками.")
        return
    today = date.today()
    for doc in expiring:
        days_left = doc.days_until_expiry(today)
        message = doc.format_notification(days_left)
        note = create_notification(doc.owner, doc, message)
        add_notification(notifications, note)
        print(message)
    save_notifications(notifications)


def menu() -> None:
    users = load_users()
    documents = load_documents(users=users)
    notifications = load_notifications(users=users, documents=documents)

    while True:
        print("\n=== Сервис напоминаний о сроках документов ===")
        print("1. Показать все документы")
        print("2. Добавить документ")
        print("3. Найти документ по названию")
        print("4. Показать ближайшие сроки")
        print("5. Показать статистику")
        print("6. Показать уведомления")
        print("7. Добавить пользователя")
        print("8. Показать пользователей")
        print("0. Выход")
        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_documents(sort_documents_by_expiry(documents))
        elif choice == 2:
            create_new_document(documents, users)
        elif choice == 3:
            query = input_str("Поиск: ")
            found = find_documents(documents, query)
            show_documents(found)
        elif choice == 4:
            show_expiring(documents)
        elif choice == 5:
            show_statistics(documents)
        elif choice == 6:
            create_notifications_for_expiring(documents, notifications)
            show_notifications(notifications)
        elif choice == 7:
            create_new_user(users)
        elif choice == 8:
            show_users(users)
        elif choice == 0:
            save_users(users)
            save_documents(documents)
            save_notifications(notifications)
            print("До свидания.")
            break
        else:
            print("Нет такого пункта.")


def main() -> None:
    menu()


if __name__ == "__main__":
    main()
