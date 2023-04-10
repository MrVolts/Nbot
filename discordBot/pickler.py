import os
import pickle
#general use module for saving and loading data
def save(data,filename=None,defaultpath = "/persistantData/"):
    with open("."+defaultpath+filename, "wb") as f:
        pickle.dump(data, f)

def load(filename,defaultpath = "/persistantData/"):
    with open("."+defaultpath+filename, "rb") as f:
        return pickle.load(f)


def listnames():
    return os.listdir("./persistantData")#w