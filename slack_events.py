import json
import os
import hmac
import hashlib
import time
import urllib.parse
import boto3

ssm = boto3.client("ssm")
dynamodb = boto3.resource("dynamodb")
signups_table = dynamodb.Table("WalkSignups")

# Cache secrets after first fetch
SLACK_SIGNING_SECRET = None

def get_signing_secret():
    global SLACK_SIGNING_SECRET
    if SLACK_SIGNING_SECRET is None:
        param = ssm.get_parameter(
            Name="/walkntalk/slack_signing_secret",
            WithDecryption=True
        )
        SLACK_SIGNING_SECRET = param["Parameter"]["Value"]
    return SLACK_SIGNING_SECRET

def verify_slack_signature(headers, body):
    secret = get_signing_secret().encode()
    timestamp = headers.get("x-slack-request-timestamp") or headers.get("X-Slack-Request-Timestamp")
    sig = headers.get("x-slack-signature") or headers.get("X-Slack-Signature")

    if not timestamp or not sig:
        return False

    # optional replay protection
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    basestring = f"v0:{timestamp}:{body}".encode()
    my_sig = "v0=" + hmac.new(secret, basestring, hashlib.sha256).hexdigest()
    return hmac.compare_digest(my_sig, sig)

def get_week_key():
    from datetime import date
    y, w, _ = date.today().isocalendar()
    return f"{y}-W{w}"

def lambda_handler(event, context):
    headers = event.get("headers") or {}
    body = event.get("body") or ""
    if event.get("isBase64Encoded"):
        import base64
        body = base64.b64decode(body).decode("utf-8")

    # Slack url_verification
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        payload = {}

    if payload.get("type") == "url_verification":
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain"},
            "body": payload.get("challenge", "")
        }

    # All other requests must be verified
    if not verify_slack_signature(headers, body):
        return {"statusCode": 401, "body": "invalid signature"}

    # Slack wraps events
    if payload.get("type") == "event_callback":
        event_obj = payload.get("event", {})
        if event_obj.get("type") == "reaction_added":
            handle_reaction_added(event_obj)

    return {"statusCode": 200, "body": ""}

def handle_reaction_added(event):
    # Only care about :walking: in a specific channel (optional)
    reaction = event.get("reaction")
    item = event.get("item", {})
    channel = item.get("channel")
    user = event.get("user")

    if reaction != "walking":
        return
    # Optionally restrict to your walk channel id
    WALK_CHANNEL_ID = os.environ.get("WALK_CHANNEL_ID")
    if WALK_CHANNEL_ID and channel != WALK_CHANNEL_ID:
        return

    # Store signup
    week_key = get_week_key()
    signups_table.put_item(
        Item={
            "week_key": week_key,
            "user_id": user
        }
    )
