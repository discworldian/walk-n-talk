#!/usr/bin/env python3
import json
import logging
import os
import random
import sys
from pathlib import Path
from typing import List

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
WALK_CHANNEL = os.environ.get("WALK_CHANNEL")
PAIRINGS_CRON = os.environ.get("PAIRINGS_CRON", "0 16 * * FRI")

STATE_FILE = os.environ.get("STATE_FILE", "signup_state.json")

if not SLACK_BOT_TOKEN:
    print("Missing SLACK_BOT_TOKEN in environment.", file=sys.stderr)
    sys.exit(1)

if not WALK_CHANNEL:
    print("Missing WALK_CHANNEL in environment.", file=sys.stderr)
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(name)s:%(funcName)s:%(message)s",
)
logger = logging.getLogger("pair_and_msg")

client = WebClient(token=SLACK_BOT_TOKEN)


def make_walkntalk_groups(user_ids: List[str]) -> List[List[str]]:

    users = user_ids[:]
    random.shuffle(users)

    groups: List[List[str]] = []
    i = 0
    n = len(users)

    while i < n:
        remaining = n - i
        if remaining == 3:
            # final trio
            groups.append(users[i:i + 3])
            break
        else:
            # normal pair
            groups.append(users[i:i + 2])
            i += 2

    return groups


def format_mentions(user_ids: List[str]) -> str:
    return " ".join(f"<@{u}>" for u in user_ids)


def load_participants_from_state(path: str | Path) -> List[str]:
    path = Path(path)
    if not path.exists():
        logger.error("State file %s does not exist.", path)
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse JSON state file %s: %s", path, e)
        return []

    participants = data.get("participants") or []
    if not isinstance(participants, list):
        logger.error("State file %s has invalid 'participants' field.", path)
        return []

    participants = [str(u) for u in participants if u]
    return participants


def dm_group(client: WebClient, user_ids: List[str]) -> None:

    try:
        resp = client.conversations_open(users=user_ids)
        dm_channel = resp["channel"]["id"]
    except SlackApiError as e:
        logger.error("Failed to open DM for %s: %s", user_ids, e)
        return

    try:
        client.chat_postMessage(
            channel=dm_channel,
            text=(
                f"👟 You’ve been paired for this week’s Walk n Talk!\n"
                f"Participants: {format_mentions(user_ids)}\n\n"
                "Pick a time together and go for a walk while you chat."
            ),
        )
        logger.info("Sent DM to group: %s", user_ids)
    except SlackApiError as e:
        logger.error("Failed to send DM to %s: %s", user_ids, e)


def post_public_summary(client: WebClient, channel: str, groups: List[List[str]]) -> None:
    if not groups:
        try:
            client.chat_postMessage(
                channel=channel,
                text="👣 Not enough signups for Walk n Talk pairings this week.",
            )
            logger.info("Posted 'not enough signups' message in %s", channel)
        except SlackApiError as e:
            logger.error("Failed to post public message: %s", e)
        return

    lines: List[str] = []
    for idx, group in enumerate(groups, start=1):
        lines.append(f"*Group {idx}:* {format_mentions(group)}")

    text = "👣 This week’s Walk n Talk pairings:\n" + "\n".join(lines)

    try:
        client.chat_postMessage(
            channel=channel,
            text=text,
        )
        logger.info("Posted public summary with %d groups in %s", len(groups), channel)
    except SlackApiError as e:
        logger.error("Failed to post public summary: %s", e)


def main() -> None:
    participants = load_participants_from_state(STATE_FILE)
    if len(participants) < 2:
        logger.warning("Not enough participants to create pairings: %s", participants)
        post_public_summary(client, WALK_CHANNEL, [])
        return

    logger.info("Loaded %d participants: %s", len(participants), participants)

    groups = make_walkntalk_groups(participants)
    logger.info("Created %d groups", len(groups))

    # DM each group
    for group in groups:
        dm_group(client, group)

    # Post summary in public channel
    post_public_summary(client, WALK_CHANNEL, groups)


if __name__ == "__main__":
    main()
