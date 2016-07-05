import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime
# import pudb


'''This file contains simple functions to plot parameters over time.'''

def plot_over_time(data_mat, daily_data, ylabel):

    label_dict = {'temp': 'Temperature [°C]', 'humidity': 'Humidity [%]',
                  'pressure': 'Pressure [hPa]', 'wind_speed': 'Wind Speed [m/s]',
                  'rain_amt': 'Rain Amount [l/m²]', 'rain_chance': 'Rain Chance [%]',
                  'cloud_cover': 'Cloud Cover [%]'}

    sort_mat = data_mat[data_mat[:, 0].argsort()]
    time_vals = sort_mat[:, 0]
    y_vals = sort_mat[:, 1]

    if daily_data:
        date_objs = [datetime.date(int(str(i)[:4]), int(str(i)[4:6]), int(str(i)[6:8])) for i in time_vals]
    else:  # hourly
        date_objs = [datetime.datetime(int(str(i)[:4]), int(str(i)[4:6]), int(str(i)[6:8]), int(str(i)[8:10])) for i in time_vals]

    temp_pt = dates.date2num(date_objs)
    fig, ax = plt.subplots()
    ax.plot_date(temp_pt, y_vals, '-')
    ax.autoscale_view()
    fig.autofmt_xdate()
    dtype_str = 'Daily' if daily_data else 'Hourly'
    plt.title('{} {} Over Time'.format(dtype_str, label_dict[ylabel]))
    plt.ylabel(label_dict[ylabel])
    plt.show()




if __name__ == '__main__':
    # pu.db  # @XXX
    # create some dummy data
    test_dates = np.arange(19990101, 19990117, 1)

    test_times = np.array([1999010101, 1999010102, 1999010103, 1999010104, 1999010105,
                           1999010106, 1999010107, 1999010108, 1999010109, 1999010110, 1999010111,
                           1999010112, 1999010113, 1999010114, 1999010115, 1999010116, 1999010117,
                           1999010118, 1999010119, 1999010120, 1999010121, 1999010122, 1999010123, 1999010200])

    test_temp = np.random.uniform(low=-10, high=40, size=len(test_dates))
    test_temp2 = np.random.uniform(low=-10, high=40, size=24)

    test_input = np.vstack((test_dates, test_temp)).T
    test_input2 = np.vstack((test_times, test_temp2)).T


    plot_over_time(test_input, True, 'temp')
    plot_over_time(test_input2, False, 'temp')
