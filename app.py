import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Read env vars (in Docker, from env; in CI, from GitHub secrets)
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)


@app.event("reaction_added")
def handle_reaction_added(event, logger):
    logger.info(f"Reaction event: {event}")


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()