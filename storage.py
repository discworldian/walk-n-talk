import os
import json
from threading import Lock

DATA_DIR = "/app/data"
DATA_FILE = os.path.join(DATA_DIR, "signups.json")

_lock = Lock()


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"signups": []}, f)


def _load():
    if not os.path.exists(DATA_FILE):
        return {"signups": []}
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"signups": []}


def _save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def add_signup(user_id):
    with _lock:
        data = _load()
        users = data.get("signups", [])
        if user_id not in users:
            users.append(user_id)
        data["signups"] = users
        _save(data)


def get_signups():
    return _load().get("signups", [])


def clear_signups():
    with _lock:
        _save({"signups": []})
