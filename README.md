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

### Without docker
* [Install Python](https://www.python.org/downloads/) on your testing device.
* Install the Slack prerequisites with ```python -m pip install slack-bolt slack-sdk```.

### Optional - add pip to path
To ensure you can simply run ```pip``` rather than type ```python -m pip```, you can add the Python directory to your PATH. 
*  Open a terminal
* Type ```sysdm.cpl```
* Go to **Advanced** > **Environment Variables**
* Under **User variables**, select **Path**
* Click **Edit**
* Click **New**
* Add the path where Python is installed, e.g. ```C:\Users\<YOUR USERNAME>\AppData\Local\Python\pythoncore-3.14-64\Scripts```
* Click on **OK** > **OK** > **OK**
* Restart PowerShell (and VSCode if you're running these commands from a terminal in VSCode)

You can test that this change was successful with ```pip --version```. 

### With docker
* Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Run the installer

> [!INFO]
> Running Docker in Windows requires WSL 2 to be installed, and virtualisation needs to be enabled in the BIOS. 

Verify docker is working: 
* Open a terminal
* Run ```docker --version```

If this all works correctly, the next step is to get the app running in Docker.

Run the app using ```docker compose up

# Set up a channel and invite the app
* Create the channel where you want the bot to run
* Type ```/apps```
* Search for the app by name

The app will now start listening in the channel.