import requests
import allure
from helpers import random_email
from urls import BASE_URL, CREATE_USER, LOGIN_USER
from data import password, status_code_success_201, status_code_failure_400

@allure.epic("API пользователя: регистрация и авторизация")
class TestUserApi:
    @allure.title('Успешное создание пользователя')
    def test_create_user(self):
        email = random_email()
        payload = { "email": email,
                    "password": password,
                    "submitPassword": password
                    }
        response = requests.post(f"{BASE_URL}{CREATE_USER}", json=payload)
        
        assert response.status_code == status_code_success_201
        assert response.json()["user"]["email"] == email
        assert "id" in response.json()["user"]
        assert "access_token" in response.json()

    @allure.title('Создание существующего пользователя') 
    def test_create_existing_user(self, user_create):
        payload = user_create()
        response = requests.post(f"{BASE_URL}{CREATE_USER}", json=payload)
        
        assert response.status_code == status_code_failure_400
        assert "message" in response.json() and "Почта уже используется" in response.json()["message"]

    @allure.title('Успешная авторизация пользователя')
    def test_login_user(self, user_create):
        payload = user_create()
        response = requests.post(f"{BASE_URL}{LOGIN_USER}", json=payload)
                 
        assert response.status_code == status_code_success_201
        assert response.json()["user"]["email"] == payload["email"]
        assert response.json()["user"]["id"] == payload["id"]
