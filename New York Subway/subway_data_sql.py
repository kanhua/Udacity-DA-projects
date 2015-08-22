__author__ = 'kanhua'

import pandas
import pandasql


subway_data = pandas.read_csv("turnstile_data_master_with_weather.csv")
subway_data.rename(columns = lambda x: x.replace(' ', '_').lower(), inplace=True)
print(subway_data.columns.values)


q="""SELECT timen FROM subway_data GROUP BY thunder;"""
result=pandasql.sqldf(q, globals())

print(result)