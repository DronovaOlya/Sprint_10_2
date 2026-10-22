import random

def random_email():
    random_number = random.randint(000, 999)
    return f"test_{random_number}@yandex.ru"

def random_name():
    random_number = random.randint(000, 999)
    return f"Тестовое название_{random_number}"