import os
from bs4 import BeautifulSoup
from wrapper.DataWrapH5py import Daily_DataBase, Hourly_DataBase
HOURLY_DB = 'hourly_database.hdf5'
DAILY_DB = 'daily_database.hdf5'
from scraping import test_scraper_output


def get_element_val(div_obj, el_type, class_string):
    return div_obj.findAll(el_type, {"class": class_string})[0].string


def get_sub_element(div_obj, el_type, class_string):
    return div_obj.findAll(el_type, {"class": class_string})


def hourly_sub_dict_from_div(div_obj):
    sub_dict = {}
    temp_div = get_sub_element(div_obj, "div", "forecast-temperature")[0]
    sub_dict['temp'] = float(get_element_val(temp_div, "span", "temperature")[:-1].replace(',', '.'))  # deg C

    rain_div = get_sub_element(div_obj, "div", "forecast-rain")[0]
    rain_span = get_sub_element(rain_div, "span", "wt-font-semibold")
    sub_dict['rain_chance'] = float(rain_span[0].string[:-1].replace(',', '.'))  # %
    if len(rain_span) > 1:
        sub_dict['rain_amt'] = float(rain_span[1].string.split('l')[0].replace(',', '.'))  # l/m^2
    else:
        sub_dict['rain_amt'] = None

    wind_div = get_sub_element(div_obj, "div", "forecast-wind-text")[0]
    wind_speed_string = get_element_val(wind_div, "span", "wt-font-semibold").split(' ')

    # convert km/h to m/h
    km_per_h = float(wind_speed_string[0].split('(')[1].replace(',', '.'))
    m_per_s = km_per_h * 1000 / 60
    if m_per_s > 500:
        m_per_s = 500.0
    sub_dict['wind_speed'] = m_per_s

    hum_div = get_sub_element(div_obj, "div", "forecast-humidity-text")[0]
    sub_dict['humidity'] = float(get_sub_element(hum_div, "span", "wt-font-semibold")[0].string[:-1].replace(',', '.'))  # %
    sub_dict['pressure'] = float(get_sub_element(hum_div, "span", "wt-font-semibold")[1].string.split('h')[0].replace(',', '.'))  # hPa

    return sub_dict


def build_hourly_dict(hourly_results):
    hourly_dict = {}
    hour_class = "forecast-date wt-font-semibold"
    for res_div in hourly_results:
        hour_str = get_element_val(res_div, "div", hour_class).split(':')[0]
        hourly_dict[hour_str] = hourly_sub_dict_from_div(res_div)

    return hourly_dict


def daily_sub_dict_from_div(div_obj):
    sub_dict = {}

    # <div class="text-date">26.04.</div>
    # sub_dict['date'] = get_element_val(div_obj, "div", "text-date")  # 'DD.MM.'

    # <div class="forecast-day-temperature">
        # <span class="wt-color-temperature-max">8°</span> /
        # <span class="wt-color-temperature-min">2°</span>
    # </div>
    sub_dict['high'] = float(get_element_val(div_obj, "span", "wt-color-temperature-max")[:-1])  # deg C
    sub_dict['low'] = float(get_element_val(div_obj, "span", "wt-color-temperature-min")[:-1])  # deg C


    # Get forecasts for every 6 hours
    forecast_columns = get_sub_element(div_obj, "div", "forecast-column")

    max_rain_chance = 0
    rain_amt_sum = 0
    wind_speed_sum = 0

    for col in forecast_columns:
        col_dict = {}
        six_hour_str = get_element_val(col, "div", "forecast-column-date")

        # <div class="forecast-column-rain">
            # <span>Risiko</span>
            # <span class="wt-font-semibold">44%</span><br/>
            # <span class="wt-font-semibold">1,1 l/m²</span>
        # </div>

        rain_div = get_sub_element(col, "div", "forecast-column-rain")[0]
        rain_span = get_sub_element(rain_div, "span", "wt-font-semibold")

        rain_chance_str = rain_span[0].string  # %
        col_dict['rain_chance'] = float(rain_chance_str[:-1].replace(',', '.'))
        if int(rain_chance_str.split('%')[0]) > max_rain_chance:
            max_rain_chance = int(rain_chance_str.split('%')[0])

        if len(rain_span) > 1:
            rain_amt_str = rain_span[1].string.split('l')[0].strip()  # l/m^2
            if rain_amt_str:
                rain_amt = float(rain_amt_str.replace(',', '.'))
                rain_amt_sum += rain_amt
                col_dict['rain_amt'] = rain_amt
        else:
            sub_dict['rain_amt'] = None


        # wind
        # <div class="forecast-wind-text">
        # <span class="wt-font-semibold">(41 km/h)</span>
        # </div>
        wind_div = get_sub_element(div_obj, "div", "forecast-wind-text")[0]
        wind_speed_string = get_element_val(wind_div, "span", "wt-font-semibold").split(' ')

        # convert km/h to m/s
        m_per_s = float(wind_speed_string[0].split('(')[1]) * 1000 / 60
        if m_per_s > 500:
            m_per_s = 500.0
        wind_speed_sum += m_per_s
        col_dict['wind_speed'] = m_per_s

        sub_dict[six_hour_str] = col_dict

    sub_dict['rain_chance'] = float(max_rain_chance)
    sub_dict['rain_amt'] = float(rain_amt_sum)
    sub_dict['wind_speed'] = float(wind_speed_sum / 4)

    return sub_dict


def build_daily_dict(daily_results):
    daily_dict = {}

    for div_num, res_div in enumerate(daily_results):
        daily_dict[str(div_num+1)] = daily_sub_dict_from_div(res_div)


    return daily_dict


def scrape(base_dir, DB_dir):
    IN_DIR = base_dir + 'new/'
    OUT_DIR = base_dir + 'processed/'

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    SITE_ID = 3  # wetter.de site ID

    for html_name in os.listdir(IN_DIR):
        with open(IN_DIR + html_name) as html_fh:
            CITY = html_name.split('_')[-2]
            DATE = int(('').join(html_name.split('_')[-5:-2][::-1]))
            SAMPLE_TYPE = html_name.split('_')[-1].split('.')[0]
            main_dict = {"site": SITE_ID, "city": CITY, "date": DATE, 'daily': {}, 'hourly': {}}

            soup = BeautifulSoup(html_fh, from_encoding='utf-8')

            data_dict = None

            try:
                if SAMPLE_TYPE == 'hourly':
                    hour_forecast = soup.findAll("div", {"class": "column column-4 forecast-detail-column-1h"})
                    data_dict = build_hourly_dict(hour_forecast)

                elif SAMPLE_TYPE == 'daily':
                    days_forecast = soup.findAll("div", {"class": "location-forecast-item"})
                    data_dict = build_daily_dict(days_forecast)
            except:
                print(CITY + SAMPLE_TYPE + ' FAILED')
                continue

            main_dict[SAMPLE_TYPE] = data_dict

            # call Jan's verify function on dict
            assert(test_scraper_output.run_tests(main_dict))

            if SAMPLE_TYPE == 'hourly':
                DB = Hourly_DataBase()
            if SAMPLE_TYPE == 'daily':
                DB = Daily_DataBase()

            DB.save_dict(main_dict)

        # move html to processed folder
        os.rename(IN_DIR + html_name, OUT_DIR + html_name)

if __name__ == '__main__':
    scrape(os.getcwd() + '/output/', os.getcwd() + '/output/')
