from wit import Wit
import os
from random import shuffle

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

def merge(session_id, context, entities, msg):
    if 'joke' in context:
        del context['joke']
    category = first_entity_value(entities, 'category')
    if category:
        context['cat'] = category
    sentiment = first_entity_value(entities, 'sentiment')
    if sentiment:
        context['ack'] = 'Glad you liked it. ' if sentiment == 'positive' else 'Hmm.'
    elif 'ack' in context:
        del context['ack']
    loc = first_entity_value(entities, 'location')
    if loc:
        context['loc'] = loc
    return context

def select_joke(session_id, context):
    try:
        jokes = all_jokes[context['cat']]
    except KeyError:
        jokes = all_jokes['default']
    shuffle(jokes)
    context['joke'] = jokes[0]
    return context

def error(session_id, context, e):
    print(str(e))

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
}

actions = {
    'say': say,
    'merge': merge,
    'error': error,
    'select-joke': select_joke,
}

client = Wit(os.environ.get('WIT_TOKEN'), actions)
session_id = 'my-user-id-42'
