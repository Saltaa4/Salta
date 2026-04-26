import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DEFAULT_SETTINGS = {
    "sound": True,
    "difficulty": "normal",
    "car_color": "blue",
    "username": "Player"
}


def load_json(filename, default):
    path = BASE_DIR / filename

    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
    except (json.JSONDecodeError, OSError):
        pass

    return default


def save_json(filename, data):
    path = BASE_DIR / filename

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_settings():
    settings = load_json("settings.json", DEFAULT_SETTINGS.copy())

    for key, value in DEFAULT_SETTINGS.items():
        settings.setdefault(key, value)

    return settings


def save_settings(settings):
    save_json("settings.json", settings)


def load_leaderboard():
    data = load_json("leaderboard.json", [])

    if not isinstance(data, list):
        return []

    return data


def save_leaderboard(leaderboard):
    leaderboard = sorted(
        leaderboard,
        key=lambda entry: int(entry.get("score", 0)),
        reverse=True
    )[:10]

    save_json("leaderboard.json", leaderboard)


def add_leaderboard_entry(entry):
    leaderboard = load_leaderboard()
    leaderboard.append(entry)
    save_leaderboard(leaderboard)
    return load_leaderboard()