import requests

post_response = requests.post("http://127.0.0.1:8080/v1/advertisement/",
                              json={"title": "title",
                                    "description": "description1",
                                    "price": 1100.10,
                                    "author": "user1"})
print()
print("POST response:", post_response.json())
print("POST response status code:", post_response.status_code)

get_response = requests.get(f"http://127.0.0.1:8080/v1/advertisement/{post_response.json().get("id")}/")

print("GET response:", get_response.json())
print("GET response status code:", get_response.status_code)

patch_response = requests.patch(
    f"http://127.0.0.1:8080/v1/advertisement/{post_response.json().get("id")}/",
    json={
        "description": "description2",
        "price": 2000.0,
        "author": "polzovatel"}
)

print(patch_response.json())
print(patch_response.status_code)

response = requests.get(f"http://127.0.0.1:8080/v1/advertisement/{post_response.json().get("id")}/")

print(response.json())
print(response.status_code)

response = requests.get(f"http://127.0.0.1:8080/v1/advertisement/{post_response.json().get("id")}/")

print(response.status_code)
print(response.json())

response = requests.get("http://127.0.0.1:8080/v1/advertisement/?title=title")
print(response.status_code)
print(response.json())

response = requests.delete(f"http://127.0.0.1:8080/v1/advertisement/{post_response.json().get("id")}/")

print(response.json())
print(response.status_code)

response = requests.get(f"http://127.0.0.1:8080/v1/advertisement/{post_response.json().get("id")}/")

print(response.status_code)
print(response.json())
