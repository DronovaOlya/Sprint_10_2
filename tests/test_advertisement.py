import requests
import allure
from urls import BASE_URL, CREATE_ADVERTISEMENT, UPDATE_ADVERTISEMENT
from data import data_advertisement, status_code_success_201, status_code_success_200, status_code_failure_401
from helpers import random_name

@allure.epic('API объявления: создание и изменение')
class TestAdvertisementApi:
    @allure.title('Успешное создание объявления')
    def test_create_advertisement(self, user_create):
        user = user_create()
        payload = data_advertisement.copy()
        files = {key: (None, str(value)) for key, value in payload.items()}
        response = requests.post(f"{BASE_URL}{CREATE_ADVERTISEMENT}", files=files, headers={"Authorization": f"Bearer {user['access_token']}"})
    
        assert response.status_code == status_code_success_201
        assert response.json()["name"] == payload["name"]
        assert "id" in response.json()

    @allure.title('Успешное редактирование объявления')
    def test_update_advertisement(self, user_create, create_advertisement):
        user = user_create()
        advertisement = create_advertisement(user)
        advertisement_id = advertisement["id"]
        old_name = advertisement["name"]
        new_name = random_name() 
        payload = {
                    "name": new_name,
                    "category": advertisement["category"],
                    "condition": advertisement["condition"],
                    "city": advertisement["city"],
                    "description": advertisement["description"],
                    "price": advertisement["price"]
                }
        files = {key: (None, str(value)) for key, value in payload.items()}
        response = requests.patch(f"{BASE_URL}{UPDATE_ADVERTISEMENT}{advertisement_id}", files=files, headers={"Authorization": f"Bearer {user['access_token']}"})
        
        assert response.status_code == status_code_success_200
        assert response.json()["name"] == new_name

    @allure.title('Редактирование объявления, другим пользователем')
    def test_update_advertisement_another_user(self, user_create, create_advertisement):
        user_a = user_create()                        
        user_b = user_create()                        
        advertisement = create_advertisement(user_a)
        advertisement_id = advertisement["id"]
        old_name = advertisement["name"]
        new_name = random_name()
        payload = {
                    "name": new_name,
                    "category": advertisement["category"],
                    "condition": advertisement["condition"],
                    "city": advertisement["city"],
                    "description": advertisement["description"],
                    "price": advertisement["price"]
                }
        files = {key: (None, str(value)) for key, value in payload.items()}
        response = requests.patch(f"{BASE_URL}{UPDATE_ADVERTISEMENT}{advertisement_id}", files=files, headers={"Authorization": f"Bearer {user_b['access_token']}"})

        assert response.status_code == status_code_failure_401
        assert "message" in response.json() and "Оффер не найден или у вас нет прав на его редактирование" in response.json()["message"]


            