import boto3
import random
from slack_sdk import WebClient

ssm = boto3.client("ssm")
dynamodb = boto3.resource("dynamodb")
signups_table = dynamodb.Table("WalkSignups")

SLACK_BOT_TOKEN = None

def get_bot_token():
    global SLACK_BOT_TOKEN
    if SLACK_BOT_TOKEN is None:
        param = ssm.get_parameter(
            Name="/walkntalk/slack_bot_token",
            WithDecryption=True
        )
        SLACK_BOT_TOKEN = param["Parameter"]["Value"]
    return SLACK_BOT_TOKEN

def get_week_key():
    from datetime import date
    y, w, _ = date.today().isocalendar()
    return f"{y}-W{w}"

def lambda_handler(event, context):
    client = WebClient(token=get_bot_token())
    week_key = get_week_key()

    # Fetch signups
    resp = signups_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("week_key").eq(week_key)
    )
    users = [item["user_id"] for item in resp["Items"]]

    if len(users) < 2:
        return

    random.shuffle(users)
    pairs = []
    while len(users) >= 2:
        a = users.pop()
        b = users.pop()
        pairs.append((a, b))

    if users and pairs:
        a, b = pairs[-1]
        c = users.pop()
        pairs[-1] = (a, b, c)

    for group in pairs:
        dm = client.conversations_open(users=",".join(group))
        ch_id = dm["channel"]["id"]
        mentions = ", ".join(f"<@{u}>" for u in group)
        client.chat_postMessage(
            channel=ch_id,
            text=(
                f"Hi {mentions}! 👋\n\n"
                f"You’ve been matched for this week’s Walk & Talk ({week_key}). "
                "Use this DM to arrange a time that works for you."
            )
        )
