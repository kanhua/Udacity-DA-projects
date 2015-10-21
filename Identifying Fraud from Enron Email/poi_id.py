#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data
import pandas as pd
import numpy as np
import copy


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
#features_list = ['poi','salary'] # You will need to use more features

features_list=['poi','bonus', 'deferred_income', 'director_fees', 'exercised_stock_options',
               'expenses', 'from_messages', 'from_poi_to_this_person',
               'from_this_person_to_poi', 'long_term_incentive', 'other',
               'restricted_stock', 'salary', 'shared_receipt_with_poi', 'to_messages',
               'total_payments', 'total_stock_value','deferral_payments','restricted_stock_deferred']

### Load the dictionary containing the dataset
data_dict = pickle.load(open("./data/final_project_dataset.pkl", "r") )

df=pd.DataFrame(data_dict)
df=df.transpose()

### Task 2: Remove outliers
df=df.drop("LOCKHART EUGENE E",axis=0)
df=df.drop("TOTAL",axis=0)


del data_dict["TOTAL"]
del data_dict["LOCKHART EUGENE E"]


### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict

new_feature=[]

financial_features=['bonus', 'deferral_payments', 'deferred_income', 'director_fees',
                    'exercised_stock_options', 'expenses',
                    'long_term_incentive', 'other', 'restricted_stock',
                    'restricted_stock_deferred', 'salary',
                    'total_payments', 'total_stock_value']

for f in financial_features:
    new_feature.append("n_"+f)
    new_feature.append("p_"+f)



def add_features(data_dict):

    sf2_df=copy.copy(data_dict)

    new_financial_features=[]

    for name in sf2_df.keys():
        for f in financial_features:
            if sf2_df[name][f]=="NaN":
                sf2_df[name]["p_"+f]=0
                sf2_df[name]["n_"+f]=0
            elif sf2_df[name][f]>=0:
                sf2_df[name]["p_"+f]=np.log10(sf2_df[name][f])
                sf2_df[name]["n_"+f]=0
            elif sf2_df[name][f]<0:
                sf2_df[name]["n_"+f]=np.log10(-sf2_df[name][f])
                sf2_df[name]["p_"+f]=0


    return sf2_df



features_list.extend(new_feature)

for f in financial_features:
    del features_list[features_list.index(f)]

my_dataset=add_features(data_dict)





### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

from preprocess_data import linearsvc_outlier_rm

features,labels,_=linearsvc_outlier_rm(np.array(features),np.array(labels))

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()    # Provided to give you a starting point. Try a varity of classifiers.

from preprocess_data import FeatureSel
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
sd=StandardScaler()
from sklearn.pipeline import Pipeline
fsl=FeatureSel(k_best=10,pca_comp=10)
clf=Pipeline([("fsl",fsl),("sd",sd),("lvc",LinearSVC(C=0.000001,tol=0.0000001))])

clf1=Pipeline([("sd",sd),("lvc",LinearSVC(C=0.000001,tol=0.0000001))])

from sklearn.grid_search import GridSearchCV

gscv=GridSearchCV(clf,{"lvc__C":np.logspace(-6,-1,10)},scoring="f1",verbose=0)



### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html



test_classifier(clf1, my_dataset, features_list)

### Dump your classifier, dataset, and features_list so 
### anyone can run/check your results.

dump_classifier_and_data(clf, my_dataset, features_list)