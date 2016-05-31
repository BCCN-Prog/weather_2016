from query_engine import QueryEngine

city_dict = {'berlin': 91}
param_dict = {'high': 3, 'low': 4}

print('Welcome to the command line interface of the weather project')
loc = input('Location: ')
date_time = input('Date (+Time): ')
hourly_daily = input('Hourly or Daily Data?: ')
historical_scraping = input('Historical or Scraping Data?: ')
parameters = input('Which parameters?: ')

qe = QueryEngine()

#loc = city_dict[loc]
#berliparameters = param_dict[parameters]

data = qe.get_data_point(loc, date_time, hourly_daily, historical_scraping, parameters)

print(data)

