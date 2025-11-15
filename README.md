# walk-n-talk
Slack app to pair up colleagues for weekly walk 'n talks.

## Authorisation in Slack
* Go to https://api.slack.com/ and select **Create App**. 
* On the left-hand side, under **Socket Mode**, enable **Socket mode** and store the app token in a secure location, such as a password manager, and/or within repository secrets. This will be referred to as the ```SLACK_APP_TOKEN```.
* Add the following permissions on your workspace:
    * ```chat:write```
    * ```reactions:write```
    * ```users.read```
    * ```connections:write```

    From this page, store the **Bot User OAuth Token**. This will be referred to as the ```SLACK_BOT_TOKEN```.

