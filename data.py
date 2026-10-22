from helpers import random_name

password = "123456"

data_advertisement = {"name":random_name(),
                        "category":"Садоводство",
                        "condition":"Новый",
                        "city":"Москва",
                        "description":"Тестовое описание товара",
                        "price":"12000"}

status_code_success_201 = 201
status_code_success_200 = 200
status_code_failure_400 = 400
status_code_failure_401 = 401