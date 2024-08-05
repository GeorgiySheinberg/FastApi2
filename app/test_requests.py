"""
"""
import requests

search_title = "Test_title"

# Регистрация пользователя

response = requests.post("http://127.0.0.1:8000/v1/user", json={"login": "USER NAME", "password": "UserPassword1234"})
print(response.status_code)
USER_ID = response.json().get("user_id")
print(response.json())

# Получение токена

response = requests.post("http://127.0.0.1:8000/v1/login/", json={"login": "USER NAME",
                                                                  "password": "UserPassword1234"})
print(response.status_code)
print(response.json())
token = response.json().get("token")

# Изменение пользователя
response = requests.patch(f"http://127.0.0.1:8000/v1/user/{USER_ID}/",
                          json={"login": "New User Name",
                                'password': 'new_password'},
                          headers={"x-token": token})
print(response.status_code)
print(response.json())

# Создание объявления

post_response = requests.post("http://127.0.0.1:8000/v1/advertisement/",
                              json={"title": "Test_title",
                                    "description": "Test description",
                                    "price": 1000.0},
                              headers={"x-token": token})
print(post_response.status_code)
print(post_response.json())

# Просмотр объявления неавторизованным пользователем

response = requests.get(f"http://127.0.0.1:8000/v1/advertisement/{post_response.json().get("id")}/")

print(response.status_code)
print(response.json())

# Редактирование объявление авторизованным пользователем
patch_response = requests.patch(
    f"http://127.0.0.1:8000/v1/advertisement/{post_response.json().get("id")}/",
    json={
        "description": "New description",
        "price": 2000.0,
        "login": "New login"},
    headers={"x-token": token}

)

print(patch_response.json())
print(patch_response.status_code)

# Поиск по полям
response = requests.get(f"http://127.0.0.1:8000/v1/advertisement/?title=Test_title")
print(response.status_code)
print(response.json())

# Удаление объявления
response = requests.delete(f"http://127.0.0.1:8000/v1/advertisement/{post_response.json().get("id")}/",
                           headers={"x-token": token})

print(response.json())
print(response.status_code)

# проверка
response = requests.get(f"http://127.0.0.1:8000/v1/advertisement/{post_response.json().get("id")}/")

print(response.status_code)
print(response.json())

# Удаление пользователя
response = requests.delete(f"http://127.0.0.1:8000/v1/user/{USER_ID}/", headers={"x-token": token})
print(response.status_code)
print(response.json())

# Проверка
response = requests.get(f"http://127.0.0.1:8000/v1/user/{USER_ID}/")

print(response.status_code)
print(response.json())
