from slackclient import SlackClient
import os as os

token = os.environ.get('SLACK_BOT_TOKEN')
BOT_NAME = 'wetterfeeddd'

#sc = SlackClient(token)
#print(sc.api_call("api.test"))

slack_client = SlackClient(token)

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                wetterfee_id = user.get('id')
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
            else:
                print("ID is " + user['name'] + " with ID " + user.get('id'))

    else:
        print("could not find bot user with the name " + BOT_NAME)
