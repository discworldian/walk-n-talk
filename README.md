# walk-n-talk
Slack app to pair up colleagues for weekly walk 'n talks. In order to run the app, you need to create a Slack app, and allow it to run in the Slack workspace. Then, you need to run the code on a server. The option to create a  local testing set-up is also explained below. 

## Create the Slack app
### Create app
* Go to https://api.slack.com/ and select **Create App**. 
* Give the app a sensible name, e.g. "Walk and Talk"
* Add an icon image
### Turn on socket mode
* On the left-hand side, under **Socket Mode**, enable **Socket mode** and store the app token in a secure location, such as a password manager, and/or within repository secrets. This will be referred to as the ```SLACK_APP_TOKEN```.
### Add permissions
* Add the following permissions on your workspace:
    * ```chat:write```
    * ```reactions:read``` and ```reactions:write```
    * ```users.read```
    * ```connections:write```

    From this page, store the **Bot User OAuth Token**. This will be referred to as the ```SLACK_BOT_TOKEN```.
### Enable events
* Go to **Event Subscriptions** in the left-hand side menu
* Click on the **Enable Events** slide to turn it on
* Click on **Subscribe to bot events** 
* Click on **Add Bot User Event**
* Select **reaction_added**
* Click on **Save Changes**

## Local testing setup
The local testing setup uses Docker Desktop to run the application.

* Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Run the installer

> [!INFO]
> Running Docker in Windows requires WSL 2 to be installed, and virtualisation needs to be enabled in the BIOS. 

Verify docker is working: 
* Open a terminal
* Run ```docker --version```

If this all works correctly, the next step is to get the app running in Docker.

Run the app using ```docker compose up```.

# Set up a channel and invite the app
* Create the channel where you want the bot to run
* Type ```/apps```
* Search for the app by name

The app will now start listening in the channel. You will need the ID of the channel for the environment variable WALK_CHANNEL. 

## Tests
* ```docker compose run --rm walkntalk-bot python post_weekly.py``` will run the weekly post message.