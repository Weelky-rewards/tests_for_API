import pytest

import helpers


@pytest.fixture()
def create_delete_user():
    created_users_id = []

    def _create(user_name, email, password):
        response = helpers.create_account(user_name, email, password)
        if response.status_code != 200:
            pytest.fail(f"Не удалось создать: {response.text}")

        account_id = response.json()["account"]["id"]
        created_users_id.append(account_id)
        return account_id

    yield _create
    for acc_id in created_users_id:
        helpers.delete_account(acc_id)

@pytest.fixture()
def create_delete_profile():
    created_users_id = []

    def _create(user_name, email, password):
        response = helpers.create_account(user_name, email, password)
        if response.status_code != 200:
            pytest.fail(f"Не удалось создать: {response.text}")

        account_id = response.json()["account"]["id"]
        created_users_id.append(account_id)
        _ = helpers.create_profile(user_name,email,password)
        return account_id

    yield _create
    for acc_id in created_users_id:
        helpers.delete_account(acc_id)