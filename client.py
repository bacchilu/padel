from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from pprint import pprint

import requests

import jwt


JWT_SECRET_KEY = "HELLO_WORLD"


@dataclass
class Payload:
    id: int
    user: str
    exp: datetime = field(
        default_factory=lambda: datetime.now(tz=timezone.utc) + timedelta(days=1)
    )


jwt_token = jwt.encode(
    asdict(Payload(id=1, user="Luca")), JWT_SECRET_KEY, algorithm="HS256"
)
response = requests.post(
    "http://0.0.0.0:5000/disponibilita",
    headers={
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    },
    json={
        "giorni": ["2023-10-01 11", "2023-10-02 09", "2024-11-11 12"],
        "callback": "bacchilu@gmail.com",
    },
)

if response.status_code == 200:
    print("Success")
    pprint(response.json())
else:
    print("Failure:", response.status_code, response.text)
