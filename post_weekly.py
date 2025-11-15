import os
from slack_bolt import App
from storage import set_active_message
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SIGNUP_CRON = os.environ.get("SIGNUP_CRON", "0 9 * * MON")

app = App(token=SLACK_BOT_TOKEN)

def post_weekly_message(channel_id):
    """Posts the weekly signup message and stores the message ID."""
    text = "It's Walk-n-Talk time! React to this message with any emoji to join this week's pairing. 🚶‍♀️🚶‍♂️"

    try:
        result = app.client.chat_postMessage(
            channel=channel_id,
            text=text
        )
        message_ts = result["ts"]
        set_active_message(message_ts)
        print(f"Weekly post sent. Stored message ts: {message_ts}")
        return message_ts

    except SlackApiError as e:
        print(f"Error posting message: {e.response['error']}")
        return None


if __name__ == "__main__":
    CHANNEL = os.environ.get("WALK_CHANNEL")
    if not CHANNEL:
        raise ValueError("WALK_CHANNEL env variable not set")

    post_weekly_message(CHANNEL)
