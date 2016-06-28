
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import pandas as pd
import datetime
#get_ipython().magic('matplotlib inline')


'''This file contains simple functions to plot parameters over time. For the time being
the parameter is considered to be temperature, but could be generalized later on'''


#create some dummy data
test_date=np.array([19990101, 19990102, 19990103, 19990104])
test_temp=np.array([10,14,12,2])



def gen_daily_ticks(sorted_xvalues):
    #dates = [time.strptime("{}".format(i), "%Y%m%d") for i in xvalues]
    dates = [datetime.date(int(i[:4]), int(i[4:6]), int(i[6:8])) for i in str(sorted_xvalues)]
    last_date = dates[-1]
    first_date = dates[0]
    time_span = last_date - first_date
    if time_span.days < 30:
        xticks = [str(d.day) for d in dates]
        title_year = [last_date.year] if last_date.year == first_date.year else [first_date.year, last_date.year]
        title_month = [last_date.month] if last_date.month == first_date.month else [first_date.month, last_date.month]
        title_part = [title_month,title_year]
    elif time_span.days < 366:
        xticks = []  # string with month and year
    else:
        xticks = [] # month and year
    return xticks, title_part
def gen_hourly_ticks(xvalues):
    pass

def gen_x_ticks(xvalues, daily = True):
    #a = time.strptime("19000101", "%Y%m%d")
    if daily:
        return gen_daily_ticks(xvalues)
    else:
        return gen_hourly_ticks(xvalues)

def temp_evol(xvalues,yvalues,xlabel,ylabel):
    #This function plots datapoints for parameter of interest over time and generates a trendline
    #plot the data points

    #sorting wrt. time
    xvalues = xvalues.sort(axis =0)
    print(xvalues)

    #plt.plot(yvalues, linewidth=3.0)


    #if xlabels[0].tm_year == xlabels[1].tm_year and xlabels[0].tm_year == xlabels[2].tm_year:
    #    if xlabels[0].tm_month == xlabels[1].tm_month and xlabels[0].tm_year == xlabels[2].tm_year:
    #        if xlabels[0].tm_day == xlabels[1].tm_day:

    plt.xticks([])
    plt.title('Evolution of {} in function of {}'.format(ylabel,xlabel))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

#temp_evol(test_date,test_temp,'time','temp')

'''This function uses the matplotlib library to plot parameters over time and includes a trendline. For the time being
the parameter is considered to be temperature, but could be generalized later on'''

def temp_evol_1(time,parameter):
    #This function plots datapoints for parameter of interest over time and generates a trendline
    
    #plot the data points
    fig = plt.figure()
    plt.scatter(time,parameter)
    plt.title('Evolution of temperature over time')
    plt.xlabel('Time (Years)')
    plt.ylabel('Temperature(°C)')
    
    #plot trendline with printed trendline function
    m,b=np.polyfit(time,parameter,1)
    plt.plot(time, m*time + b, label="y={:.2f}x+{:.2f}".format(m, b))
    plt.legend(loc='best')
    plt.show() 
    return


#temp_evol_1(test_date,test_temp)


'''This function uses the seaborn statistical visualization library to plot parameters over time. For the time being
the parameter is considered to be temperature, but could be generalized later on'''

def temp_evol_2(time,temperature,ylabel):
    d = {'Time': time, ylabel: temperature}
    df = pd.DataFrame(data=d)
    #sns.lmplot('Time','Temperature',df,fit_reg=True, ci=None)
    sns.lmplot('Time',ylabel,df)
    return





