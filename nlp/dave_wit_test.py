import sys
from wit import Wit

# Quickstart example
# See https://wit.ai/l5t/Quickstart

if len(sys.argv) != 2:
    print("usage: python examples/quickstart.py <wit-token>")
    exit(1)
access_token = sys.argv[1]

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    #loc = entities[entity][0]['location']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def say(session_id, context, msg):
    print(msg)

def merge(session_id, context, entities, msg):
    loc = first_entity_value(entities, 'location')
    if loc:
        context['loc'] = loc
    return context

def error(session_id, context, e):
    print(str(e))

def fetch_weather(session_id, context):
    context['forecast'] = 'sunny'
    return context

def zero_context(session_id, context):
    context = {}
    return context

def dave_here(session_id, context):
    say(session_id, context, 'Reached dave_here()')

actions = {
    'say': say,
    'merge': merge,
    'error': error,
    'fetch-weather': fetch_weather,
    'zero_context': zero_context,
    'dave_here': dave_here,
}

client = Wit(access_token, actions)

session_id = 'my-user-session-42'
context0 = {}
context1 = client.run_actions(session_id, 'what is the weather in London?', context0)
print('The session state is now: ' + str(context1))
context2 = client.run_actions(session_id, 'and in Brussels?', context1)
print('The session state is now: ' + str(context2))

#client.interactive()
