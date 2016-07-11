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
