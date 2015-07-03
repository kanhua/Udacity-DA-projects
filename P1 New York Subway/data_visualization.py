import numpy as np
import pandas
import matplotlib.pyplot as plt

def entries_histogram(turnstile_weather):
    '''
    Before we perform any analysis, it might be useful to take a
    look at the data we're hoping to analyze. More specifically, let's
    examine the hourly entries in our NYC subway data and determine what
    distribution the data follows. This data is stored in a dataframe
    called turnstile_weather under the ['ENTRIESn_hourly'] column.

    Let's plot two histograms on the same axes to show hourly
    entries when raining vs. when not raining. Here's an example on how
    to plot histograms with pandas and matplotlib:
    turnstile_weather['column_to_graph'].hist()

    Your histograph may look similar to bar graph in the instructor notes below.

    You can read a bit about using matplotlib and pandas to plot histograms here:
    http://pandas.pydata.org/pandas-docs/stable/visualization.html#histograms

    You can see the information contained within the turnstile weather data here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''

    plt.figure()
    turnstile_weather['ENTRIESn_hourly'][turnstile_weather["rain"]==0]
    turnstile_weather['ENTRIESn_hourly'][(turnstile_weather.rain==1) & (turnstile_weather.rain==1)].hist()
    rain_data=turnstile_weather.loc[turnstile_weather["rain"]==1,:]
    no_rain_data=turnstile_weather.loc[turnstile_weather["rain"]==0,:]

    print(rain_data.shape[0])
    print(no_rain_data.shape[0])

    rain_data["ENTRIESn_hourly"].hist(alpha=0.5,bins=2500,normed=True)
    print("max rain:%s"%str(max(rain_data["ENTRIESn_hourly"])))
    no_rain_data["ENTRIESn_hourly"].hist(alpha=0.5,bins=2500,normed=True)
    print("max no rain:%s"%str(max(no_rain_data["ENTRIESn_hourly"])))
    #plt.ylim([0,1000])
    plt.xlim([0,2000])
    plt.xlabel("ENTRIESn_hourly")
    plt.ylabel("frequency")
    plt.legend(["rainy days","non-rainy days"])
    plt.savefig("./entries_hist2.png")
    plt.show()
    return plt


data=pandas.read_csv("./data/turnstile_data_master_with_weather.csv")
entries_histogram(data)