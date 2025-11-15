import os
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from storage import init_db, add_signup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read tokens from environment variables
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

# Create the Bolt app
app = App(token=SLACK_BOT_TOKEN)

@app.event("reaction_added")
def handle_reaction_added(event, logger):
    logger.info(f"Reaction event received: {event}")
    user_id = event.get("user")
    add_signup(user_id)
    logger.info(f"Signed up: {user_id}")

if __name__ == "__main__":
    init_db()
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    logger.info("Starting Socket Mode handler…")
    handler.start()
