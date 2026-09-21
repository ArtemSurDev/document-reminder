from users import add_user, find_user


def test_add_user():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    assert len(users) == 1
    assert users[0]["name"] == "Иван Петров"
    assert users[0]["email"] == "ivan@example.com"


def test_add_multiple_users():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    add_user(users, "Мария Сидорова", "maria@example.com")
    assert len(users) == 2
    assert users[1]["id"] == 2


def test_find_user():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    add_user(users, "Мария Сидорова", "maria@example.com")
    found = find_user(users, "мария")
    assert found is not None
    assert found["name"] == "Мария Сидорова"


def test_find_user_case_insensitive():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    found = find_user(users, "ИВАН")
    assert found is not None


def test_find_user_not_found():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    assert find_user(users, "Пётр") is None
