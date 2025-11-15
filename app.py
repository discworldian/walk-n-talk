import os
import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Basic logging to stdout so you can see events in `docker compose up`
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read tokens from environment variables (provided via .env in Docker)
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

# Create the Bolt app
app = App(token=SLACK_BOT_TOKEN)


@app.event("reaction_added")
def handle_reaction_added(event, logger):
    # This will show up in your `docker compose up` logs
    logger.info(f"Reaction event received: {event}")


if __name__ == "__main__":
    # Socket Mode: no public URL needed, just the app-level token
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    logger.info("Starting Socket Mode handler…")
    handler.start()
