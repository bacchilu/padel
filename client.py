import requests


response = requests.post(
    "http://0.0.0.0:5000/disponibilita",
    json={
        "giorni": ["2023-10-01T11:00:00", "2023-10-02T12:00:00"],
        "callback": "bacchilu@gmail.com",
    },
)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Failure:", response.status_code, response.text)
