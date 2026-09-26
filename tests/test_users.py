from models import User
from models.users import add_user, find_user, find_user_by_id


def test_user_creation():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_user_str():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert "Иван Петров" in str(user)
    assert "ivan@example.com" in str(user)


def test_user_from_data():
    data = {"id": 5, "name": "Мария", "email": "maria@example.com"}
    user = User.from_data(data)
    assert user.id == 5
    assert user.name == "Мария"


def test_user_to_dict():
    user = User(1, "Иван", "ivan@example.com")
    assert user.to_dict() == {
        "id": 1,
        "name": "Иван",
        "email": "ivan@example.com",
    }


def test_add_user():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    assert len(users) == 1
    assert isinstance(users[0], User)


def test_find_user():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    add_user(users, "Мария Сидорова", "maria@example.com")
    found = find_user(users, "мария")
    assert found is not None
    assert found.name == "Мария Сидорова"


def test_find_user_by_id():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    found = find_user_by_id(users, 1)
    assert found is not None
    assert found.name == "Иван Петров"


def test_find_user_by_id_not_found():
    users = []
    add_user(users, "Иван Петров", "ivan@example.com")
    assert find_user_by_id(users, 99) is None
