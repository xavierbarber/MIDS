# -*- coding: utf-8 -*-


###############################################################################
# Imports
###############################################################################
import pickle as pickle


###############################################################################
# Functions
###############################################################################

## This function allow the user to load any object python into the programme
def load_pickle(name):
    #print(name)
    with open(name, 'rb') as handle:
        unserialized_data = pickle.load(handle)
    return unserialized_data

## This function allow the user to store any object python
def save_pickle(data, name):
    #print(name)
    with open(name, 'wb') as handle:
        pickle.dump(data, handle, protocol=2)