import re
from datetime import datetime, date, time
from dataclasses import dataclass, asdict
from typing import Literal


@dataclass(kw_only=True)
class TimeSlot:
    date: date
    time: int

    @classmethod
    def from_iso(cls, iso_str):
        d = datetime.fromisoformat(iso_str)
        if 9 <= d.hour <= 23:
            return cls(date=d.date(), time=d.hour)
        raise Exception("Wrong data format")

    def to_dict(self):
        return {**asdict(self), "date": self.date.isoformat()}

    def is_expired(self):
        return datetime.combine(self.date, time(self.time)) < datetime.now()


@dataclass(kw_only=True)
class Callback:
    type: Literal["EMAIL", "URL"]
    value: str


@dataclass(kw_only=True)
class BookingRequests:
    user_id: int
    time_slot: TimeSlot
    callback: Callback

    @staticmethod
    def check_email_or_url(input_string: str):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        url_pattern = r"^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
        if re.match(email_pattern, input_string):
            return Callback(type="EMAIL", value=input_string)
        elif re.match(url_pattern, input_string):
            return Callback(type="URL", value=input_string)
        raise Exception("Wrong data format")

    @classmethod
    def from_dict(cls, user_id: int, json_data: dict):
        return [
            cls(
                user_id=user_id,
                time_slot=TimeSlot.from_iso(d),
                callback=cls.check_email_or_url(json_data["callback"]),
            )
            for d in json_data["giorni"]
        ]

    def to_dict(self):
        return {**asdict(self), "time_slot": self.time_slot.to_dict()}


@dataclass
class UserData:
    id: int
    user: str


@dataclass
class SlotData:
    id: int
    name: str


@dataclass
class BookingData:
    slot_id: int
    data: BookingRequests
