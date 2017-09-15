# -*- coding: utf-8 -*-


###############################################################################
# Imports
###############################################################################
import pickle as pickle

###############################################################################
# Functions
###############################################################################

"""
This function allow the user to load any object python into the programme
"""


def load_pickle(filepath):
    #print(filepath)
    with open(filepath, 'rb') as handle:
        unserialized_data = pickle.load(handle)
    return unserialized_data

"""
This function allow the user to store any object python
"""


def save_pickle(data, filepath):
    #print(filepath)
    with open(filepath, 'wb') as handle:
        pickle.dump(data, handle, protocol=2)

"""
This fuction allow the user convert a csv file into object python dict.
the id of the table is found in the first column
"""


def csv_2_dict(filepath):
    dict_ = dict()
    with open(filepath, '+r') as handle:
        line_list_cab = handle.readline().replace('\n','').split(',')
        line_list_range = list(range(1, len(line_list_cab)))
        for line in handle.readlines():
            line_list = line.replace('\n','').split(',')
            key = line_list[0]
            dict_2 = dict()
            for item_pos in line_list_range:
                dict_2[line_list_cab[item_pos]] = line_list[item_pos]
            dict_[key] = dict_2
    return dict_