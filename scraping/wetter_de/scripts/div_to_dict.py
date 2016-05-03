import os
from bs4 import BeautifulSoup
import pudb

def get_element_val(div_obj, el_type, class_string):
    return div_obj.findAll(el_type, {"class": class_string})[0].string

def get_sub_element(div_obj, el_type, class_string):
    return div_obj.findAll(el_type, {"class": class_string})


def hourly_sub_dict_from_div(div_obj):
    sub_dict = {}
    temp_div = get_sub_element(div_obj, "div", "forecast-temperature")[0]
    sub_dict['temp'] = get_element_val(temp_div, "span", "temperature")  # deg C

    rain_div = get_sub_element(div_obj, "div", "forecast-rain")[0]
    rain_span = get_sub_element(rain_div, "span", "wt-font-semibold")
    sub_dict['rain_chance'] = rain_span[0].string  # l/m^2
    if len(rain_span) > 1:
        sub_dict['rain_amt'] = rain_span[1].string  # %

    wind_div = get_sub_element(div_obj, "div", "forecast-wind-text")[0]
    # @TODO: convert from km/h to m/s
    sub_dict['wind_speed'] = get_element_val(wind_div, "span", "wt-font-semibold")

    hum_div = get_sub_element(div_obj, "div", "forecast-humidity-text")[0]
    sub_dict['humidity'] = get_sub_element(hum_div, "span", "wt-font-semibold")[0].string  # %
    sub_dict['pressure'] = get_sub_element(hum_div, "span", "wt-font-semibold")[1].string  # hPa

    return sub_dict


def build_hourly_dict(hourly_results):
    pu.db
    hourly_dict = {}
    hour_class = "forecast-date wt-font-semibold"
    for res_div in hourly_results:
        hourly_dict[get_element_val(res_div, "div", hour_class)] = hourly_sub_dict_from_div(res_div)

    return hourly_dict

def build_daily_dict(daily_results):
    return daily_results

def div_to_dict(base_dir):
    IN_DIR = base_dir + '/output/new'
    # OUT_DIR = base_dir + '/output/processed'
    SITE = 'wetter_de'


    for html_name in os.listdir(IN_DIR):
        with open(IN_DIR + '/' + html_name) as html_fh:
            CITY = html_name.split('_')[-2]
            DATE = ('_').join(html_name.split('_')[-5:-2])
            SAMPLE_TYPE = html_name.split('_')[-1].split('.')[0]
            main_dict = {"site": SITE, "city": CITY, "date": DATE}

            soup = BeautifulSoup(html_fh, from_encoding='utf-8')

            data_dict = None

            if SAMPLE_TYPE == 'hourly':
                hour_forecast = soup.findAll("div", {"class": "column column-4 forecast-detail-column-1h"})
                data_dict = build_hourly_dict(hour_forecast)

            elif SAMPLE_TYPE == 'daily':
                days_forecast = soup.findAll("div", {"class": "forecast-item-day"})
                data_dict = build_daily_dict(days_forecast)

            main_dict[SAMPLE_TYPE] = data_dict


    # @TODO: move html to processed folder



if __name__ == '__main__':
    div_to_dict(os.getcwd())
