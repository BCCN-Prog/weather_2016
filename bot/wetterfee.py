import os
import time
from slackclient import SlackClient
from wit import Wit
#import wit_bot
from random import shuffle

def handle_command(command, channel, context={}):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    # response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
    #            "* command with numbers, delimited by spaces."
    response = ''
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    if 'coffee' in command:
        response = "There is a coffee shop just outside the class room. It's open 'til 4pm."
    if get_weather_context(command) and 'weather' in context:
        if has_loc(command):
            loc = get_loc(command)
        else:
            loc = 'Berlin'
        if has_date(command):
            date = get_date(command)
        else:
            date = time.strftime("%D")
        response = get_forecast(loc, date)
        del context['weather']
    if not(context):
        context = client.run_actions(session_id, command, context)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
    return context

def get_weather_context(command):
    response = False
    buzz_words = ['weather', 'cold', 'warm', 'rain', 'sunny', 'cloudy']
    for word in buzz_words:
        if word in command:
            response = True
    return response

def has_word(buzz_words, command):
    response = False
    for word in buzz_words:
        if word in command:
            response = True
    return response

def has_date(command):
    buzz_words = ['today', 'tomorrow', 'yesterday', 'on', 'May', 'June', 'July', 'April']
    return has_word(buzz_words, command)

def has_loc(command):
    buzz_words = ['in']
    return has_word(buzz_words, command)

def get_date(command):
    if 'on' in command:
        idx = command.split(' ').index('on')
        return command.split(' ')[idx+1] + ' ' + command.split(' ')[idx+2]
    return 'May 31'

def get_loc(command):
    idx = command.split(' ').index('in')
    return command.split(' ')[idx+1]

def get_forecast(loc, date):
    return "On " + date + " the weather in " + loc + " will be " + "sunny"

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

# set up Wit
def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def say(session_id, context, msg):
    print(msg)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=msg, as_user=True)

def send(request, response):
    print(response['text'])
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response['text'], as_user=True)

def merge(session_id, context, entities, msg):
    if 'joke' in context:
        del context['joke']
    category = first_entity_value(entities, 'category')
    if category:
        context['cat'] = category
    return context

def select_joke(session_id, context):
    try:
        jokes = all_jokes[context['cat']]
    except KeyError:
        jokes = all_jokes['all']
    shuffle(jokes)
    context['joke'] = jokes[0]
    return context

def error(session_id, context, e):
    print(str(e))



# wetterfee's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

all_jokes = {
    'chuck': [
        'Chuck Norris counted to infinity - twice.',
        'Death once had a near-Chuck Norris experience.',
    ],
    'tech': [
        'Did you hear about the two antennas that got married? The ceremony was long and boring, but the reception was great!',
        'Why do geeks mistake Halloween and Christmas? Because Oct 31 === Dec 25.',
    ],
    'default': [
        'Why was the Math book sad? Because it had so many problems.',
    ],
    'all': [
        'Chuck Norris counted to infinity - twice.',
        'Death once had a near-Chuck Norris experience.',
        'Did you hear about the two antennas that got married? The ceremony was long and boring, but the reception was great!',
        'Why do geeks mistake Halloween and Christmas? Because Oct 31 === Dec 25.',
        'Why was the Math book sad? Because it had so many problems.',
    ],
}

actions = {
    'say': say,
    'merge': merge,
    'error': error,
    'select-joke': select_joke,
    'send': send,
}

client = Wit(os.environ.get('WIT_TOKEN'), actions)
session_id = 'my-user-id-42'


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    context = {}
    if slack_client.rtm_connect():
        print("wetterfee connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                context = handle_command(command, channel, context)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
