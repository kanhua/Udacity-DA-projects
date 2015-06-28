import pandas
import numpy as np
import copy
from linreg import normalize_features,print_theta
from sklearn.linear_model import Lasso,LinearRegression,RidgeCV,Ridge,SGDRegressor
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import cross_val_score,KFold

raw_dataframe=pandas.read_csv("./data/improved-dataset/turnstile_weather_v2.csv")

dataframe=raw_dataframe.loc[raw_dataframe["ENTRIESn_hourly"]<100000,:]

print(raw_dataframe.shape[0])
print(raw_dataframe.columns)
#dataframe=raw_dataframe

selected_features=['rain','tempi','fog','pressurei','wspdi', 'meanpressurei', 'meantempi',\
                   'meanwspdi']

#selected_features=['rain']

features_to_dummy=['hour','conds']

#features_to_dummy=[]

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


#la=RidgeCV(alphas=[0.01,0.1,1,10])

#la=SGDRegressor(loss="squared_loss",alpha=0.1,penalty='l1')
la=LinearRegression()
la.fit(features_array,values_array)
idx=np.argsort(abs(la.coef_))

idx=idx[::-1]

print(features.columns[idx])
print(la.coef_[idx])
print(la.score(features_array,values_array))
print("coefficient of rain:%s"%str(la.coef_[0]))

predict_array=la.predict(features_array)

res=np.power(predict_array-values_array,2)

#plt.semilogy(values_array,res,'.')
r_var=np.var(values_array)
plt.hist(res/r_var,bins=1000)

plt.close()

plt.semilogy(values_array,res/r_var,'.')
plt.xlabel("true values of ENTRIESn_hourly")
plt.ylabel("squared residuals/total variance of the samples")
plt.savefig("resplot.png")

plt.show()
kf_total = KFold(dataframe.shape[0], n_folds=5)

a=cross_val_score(la,features_array,values_array,cv=kf_total)

print(a)

print_theta(features.columns,la.coef_)

