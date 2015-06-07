import pandas
import numpy as np
import copy
from linreg import normalize_features
from sklearn.linear_model import Lasso,LinearRegression
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import cross_val_score
dataframe=pandas.read_csv("./improved-dataset/turnstile_weather_v2.csv")


selected_features=['rain','precipi','tempi','fog','pressurei','weekday','wspdi']

features_to_dummy=['hour','UNIT','day_week','conds']

# Select Features (try different features!)
features = dataframe[[f for f in selected_features if f not in features_to_dummy]]

total_dummy_feature_num=0
for fd in features_to_dummy:

    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe[fd], prefix=fd)
    total_dummy_feature_num+=dummy_units.shape[1]
    features = features.join(dummy_units)

print(total_dummy_feature_num)

print(features.columns)
# Values
values = dataframe['ENTRIESn_hourly']
m = len(values)

features, mu, sigma = normalize_features(features)
features['ones'] = np.ones(m) # Add a column of 1s (y intercept)

features_array=np.array(features)
values_array=np.array(values)


la=Lasso(alpha=1)
la.fit(features_array,values_array)
idx=np.argsort(abs(la.coef_))

idx=idx[::-1]

print(features.columns[idx])
print(la.coef_[idx])
print(la.score(features_array,values_array))

a=cross_val_score(la,features_array,values_array,cv=3)

print(a)

