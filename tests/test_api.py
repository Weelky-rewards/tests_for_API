import pytest
import requests

from helpers import login_account, create_profile


#тест на регистрацию с не существующим пользователем
def test_login_unexist():
    body = {"username": "Unexist_profile_937",
            "password": "qwerty"
    }
    response = requests.post("https://secby.ru/api/auth/login",json=body)
    assert response.status_code == 401

#тест на регистрацию с существующим пользователем
def test_login_exist(create_delete_user):
    new_user_name = "test_user_777"
    new_email = "test_user_777@mail.ru"
    new_password = "qwerty123"

    create_delete_user(new_user_name, new_email, new_password)

    body = {"username": "test_user_777",
            "password": "qwerty123"
            }

    response = requests.post("https://secby.ru/api/auth/login", json=body)
    assert response.status_code == 200

#тест на регистрацию с неправильным паролем
def test_login_with_invalid_password(create_delete_user):
    new_user_name = "test_user_777"
    new_email = "test_user_777@mail.ru"
    new_password = "qwerty123"

    create_delete_user(new_user_name, new_email, new_password)

    body = {"username": "test_user_777",
            "password": "qwerty123!"
            }

    response = requests.post("https://secby.ru/api/auth/login", json=body)
    assert response.status_code == 401

#тест на получение токена
def test_take_token(create_delete_user):
    new_user_name = "test_user_777"
    new_email = "test_user_777@mail.ru"
    new_password = "qwerty123"

    create_delete_user(new_user_name, new_email, new_password)
    response = login_account(new_user_name,new_password).json()

    assert response["access_token"] is not None
    assert response["token_type"] == "bearer"

#тест на корректное подтверждение правильного токена
def test_verify_token(create_delete_user):
    new_user_name = "test_user_777"
    new_email = "test_user_777@mail.ru"
    new_password = "qwerty123"

    create_delete_user(new_user_name, new_email, new_password)
    response = login_account(new_user_name,new_password).json()

    token = response["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post("https://secby.ru/api/auth/verify", headers=headers)

    assert response.status_code == 200

#тест на отказ в доступе с неправильным токеном
def test_verify_invalid_token(create_delete_user):
    new_user_name = "test_user_777"
    new_email = "test_user_777@mail.ru"
    new_password = "qwerty123"

    create_delete_user(new_user_name, new_email, new_password)
    response = login_account(new_user_name,new_password).json()

    token = response["access_token"]
    test_token = "invalid_token"
    if token != test_token:
        headers = {
            "Authorization": f"Bearer {test_token}",
            "Content-Type": "application/json"
        }
        response = requests.post("https://secby.ru/api/auth/verify", headers=headers)

        assert response.status_code == 401
    else:
        pytest.fail("Тестовый токен должен отличаться от оригинального")

#тест на успешное создание профиля
def test_create_new_profile(create_delete_user):
    new_user_name = "test_user_777"
    new_email = "test_user_777@mail.ru"
    new_password = "qwerty123"

    create_delete_user(new_user_name, new_email, new_password)
    response = create_profile(new_user_name,new_email,new_password)

    assert response.status_code == 200

#тест на проверку получаения информации о профиле пользователя
def test_get_profile_me(create_delete_user):
    new_user_name = "test_user_777"
    new_email = "test_user_777@mail.ru"
    new_password = "qwerty123"

    create_delete_user(new_user_name, new_email, new_password)
    response = login_account(new_user_name, new_password).json()

    token = response["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"https://secby.ru/api/profiles/me", headers=headers)

    assert response.status_code == 200
    assert response.json()['profile']['username'] == new_user_name
    assert response.json().get('profile') and 'profiles' not in response.json()

#тест на то что обычный пользователь получает только свой профиль
def test_get_profile(create_delete_profile):
    new_user_name = "test_user_777"
    new_email = "test_user_777@mail.ru"
    new_password = "qwerty123"

    create_delete_profile(new_user_name, new_email, new_password)
    create_delete_profile(new_user_name+"1", "1" + new_email, new_password)
    create_delete_profile(new_user_name + "2", "2" + new_email, new_password)
    response = login_account(new_user_name, new_password).json()

    token = response["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"https://secby.ru/api/profiles/", headers=headers)

    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['profiles'][0]['username'] == new_user_name

#тест на то что обычный пользователь не может получить информацию об администраторе
def test_regular_user_cannot_get_admin_profile(create_delete_profile):
    user_name = "test_user_777"
    user_email = "test_user_777@mail.ru"
    user_password = "qwerty123"

    create_delete_profile(user_name, user_email, user_password)

    response = login_account(user_name, user_password).json()
    token = response["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"https://secby.ru/api/profiles/1", headers=headers)

    assert response.status_code == 403

#тест на то что администратор может видеть все профили
def test_admin_get_profiles(create_delete_profile):
    new_user_name = "test_user_777"
    new_email = "test_user_777@mail.ru"
    new_password = "qwerty123"

    create_delete_profile(new_user_name, new_email, new_password)
    create_delete_profile(new_user_name + "1", "1" + new_email, new_password)
    create_delete_profile(new_user_name + "2", "2" + new_email, new_password)
    response = login_account("admin", "admin123").json()

    token = response["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"https://secby.ru/api/profiles/", headers=headers)

    assert response.status_code == 200
    assert response.json()['count'] >= 3

#тест на получения администратором собственного профиля
def test_admin_get_own_profile():
    response = login_account("admin", "admin123")

    token = response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"https://secby.ru/api/profiles/me", headers=headers)

    assert response.status_code == 200
    assert response.json()['profile']['role']['name'] == 'admin'

#тест на то что администратор не может получить несуществующиего пользователя
def test_admin_get_nonexistent_user(create_delete_profile):
    response = login_account("admin", "admin123").json()
    token = response["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"https://secby.ru/api/profiles/999999", headers=headers)

    assert response.status_code == 404