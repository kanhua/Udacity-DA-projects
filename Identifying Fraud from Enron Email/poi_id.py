#!/usr/bin/python

import sys
import pickle

sys.path.append("../tools/")

import pandas as pd
import numpy as np
import copy
from preprocess_data import FeatureSel,add_features
from sklearn.svm import LinearSVC

from sklearn.preprocessing import StandardScaler
from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
# features_list = ['poi','salary'] # You will need to use more features

features_list = ['poi', 'bonus', 'deferral_payments', 'deferred_income', 'director_fees',
                 'exercised_stock_options', 'expenses', 'from_messages',
                 'from_poi_to_this_person', 'from_this_person_to_poi',
                 'long_term_incentive', 'other', 'restricted_stock',
                 'restricted_stock_deferred', 'salary', 'shared_receipt_with_poi',
                 'to_messages', 'total_payments', 'total_stock_value']

print(len(features_list))

### Load the dictionary containing the dataset
data_dict = pickle.load(open("./data/final_project_dataset.pkl", "r"))


### Task 2: Remove outliers

del data_dict["TOTAL"]
del data_dict["LOCKHART EUGENE E"]


### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict


def add_features(data_dict, financial_features="none"):
    '''
    This function takes separate positive and negative values of financial features,
    and then it takes logarithm of the values of each feature.
    :param financial_features: will be set to default value if it is "none"
    :param data_dict: the data dictionary
    :return: data dictionary with new features, names of new features, names of financial features
    '''

    if financial_features=="none":
        financial_features = ['bonus', 'deferral_payments', 'deferred_income', 'director_fees',
                              'exercised_stock_options', 'expenses',
                              'long_term_incentive', 'other', 'restricted_stock',
                              'restricted_stock_deferred', 'salary',
                              'total_payments', 'total_stock_value']

    new_data_dict = copy.copy(data_dict)

    for name in new_data_dict.keys():
        for f in financial_features:
            if new_data_dict[name][f] == "NaN":
                new_data_dict[name]["p_" + f] = 0
                new_data_dict[name]["n_" + f] = 0
            elif new_data_dict[name][f] >= 0:
                new_data_dict[name]["p_" + f] = np.log10(new_data_dict[name][f])
                new_data_dict[name]["n_" + f] = 0
            elif new_data_dict[name][f] < 0:
                new_data_dict[name]["n_" + f] = np.log10(-new_data_dict[name][f])
                new_data_dict[name]["p_" + f] = 0

    new_feature = []

    for f in financial_features:
        new_feature.append("n_" + f)
        new_feature.append("p_" + f)

    return new_data_dict, new_feature, financial_features


my_dataset, new_feature_names, financial_features = add_features(data_dict)

features_list.extend(new_feature_names)

for f in financial_features:
    del features_list[features_list.index(f)]



### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)

from preprocess_data import linearsvc_outlier_rm

# features,labels,_=linearsvc_outlier_rm(np.array(features),np.array(labels))

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

from sklearn.naive_bayes import GaussianNB

clf = GaussianNB()  # Provided to give you a starting point. Try a varity of classifiers.

sd = StandardScaler()
from sklearn.pipeline import Pipeline

fsl = FeatureSel(k_best=5, pca_comp=5)
# clf=Pipeline([("fsl",fsl),("sd",sd),("lvc",LinearSVC(C=0.000001))])

clf1 = Pipeline([("sd", sd), ("lvc", LinearSVC(C=0.000001, tol=0.0000001))])

from sklearn.grid_search import GridSearchCV

clf = Pipeline([("fsl", fsl), ("sd", sd), ("lvc", LinearSVC())])
gscv = GridSearchCV(clf, {"lvc__C": np.logspace(-6, -1, 10)}, scoring="recall", verbose=0)


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script.
### Because of the small size of the dataset, the script uses stratified
### shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html


test_classifier(gscv, my_dataset, features_list)

### Dump your classifier, dataset, and features_list so 
### anyone can run/check your results.

dump_classifier_and_data(clf, my_dataset, features_list)
