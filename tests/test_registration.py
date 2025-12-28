import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists is True, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user is True, "Пользователь должен быть добавлен в базу данных."

# Возможные варианты тестов:
def test_add_existing_user(setup_database):
    """Добавление пользователя с уже существующим логином."""
    add_user('testuser', 'testuser2@example.com', 'newpass')
    # Попытка добавить с тем же логином
    result = add_user('testuser', 'anotheremail@example.com', 'anotherpass')
    assert result is False, "Добавление пользователя с существующим логином должно возвращать False."

def test_authenticate_user_success(setup_database):
    """Успешная аутентификация."""
    add_user('authuser', 'authuser@example.com', 'securepass')
    assert authenticate_user('authuser', 'securepass') is True, "Должна пройти успешная аутентификация."

def test_authenticate_user_notsuccess(setup_database)
    """Аутентификация несуществующего пользователя"""
    add_user('authuser', 'authuser@example.com', 'securepass')
    assert authenticate_user('authpeople', 'securepass') is False, "Аутентификация несуществующего пользователя должна вернуть False."

def test_authenticate_user_wrong_password(setup_database):
    """Аутентификация с неправильным паролем."""
    add_user('authfail', 'authfail@example.com', 'correctpass')
    assert authenticate_user('authfail', 'wrongpass') is False, "Аутентификация с неправильным паролем должна вернуть False."

def test_
"""
Тест добавления пользователя с существующим логином.+
Тест успешной аутентификации пользователя.+
Тест аутентификации несуществующего пользователя.+
Тест аутентификации пользователя с неправильным паролем.+
Тест отображения списка пользователей.
"""