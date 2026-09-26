from typing import Optional


class User:

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.email})"

    @classmethod
    def from_data(cls, data: dict) -> "User":
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }


def add_user(users: list[User], name: str, email: str) -> User:
    user_id = len(users) + 1
    user = User(user_id, name, email)
    users.append(user)
    return user


def find_user(users: list[User], query: str) -> Optional[User]:
    for user in users:
        if query.lower() in user.name.lower():
            return user
    return None


def find_user_by_id(users: list[User], user_id: int) -> Optional[User]:
    for user in users:
        if user.id == user_id:
            return user
    return None


def show_users(users: list[User]) -> None:
    if not users:
        print("Список пользователей пуст.")
        return
    for user in users:
        print(user)
