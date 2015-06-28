import pandas
import numpy as np
from sklearn.cross_validation import cross_val_score,KFold
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import f1_score

raw_dataframe=pandas.read_csv("./data/improved-dataset/turnstile_weather_v2.csv")

dataframe=raw_dataframe.loc[raw_dataframe["ENTRIESn_hourly"]<1000,:]

print(raw_dataframe.shape[0])
print(raw_dataframe.columns)
#dataframe=raw_dataframe

selected_features=['tempi','pressurei','wspdi','precipi','fog','weekday']

#selected_features=['fog']
#selected_features=['rain']

features_to_dummy=['hour']

#features_to_dummy=[]

# Select Features (try different features!)
features = dataframe[[f for f in selected_features if f not in features_to_dummy]]

total_dummy_feature_num=0
for fd in features_to_dummy:

    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe[fd], prefix=fd)
    total_dummy_feature_num+=dummy_units.shape[1]
    features = features.join(dummy_units)


values = dataframe['rain']


features_array=np.array(features)
values_array=np.array(values)


rf=RandomForestClassifier()


rf.fit(features_array,values_array)


for i,r in enumerate(rf.feature_importances_):
    print(features.columns[i]+":"+str(r))

cs=cross_val_score(RandomForestClassifier(), features_array,values_array,cv=5,scoring='f1')
print(cs)


