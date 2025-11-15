import json
import os
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG_PATH = "config.json"

def load_raw_config() -> Dict[str, Any]:
    """
    Load JSON config from disk. Path can be overridden with WALKNTALK_CONFIG.
    """
    path = Path(os.environ.get("WALKNTALK_CONFIG", DEFAULT_CONFIG_PATH))

    if not path.exists():
        # Minimal default if no file exists
        return {
            "weekly_schedule": {
                "signup_message_cron": "0 9 * * MON",
                "pairings_cron": "0 16 * * FRI",
            }
        }

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_schedule_config() -> dict:
    """
    Return schedule configuration, with environment variables overriding the file.
    """
    cfg = load_raw_config()
    weekly = cfg.setdefault("weekly_schedule", {})

    # values from file or defaults
    signup_cron = weekly.get("signup_message_cron", "0 9 * * MON")
    pairings_cron = weekly.get("pairings_cron", "0 16 * * FRI")

    # env var overrides (optional)
    signup_cron = os.environ.get("WALKNTALK_SIGNUP_CRON", signup_cron)
    pairings_cron = os.environ.get("WALKNTALK_PAIRINGS_CRON", pairings_cron)

    return {
        "signup_message_cron": signup_cron,
        "pairings_cron": pairings_cron,
    }
