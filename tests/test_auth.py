"""인증(회원가입 / 로그인) 테스트"""

import pytest

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"

TEST_USER = {
    "email": "tester@beandebug.dev",
    "username": "tester",
    "password": "securepass123",
    "full_name": "Test User",
}


@pytest.fixture()
def registered_user(client):
    res = client.post(REGISTER_URL, json=TEST_USER)
    assert res.status_code == 201
    return res.json()


def test_register_success(client):
    payload = {
        "email": "newuser@beandebug.dev",
        "username": "newuser",
        "password": "strongpass1",
        "full_name": "New User",
    }
    res = client.post(REGISTER_URL, json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["username"] == "newuser"
    assert "hashed_password" not in data


def test_register_duplicate_email(client, registered_user):
    payload = {**TEST_USER, "username": "other"}
    res = client.post(REGISTER_URL, json=payload)
    assert res.status_code == 400
    assert "Email already registered" in res.json()["detail"]


def test_register_duplicate_username(client, registered_user):
    payload = {**TEST_USER, "email": "other@beandebug.dev"}
    res = client.post(REGISTER_URL, json=payload)
    assert res.status_code == 400
    assert "Username already taken" in res.json()["detail"]


def test_login_success(client, registered_user):
    res = client.post(
        LOGIN_URL,
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]},
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, registered_user):
    res = client.post(
        LOGIN_URL,
        data={"username": TEST_USER["username"], "password": "wrongpassword"},
    )
    assert res.status_code == 401


def test_get_me(client, registered_user):
    # 로그인
    login_res = client.post(
        LOGIN_URL,
        data={"username": TEST_USER["username"], "password": TEST_USER["password"]},
    )
    token = login_res.json()["access_token"]
    me_res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["username"] == TEST_USER["username"]
