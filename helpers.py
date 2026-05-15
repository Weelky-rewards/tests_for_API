import requests


def create_account(user_name, email, password):
    body = {
        "username": f"{user_name}",
        "email": f"{email}",
        "password": f"{password}"
    }

    response = requests.post("https://secby.ru/api/auth/register", json=body)
    return response

def login_account(user_name, password):
    body = {
        "username": f"{user_name}",
        "password": f"{password}"
    }

    response = requests.post("https://secby.ru/api/auth/login", json=body)

    return response

def create_profile(user_name,email,password):
    response = login_account(user_name,password)
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "name": f"{user_name}",
        "surname": f"{user_name}",
        "middlename": "test",
        "birthdate": "12.07.2005",
        "about": f"{user_name} + {email}",
        "links": "test_link"
    }

    requests.post(f"https://secby.ru/api/profiles/",json=body, headers=headers)
    return response


def delete_account(id):
    response = login_account("admin","admin123").json()
    token = response["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.delete(f"https://secby.ru/api/profiles/{id}", headers=headers)

    return response