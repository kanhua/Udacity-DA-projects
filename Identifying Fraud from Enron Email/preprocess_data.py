__author__ = 'kanhua'


import pickle
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin,TransformerMixin
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectKBest
from sklearn.decomposition import PCA
import numpy as np
from sklearn.preprocessing import scale

def pkl_to_df(pkl_file="./data/final_project_dataset.pkl",remove_total=False):

    data_dict=pickle.load(open(pkl_file,"rb"),fix_imports=False,encoding="latin1")

    df=pd.DataFrame(data_dict)
    df=df.transpose()

    if remove_total==True:
        df=df.drop("TOTAL",axis=0)

    return df

def extract_df(df,exclude_features=["email_address","poi"]):
    """
    :param df: input dataframe
    :param exclude_features: list of feature names to be removed
    :return: a tuple of X,y
    """


    ndf=df.drop(exclude_features,axis=1)
    X=ndf.values

    y=df["poi"].values

    print(ndf.columns)

    return X,y

def linearsvc_outlier_rm(train_X,train_y,discard=0.1,lvc_C=0.1,take_abs=True):
    """
    Remove the outliers in the data.
    It rescaled the data, use linear SVC to do the classification,
    and then remove the data with farthest distances
    :param train_X: train data
    :param train_y: label
    :param discard: the ratio of the outliers to be removed
    :return: tuple of new X,y
    """

    assert isinstance(train_X,np.ndarray)
    assert isinstance(train_y,np.ndarray)

    # LinearSVC requires the features to be scaled
    # Here we scaled the input data, but the output data are note rescaled
    scaled_train_X=scale(train_X)

    lvc=LinearSVC(C=lvc_C)
    lvc.fit(scaled_train_X,train_y)

    dec_y=lvc.decision_function(scaled_train_X)

    #choose the smallest 90%
    num_sel=int(len(dec_y)*(1-discard))
    assert len(dec_y)==scaled_train_X.shape[0]
    assert num_sel<=scaled_train_X.shape[0]

    if take_abs==True:
        s_idx=np.argsort(np.abs(dec_y))
    else:
        s_idx=np.argsort(dec_y)

    assert len(s_idx)==scaled_train_X.shape[0]


    n_train_X=train_X[s_idx[0:num_sel],:]
    n_train_y=train_y[s_idx[0:num_sel]]

    return n_train_X,n_train_y,dec_y


class FeatureSel(BaseEstimator,TransformerMixin):
    def __init__(self,k_best=5,pca_comp=8):
        self.k_best=k_best
        self.pca_comp=pca_comp
        self.pca=PCA(n_components=self.pca_comp)
        self.skb=SelectKBest(k=self.k_best)


    def transform(self,X):
        X1=self.pca.transform(X)
        X2=self.skb.transform(X)

        return np.hstack((X1,X2))


    def fit_transform(self,X,y):
        X1=self.pca.fit_transform(X,y)
        X2=self.skb.fit_transform(X,y)

        return np.hstack((X1,X2))

    def fit(self,X,y):
        self.pca.fit(X,y)
        self.skb.fit(X,y)






if __name__=="__main__":
    df=pkl_to_df(remove_total=False)
    X,y=extract_df(df)


    from sklearn.preprocessing import Imputer
    import matplotlib.pyplot as plt

    imp=Imputer(axis=0,strategy="median")
    X=imp.fit_transform(X)

    X,y,y_dis=linearsvc_outlier_rm(X,y)
    print(y_dis)
    plt.hist(y_dis,100,hold=True)


    X,y,y_dis=linearsvc_outlier_rm(X,y)
    print(y_dis)
    plt.hist(y_dis,100)


    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    sd=StandardScaler()
    fsl=FeatureSel()
    ppl=Pipeline([("fsl",fsl),("sd",sd),("lvc",LinearSVC(C=0.0001,tol=0.0001))])

    ppl.fit(X,y)

    ppl.predict(X)







