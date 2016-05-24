# Basic sanity checks, check that data is valid and within normal ranges
def test_format(some_object):
    """Make sure the data is given as a dictionary"""
    assert(isinstance(some_object, dict))

def test_top_level(data_dic):
    """Test the top level entries of the dictionary"""
    # check for keys
    keys_present = data_dic.keys()
    keys_required = ['site', 'city', 'date', 'daily','hourly']
    sites_possible = ["wetter.com"]
    cities_possible = ["berlin", "hamburg", "muenchen",
                "koeln", "frankfurt", "stuttgart",
                "bremen", "leipzig", "hannover",
                "nuernberg", "dortmund", "dresden",
                "kassel", "kiel", "bielefeld",
                "saarbruecken", "rostock", "freiburg",
                "magdeburg", "erfurt"]
    for key in keys_required:
        assert(key in keys_present)
    # check for date
    date = data_dic['date']
    assert(isinstance(date, int)) # date should be int
    assert(date>10000000 and date<32000000)    # date should be ddmmyyyy
    # check for site
    site = data_dic['site']
    assert(isinstance(site, str)) # site should be string
    assert(site in sites_possible) # site should be one of the sites
    # check for city
    city = data_dic['city']
    assert(isinstance(city, str)) # site should be string
    assert(city in cities_possible) # site should be one of the cities
    # check hourly and daily to be dicts
    test_format(data_dic['daily'])
    test_format(data_dic['hourly'])

def test_daily(data_dic):
    """Test the dictionary holding the daily data"""
    daily_dic = data_dic['daily']
    # get all the values
    days_dics = daily_dic.values()
    keys_required = ['high', 'low', 'rain_chance', 'rain_amt']

    # for every day
    for day_dic in days_dics:
        # day should be a dict again
        test_format(day_dic)
        keys_present = day_dic.keys()
        # make sure all keys are present
        for key in keys_required:
            assert(key in keys_present)
        # make sure all values are floats
        for val in day_dic.values():
            assert(isinstance(val, float))
        # make sure they are in a plausible range
        high = day_dic['high']
        low = day_dic['low']
        assert(high>=low)
        assert(high >-60 and high < 60)
        assert(low >-60 and low <60)
        rain_amt = day_dic['rain_amt']
        assert(rain_amt>=0 and rain_amt<1000)
        rain_chance = day_dic['rain_chance']
        assert(rain_chance>=0 and rain_chance<=100)

def test_hourly(data_dic):
    """Test the dictionary holding the hourly data"""
    hourly_dic = data_dic['hourly']
    hours_dics = hourly_dic.values()
    keys_required = ['temp', 'wind_speed', 'rain_chance', 'rain_amt', 'humidity']
    # for every hour
    for hour_dic in hours_dics:
        # day should be a dict again
        test_format(hour_dic)
        keys_present = hour_dic.keys()
        # make sure all keys are present
        for key in keys_required:
            assert(key in keys_present)
        # make sure all required values are floats
        for key in keys_required:
            assert(isinstance(hour_dic[key], float))
        # make sure they are in a plausible range
        temp = hour_dic['temp']
        assert(temp >-60 and temp < 60)
        rain_amt = hour_dic['rain_amt']
        assert(rain_amt>=0 and rain_amt<1000)
        rain_chance = hour_dic['rain_chance']
        assert(rain_chance>=0 and rain_chance<=100)
        wind_speed = hour_dic['wind_speed']
        assert(wind_speed>=0 and wind_speed<500)
        humidity = hour_dic['humidity']
        assert(humidity>=0 and humidity<=100)

def run_tests(data_dic):
    """Runs the above tests. Return true if all tests pass"""
    test_format(data_dic)
    test_top_level(data_dic)
    test_daily(data_dic)
    test_hourly(data_dic)
    return True
