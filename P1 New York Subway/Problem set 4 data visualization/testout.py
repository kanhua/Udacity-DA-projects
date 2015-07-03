import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('../data/improved-dataset/turnstile_weather_v2.csv')

df['count']=0
w=df.groupby(['weekday','rain'],as_index=False)
w=w.count().loc[:,['weekday','rain','count']]

Rain=w['count'][w.rain==1]
NoRain=w['count'][w.rain==0]

group_labels = ['Weekend','Weekday']
num_items = len(group_labels)
ind = np.arange(num_items)
width = 0.5

p1=plt.bar(ind,NoRain,width,color='g',align='center')
p2=plt.bar(ind,Rain,width,color='b',align='center',bottom = NoRain,)


plt.ylabel('ENTRIESn')
plt.title('Ridership by DayType and Weather')
#plt.legend( (p1[0], p2[0]), ('NoRain', 'Rain') ,loc="best")
plt.legend(['NoRain','Rain'],loc="best")
plt.xticks(ind, group_labels)

print(p1[0])
plt.show()