# Basic sanity checks, check that data is valid and within normal ranges
import numpy as np
def test_format(some_object):
    """Make sure the data is given as a dictionary"""
    assert(isinstance(some_object, dict))

def test_top_level(data_dic):
    """Test the top level entries of the dictionary"""
    # check for keys
    keys_present = data_dic.keys()
    keys_required = ['site', 'city', 'date', 'daily','hourly']
    sites_possible = ['0', '1', '2', '3', '4']
    cities_possible = ["berlin", "hamburg", "munich", "muenchen",
                "cologne", "frankfurt", "stuttgart",
                "bremen", "leipzig", "hanover", "hannover",
                "nuremberg", "dortmund", "dresden",
                "kassel", "kiel", "bielefeld", "bielfeld",
                "saarbruecken", "rostock", "freiburg",
                "magdeburg", "erfurt", "saarbrucken",
                "münchen", "koeln", "nuernberg",
                "köln", "saarbrücken", "freiburg-im-breisgau"]
    for key in keys_required:
        assert(key in keys_present), "{} is missing".format(key)
    # check for date
    date = data_dic['date']
    assert(isinstance(date, int)), "data_dic['date'] should be int"
    assert(date>20160301 and date<20160731), "date should be yyyymmdd, is: {}".format(date)
    # check for site, this is in integer now
    site = data_dic['site']
    assert(isinstance(site, int)), "data_dic['site'] should be integer, as coded in the wiki"
    assert(str(site) in sites_possible), "'site' should be one of the possible sites"
    # check for city
    city = data_dic['city']
    assert(isinstance(city, str)),  "city name should be string"
    assert(city in cities_possible), "city should be one of possible cities"
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
            # check for required keys
            assert(key in keys_present), "{} is missing".format(key)
        # make sure all values are floats
        for key in keys_required:
            val = day_dic[key]
            if not(np.equal(val, None)):
                #all required values need to be floats
                assert(isinstance(val, float)), '{}:{} is not float'.format(key, val)
        # make sure they are in a plausible range
        high = day_dic['high']
        low = day_dic['low']
        rain_chance = day_dic['rain_chance']
        rain_amt = day_dic['rain_amt']
        # if data is missing (=None) then let the test pass
        if not(np.equal(high, None) or np.equal(low, None)):
            assert(high>=low), "High is lower than low"
        if not(np.equal(low, None)):
            assert(low >-60 and low <60), "Inplausible value for low: {}".format(low)
        if not(np.equal(high, None)):
            assert(high >-60 and high < 60), "Inplausible value for high: {}".format(high)
        if not(np.equal(rain_chance, None)):
            assert(rain_chance>=0 and rain_chance<=100), "Inplausible value for rain_chance: {}".format(rain_chance)
        if not(np.equal(rain_amt, None)):
            assert(rain_amt>=0 and rain_amt<1000), "Inplausible value for rain_amt: {}".format(rain_amt)

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
            assert(key in keys_present), "{} is missing".format(key)
        # make sure all required values are floats
        for key in keys_required:
            val = hour_dic[key]
            if not(np.equal(val, None)):
                #all required values need to be floats
                assert(isinstance(val, float)), '{}:{} is not float'.format(key, val)
        # make sure they are in a plausible range, ignore None as missing data
        temp = hour_dic['temp']
        if not(np.equal(temp, None)):
            assert(temp >-60 and temp < 60), "Inplausible value for temp: {}".format(temp)
        rain_amt = hour_dic['rain_amt']
        if not(np.equal(rain_amt, None)):
            assert(rain_amt>=0 and rain_amt<1000), "Inplausible value for rain_amt: {}".format(rain_amt)
        rain_chance = hour_dic['rain_chance']
        if not(np.equal(rain_chance, None)):
            assert(rain_chance>=0 and rain_chance<=100), "Inplausible value for rain_chance: {}".format(rain_chance)
        wind_speed = hour_dic['wind_speed']
        if not(np.equal(wind_speed, None)):
            assert(wind_speed>=0 and wind_speed<=500), "Inplausible value for wind_speed: {}".format(wind_speed)
        humidity = hour_dic['humidity']
        if not(np.equal(humidity, None)):
            assert(humidity>=0 and humidity<=100), "Inplausible value for humidity: {}".format(humidity)

def run_tests(data_dic):
    """Runs the above tests. Return true if all tests pass"""
    test_format(data_dic)
    test_top_level(data_dic)
    test_daily(data_dic)
    test_hourly(data_dic)
    return True
