# walk-n-talk
Slack app to pair up colleagues for weekly walk 'n talks.

## Setup in Slack
### Create app
* Go to https://api.slack.com/ and select **Create App**. 
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
* Install Python on your testing device
* Install the Slack prerequisites with ```python -m pip install slack-bolt slack-sdk```.