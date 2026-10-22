import pytest
import requests
from urls import BASE_URL, CREATE_USER, CREATE_ADVERTISEMENT
from helpers import random_email, random_name
from data import password, data_advertisement


@pytest.fixture
def user_create():
    def _user_create():
        email = random_email()
        payload = {"email": email, "password": password, "submitPassword": password}
        response = requests.post(f"{BASE_URL}{CREATE_USER}", json=payload)
        body = response.json()
        token = body.get("access_token", {}).get("access_token") or body.get("accessToken")
        return {
            "email": email,
            "password": password,
            "id": body["user"]["id"],
            "access_token": token,
        }
    return _user_create

@pytest.fixture
def create_advertisement():
    def _create_advertisement(owner):
        payload = data_advertisement.copy()
        payload["name"] = random_name()
        files = {key: (None, str(value)) for key, value in payload.items()}
        response = requests.post(f"{BASE_URL}{CREATE_ADVERTISEMENT}",files=files,headers={"Authorization": f"Bearer {owner['access_token']}"},)
        body = response.json()
        return body
    return _create_advertisement
