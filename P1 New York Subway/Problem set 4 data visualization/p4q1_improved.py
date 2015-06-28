__author__ = 'kanhua'

from pandas import *
from ggplot import *

def plot_weather_data(turnstile_weather):
    '''
    You are passed in a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.
    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
     * How ridership varies based on Subway station (UNIT)
     * Which stations have more exits or entries at different times of day
       (You can use UNIT as a proxy for subway station.)

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

    To see all the columns and data points included in the turnstile_weather
    dataframe.

    However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''

    #plot = # your code here

    assert isinstance(turnstile_weather,DataFrame)
    print(turnstile_weather.columns)


    weather_data=turnstile_weather[['hour','ENTRIESn_hourly','EXITSn_hourly','weekday']]


    print(weather_data)

    grouped=weather_data.groupby(['hour','weekday'],as_index=False)
    summed_entries=grouped.sum()
    print(summed_entries)
    #hour_data=summed_entries.index
    #summed_entries['hour']=hour_data
    print(summed_entries.columns)

    #summed_entries['ENTRIESn_hourly']=summed_entries['ENTRIESn_hourly']/1e6
    plot=ggplot(summed_entries,aes(x='hour',y='ENTRIESn_hourly',fill="weekday"))+\
         geom_bar(stat='identity',position="dodge")+scale_x_discrete()+\
         xlab("Hour of day")+ylab("total ENTRIESn_hourly")


    return plot



weather_data=read_csv("../data/improved-dataset/turnstile_weather_v2.csv")
#weather_data=weather_data.loc[weather_data["ENTRIESn_hourly"]<2000,:]

p=plot_weather_data(weather_data)

print(p)
