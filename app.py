import os
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from storage import init_db, add_signup, get_active_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("Sign up message schedule (SIGNUP_CRON) =", os.environ.get("SIGNUP_CRON"))
print("Pairings schedule (PAIRINGS_CRON) =", os.environ.get("PAIRINGS_CRON"))
print("Monitoring channel (WALK_CHANNEL) =", os.environ.get("WALK_CHANNEL"))

# Read tokens from environment variables
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

# Create the Bolt app
app = App(token=SLACK_BOT_TOKEN)

@app.event("reaction_added")
def handle_reaction_added(event, logger):
    active = get_active_message()
    reacted_ts = event.get("item", {}).get("ts")
    user_id = event.get("user")

    # Ignore reactions on any other message
    if reacted_ts != active:
        return

    add_signup(user_id)
    logger.info(f"Signup on active message: {user_id}")

if __name__ == "__main__":
    init_db()
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    logger.info("Starting Socket Mode handler…")
    handler.start()
