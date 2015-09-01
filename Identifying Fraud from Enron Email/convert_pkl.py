__author__ = 'kanhua'


import pickle

data_dict = pickle.load(open("./data/final_project_dataset.pkl", "r") )

pickle.dump(data_dict,open("./data/final_project_dataset_3.pkl","w"))
