import pandas
import numpy as np
import copy
from linreg import normalize_features
from sklearn.linear_model import Lasso,LinearRegression
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import cross_val_score, KFold
dataframe=pandas.read_csv("./data/improved-dataset/turnstile_weather_v2.csv")


selected_features=['rain','precipi','tempi','fog','pressurei','weekday','wspdi']

features_to_dummy=['hour','day_week','conds']

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

def linearReg():
    sl=Lasso(alpha=0.2)

    sl.fit(features_array,values_array)

    predict_val=sl.predict(features_array)

    print(sl.coef_)
    print(sl.score(features_array,values_array))

    fig = plt.figure()
    ax = plt.subplot(111)
    ax.bar(range(0,features.shape[1]),sl.coef_)
    plt.show()


def randomfreg():
    rf=RandomForestRegressor()
    rf.fit(features_array,values_array)
    print(rf.score(features_array,values_array))


#a=cross_val_score(Lasso(alpha=0.5),features_array,values_array,cv=5)
#print(a)

def easy_linear_reg(X,y):
    lr=LinearRegression()
    lr.fit(X,y)
    s=lr.score(X,y)

    return s


def forward_selection(X,y,zrange):

    assert isinstance(X,np.ndarray)
    X_size=zrange

    Mp=[list(range(X_size,X.shape[1])) for i in range(X_size)]

    Mp_rsq=[]

    for i in range(X_size):
        print(i)
        Rsq=-10000
        best_index=-1
        for j in range(X_size):
            if j not in Mp[i]:

                colindex=copy.copy(Mp[i])
                colindex.append(j)
                print(colindex)
                newX=X[:,colindex]
                r=easy_linear_reg(newX,y)
                print(r)
                if r>Rsq:
                    Rsq=r
                    best_index=j
        Mp_rsq.append(Rsq)
        for ki in range(i,X_size,1):
            Mp[ki].append(best_index)

    return Mp,Mp_rsq


m,r=forward_selection(features_array,values_array,len(selected_features))

fp=open("linreg_out.txt",'w')

for i, mp in enumerate(m):
    fp.write(str(r[i]))

    for mmp in mp:
        if mmp<len(selected_features):
            fp.write(",")
            fp.write(features.columns[mmp])
    fp.write("\n")

fp.close()


max_idx=r.index(max(r))
print(max(r))


# Retrieve the non-dummy feature index
ndfeatures=[]
ndfeatures_map=[]

for i,mk in enumerate(m[max_idx]):
    if mk<len(selected_features):
        ndfeatures.append(mk)
        ndfeatures_map.append(i)


lr=LinearRegression()
lr.fit(features_array[:,m[max_idx]],values_array)
print(m[max_idx])
print(features_array.columns[m[max_idx]])
print(lr.coef_)
bar_width=0.3
fig, ax = plt.subplots()
rects1 = ax.barh(range(len(ndfeatures)),lr.coef_[ndfeatures_map],bar_width)
ax.set_yticks(np.array(range(len(ndfeatures)))+bar_width/2)
ax.set_yticklabels(features.columns[ndfeatures])
ax.set_xlabel("theta")
plt.grid()
plt.savefig("theta.png")
plt.show()

plt.close()

kf_total = KFold(dataframe.shape[0], n_folds=10, random_state=4)

a=cross_val_score(lr,features_array[:,m[max_idx]],values_array,cv=kf_total)

print("corss validation scores:")
print(a)


predict_array=lr.predict(features_array[:,m[max_idx]])

res=np.power(predict_array-values_array,2)

r_var=np.var(values_array)
plt.semilogy(values_array,res/r_var,'.')

plt.xlabel("true values of ENTRIESn_hourly")
plt.ylabel("squared residuals/total variance of the samples")

plt.savefig("resplot.png")


for i,fid in enumerate(ndfeatures):
    print("|"+features.columns[fid]+"|"+str(lr.coef_[ndfeatures_map[i]])+"|")


