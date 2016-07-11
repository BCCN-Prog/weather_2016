from slackclient import SlackClient
import time
import os as os

import dave_wit_test as my_wit

#read exported token value from terminal
token = os.environ.get('SLACK_BOT_TOKEN')

# starterbot's ID as an environment variable
BOT_NAME = 'eliza_rt'
#BOT_ID = 'U1LTXBQEP' #os.environ.get("BOT_ID")

# connect to SlackClient
sc = SlackClient(token)


# find out the BOT_ID based on the BOT_NAME
if __name__ == "__main__":
    api_call = sc.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                BOT_ID = user.get('id')
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))

    else:
        print("could not find bot user with the name " + BOT_NAME)



# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    sc.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


print("Beginning RTM connection listen loop")
if sc.rtm_connect():
    while True:
        #print(sc.rtm_read())
        #time.sleep(1)
        realtime_read = sc.rtm_read()
        #print(realtime_read)
        command, channel = parse_slack_output(realtime_read)
        if command and channel:
                print("command: " + command + " channel: " + channel)
                handle_command(command, channel)
        time.sleep(1)
else:
    print("Connection Failed, invalid token?")
