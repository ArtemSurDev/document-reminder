from typing import Optional


def add_user(users: list[dict], name: str, email: str) -> dict:
    user_id = len(users) + 1
    user = {"id": user_id, "name": name, "email": email}
    users.append(user)
    return user


def find_user(users: list[dict], name: str) -> Optional[dict]:
    for user in users:
        if name.lower() in user["name"].lower():
            return user
    return None
