# tmslack

tmslack is a command line application for easilty sharing a [tmate](https://tmate.io) session with your fellow slack users.

## Installation

There are two parts two installing tmslack:

1. Once per workspace, you will need to create a new application with a bot user.
2. Each person on your team will need to install tmslack and configure it.

### Installing the application

In a nutshell:

1. In a browser where you are logged into a workspace, browse to [https://api.slack.com/apps?new_app=1]().
2. Choose an application name and workspace and then click *Create App*.
3. Click on *Bots* and add a bot user.
4. Click on *Install App* from the menu on the left and click on *Install App to Workspace*.
5. Authorise the application.
6. Copy the *Bot User OAuth Access Token*, you will distribute this to your team.

### Local setup

In a nutshell:

1. Run `pip install https://github.com/outpace/tmslack/archive/master.zip`
2. Add a `${HOME}/.config/tmslack/config.yml` with the following configuration:
   
   ```yaml
   user: <user>
   token: <bot-token>
   ```
   
   *User* should be your username on Slack, and the *bot-token* is the OAuth token from step six in the application installation.


## Usage

To use tmslack, you will need to be inside of an active and connected tmate session.
Once inside, just invoke tmslack with the list of users you would like to invite to your session:

    > tmate anisha taro
    👍

If you get the thumbs up, everything should be great.

If you get a stack trace, feel free to panic.
However, reviewing the error message and maybe opening an issue may be more advisable.


## Further work

* Put the bot in the cloud so that it can use an automated authorisation mechanism
* Add slash commands to generate a user-specific configuration so that messages appear as from the user
* Allow customisation of the invitation message
* Distribute via PyPI
* i18n/l10n

