
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import pandas as pd
import time
#get_ipython().magic('matplotlib inline')


# In[2]:

'''This file contains simple functions to plot parameters over time. For the time being
the parameter is considered to be temperature, but could be generalized later on'''


# In[44]:

#create some dummy data
test_date=np.array([19990101, 19990102, 19990103, 19990104])
test_temp=np.array([10,14,12,2])
test_date_2=np.array([5,8,10,3])



'''This function uses the matplotlib library to plot yvalues in function of xvalues.'''

def temp_evol(xvalues,yvalues,xlabel,ylabel):
    #This function plots datapoints for parameter of interest over time and generates a trendline
    #plot the data points
    fig = plt.figure()
    plt.plot(yvalues, linewidth=3.0)
    #a = time.strptime("19000101", "%Y%m%d")
    if xlabel == 'date':
        xlabels = [time.strptime("{}".format(i), "%Y%m%d") for i in xvalues]

    plt.xticks([])
    plt.title('Evolution of {} in function of {}'.format(ylabel,xlabel))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

temp_evol(test_date,test_temp,'time','temp')

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





