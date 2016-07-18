import os
import time
from slackclient import SlackClient
from wit import Wit
from random import shuffle
import sys
sys.path.append('../query_engine_v2')
import QueryEngine
import datetime as dt
import urllib, json
import codecs
import numpy as np

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
    if 'döner' in command:
        response = "You mentioned Döner? There is a Späti and a Kebad place just outside on Luisenstr"
    context = client.run_actions(session_id, command, context)
    print(context)
    if 'intent' in context:
        response = context['intent']
        del context['intent']
    if response=='joke':
        context = select_joke(session_id, context)
        response = 'Here is your joke: ' + context['joke']
        del context['joke']
    if response=='weather':
        if context['missingLocation'] and context['missingDate']:
            response = "Sure, for which date and location?"
            context['intent'] = 'weather'
        elif context['missingLocation']:
            response = "For which location?"
            context['intent'] = 'weather'
        elif context['missingDate']:
            response = "For which date?"
            context['intent'] = 'weather'
    if 'location' in context and 'datetime' in context:
        response = get_forecast(context['datetime'], context['location'])
        del context['location']
        del context['datetime']
        del context['missingDate']
        del context['missingLocation']

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)
    return context

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
    #slack_client.api_call("chat.postMessage", channel=channel,
    #                      text=response['text'], as_user=True)

def merge(session_id, context, entities, msg):
    intent = first_entity_value(entities, 'intent')
    datetime = first_entity_value(entities, 'datetime')
    location = first_entity_value(entities, 'location')
    print(entities.keys())
    if intent:
        context['intent'] = intent
    if location:
        context['location'] = location
        context['missingLocation'] = False
    else:
        context['missingLocation'] = True

    if datetime:
        context['datetime'] = datetime
        context['missingDate'] = False
    else:
        context['missingDate'] = True
    return context

def select_joke(session_id, context):
    jokes = all_jokes['all']
    shuffle(jokes)
    context['joke'] = jokes[0]
    return context

def error(session_id, context, e):
    print(str(e))

def parse_date(datetime):
    # build an integer from the date time string
    s = dateString = ''
    year = (datetime.split('T')[0].split('-')[0])
    if int(year)>2016:
        year = '2016'
    month = (datetime.split('T')[0].split('-')[1])
    day = (datetime.split('T')[0].split('-')[2])
    dateString = dt.date(int(year),int(month),int(day)).strftime("%a, %d %b %Y")
    return dateString, int((year) + (month) + (day))

def get_forecast(datetime, location):
    try:
        city_ID = cities_table[location.lower()]
        useAPI = False
    except KeyError:
        print("Could find the city, using API")
        useAPI = True

    # parse the date
    dateString, dateInt = parse_date(datetime)
    locString = location[0].upper() + location[1:]
    dateToday = int(dt.date.today().strftime("%Y%m%d"))
    future = (dateInt >= dateToday)
    verb = 'will be' if future else 'was'

    # if the city was found in the scraping list:
    if not(useAPI):
        try:
            s = Q.smart_slice('daily', return_params=['low', 'high', 'date', 'site', 'city_ID'],
                              params=['date', 'city_ID'],
                              lower=[dateInt, city_ID],
                              upper=[dateInt, city_ID])
            p = Q.get_data('daily', s, return_params=['low', 'high', 'date', 'site', 'city_ID'])
            temp_low = p[:,3].mean()
            temp_high = p[:,2].mean()

            # make sure there is no nan
            assert(np.isfinite(temp_low+temp_high))
            # parse the response
            response = ("Here you go: the temperature in " + locString + " on "
                        + dateString + " "+ verb + " between " + str(int(temp_low)) + " and " + str(int(temp_high))
                        + "°.")
            print(response)
        except:
            print(sys.exc_info())
            useAPI = True
            print("Scraping database failed, using API")

    if useAPI:
        try:
            temp_low, temp_high, conds = get_temp(dateInt, dateToday, location)
            response = ("Here you go: the temperature in " + locString + " on "
                        + dateString + " "+ verb + " between " + temp_low + " and " + temp_high
                        + "°. "+conds + ".")
        except:
            print(sys.exc_info())
            response = "Sorry, I have no data for that one. But remember, '" + bauernregeln[np.random.randint(len(bauernregeln))] + "'"
            print("API failed, using Bauernregeln")
    return response

def get_temp(dateInt, dateToday, location):
    future = (dateInt >= dateToday)
    if future:
        f = urllib.request.urlopen('http://api.wunderground.com/api/944b3f3c879d2394/geolookup/forecast10day/q/Germany/'+location+'.json')
    else:
        f = urllib.request.urlopen('http://api.wunderground.com/api/944b3f3c879d2394/geolookup/history_'+str(dateInt)+'/q/Germany/'+location+'.json')
    reader = codecs.getreader('utf-8') #how is data encoded?
    parsed = json.load(reader(f))
    if future:
        day_diff = dateInt - dateToday
        max_t = parsed['forecast']['simpleforecast']['forecastday'][day_diff]['high']['celsius']
        min_t = parsed['forecast']['simpleforecast']['forecastday'][day_diff]['low']['celsius']
        conds = parsed['forecast']['simpleforecast']['forecastday'][day_diff]['conditions']
    else:
        min_t = parsed['history']['dailysummary'][0]['mintempm']
        max_t = parsed['history']['dailysummary'][0]['maxtempm']
        conds = parsed['history']['observations'][0]['conds']
    return min_t, max_t, conds


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
# mapping for site IDs
cities_table = {"berlin": 1, "hamburg": 2, "muenchen": 3, "koeln": 4,
                "frankfurt": 5, "stuttgart": 6, "bremen" :7, "leipzig": 8,
                "hannover": 9, "nuernberg": 10, "dortmund": 11,
                "dresden": 12, "kassel": 13, "kiel": 14, "bielefeld": 15,
                "saarbruecken": 16, "rostock": 17, "freiburg": 18,
                "magdeburg": 19, "erfurt": 20}

bauernregeln = ["Abendrot Gutwetterbot', Morgenrot mit Regen droht.",
                "Der Nordwind ist ein rauher Vetter, aber er bringt beständig Wetter.",
                "Die Julisonne arbeitet für zwei.",
                "Painted flowers have no scent",
                "Lightning strikes more trees than blades of grass.",
                "Der Nebel, wenn er steigend sich erhält, bringt Regen, doch klar Wetter wenn er fällt.",
                "If twice rotates the weather vane, it's indicating wind and rain",
                "Grauer Morgen - schöner Tag!",
                "Iss, was gar ist. Trink, was klar ist."]

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    Q = QueryEngine.QueryEngine('daily_database.hdf5', 'hourly_database.hdf5')
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
