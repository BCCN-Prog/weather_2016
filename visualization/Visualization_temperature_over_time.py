
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
get_ipython().magic('matplotlib inline')


# In[2]:

'''This file contains simple functions to plot parameters over time. For the time being
the parameter is considered to be temperature, but could be generalized later on'''


# In[44]:

#create some dummy data
test_date=np.array([1,2,3,4])
test_temp=np.array([10,14,12,2])
test_date_2=np.array([5,8,10,3])


# In[71]:

temp_evol(test_date,test_temp,'time','temp')


# In[70]:

'''This function uses the matplotlib library to plot yvalues in function of xvalues.'''

def temp_evol(xvalues,yvalues,xlabel,ylabel):
    #This function plots datapoints for parameter of interest over time and generates a trendline
    #plot the data points
    fig = plt.figure()
    plt.plot(xvalues,yvalues, linewidth=10.0)
    plt.title('Evolution of {} in function of {}'.format(ylabel,xlabel))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


# In[4]:

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


# In[5]:

temp_evol_1(test_date,test_temp)


# In[23]:

'''This function uses the seaborn statistical visualization library to plot parameters over time. For the time being
the parameter is considered to be temperature, but could be generalized later on'''

def temp_evol_2(time,temperature,ylabel):
    d = {'Time': time, ylabel: temperature}
    df = pd.DataFrame(data=d)
    #sns.lmplot('Time','Temperature',df,fit_reg=True, ci=None)
    sns.lmplot('Time',ylabel,df)
    return


# In[35]:

'''This function uses the seaborn statistical visualization library to plot parameters over time. For the time being
the parameter is considered to be temperature, but could be generalized later on'''

def temp_evol_3(xvalues,yvalues,xlabel,ylabel):
    d = {xlabel: xvalues, ylabel: yvalues}
    df = pd.DataFrame(data=d)
    #sns.lmplot('Time','Temperature',df,fit_reg=True, ci=None)
    sns.lmplot(xlabel,ylabel,df)
    return


# In[36]:




# In[19]:




# In[52]:

t = np.linspace(0,2*np.math.pi,400)
a = np.sin(t)
b = np.cos(t)
c = a + b

plt.plot(t,a,'r') # plotting t,a separately 
plt.plot(t,b,'b') # plotting t,b separately 
plt.plot(t,c,'g') # plotting t,c separately 
plt.show()


# In[ ]:



