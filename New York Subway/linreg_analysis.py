import pandas
import numpy as np
from linreg import normalize_features,print_theta,plot_indvidual_residuals,plot_residuals_hist
from sklearn.linear_model import Lasso,LinearRegression,RidgeCV,Ridge,SGDRegressor
import matplotlib.pyplot as plt
from sklearn.cross_validation import cross_val_score,KFold

raw_dataframe=pandas.read_csv("./data/improved-dataset/turnstile_weather_v2.csv")
#dataframe=raw_dataframe.loc[raw_dataframe["ENTRIESn_hourly"]<100000,:]
dataframe=raw_dataframe
print(raw_dataframe.shape[0])
print(raw_dataframe.columns)


selected_features=['rain','tempi','fog','pressurei','wspdi', 'meanpressurei', 'meantempi',\
                   'meanwspdi']


features_to_dummy=['hour','conds']


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

plt=plot_indvidual_residuals(predict_array,values_array)
plt.savefig("resplot.png")
plt.show()
plt.close()

plot=plot_residuals_hist(predict_array,values_array)
plt.savefig("resplot_hist.png")
plt.show()
plt.close()


# Run cross validation
kf_total = KFold(dataframe.shape[0], n_folds=5)

a=cross_val_score(la,features_array,values_array,cv=kf_total)

print(a)

print_theta(features.columns,la.coef_)

