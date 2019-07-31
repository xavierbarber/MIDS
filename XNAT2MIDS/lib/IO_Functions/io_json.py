# -*- coding: utf-8 -*-

###############################################################################
# Imports
###############################################################################
import json


###############################################################################
# Functions
###############################################################################

"""
This function allows the user to save one tag dicom in an archive json
"""


def add_tag_dicom(tag, description, value, json_file_path):
    json_file = load_json(json_file_path)
    for i in range(len(json_file["ResultSet"]["Result"])):
        if json_file["ResultSet"]["Result"][i]["tag1"] == tag:
            json_file["ResultSet"]["Result"][i]["value"] = value
            break
    else:
        json_file["ResultSet"]["Result"].append({"tag1":tag, "tag2":"", "desc":description, "value":value})
    save_json(json_file, json_file_path)


"""
This function allow the user to obtain one tag dicom from an archive json


Return a dict of the tag dicom
"""

def get_tag_dicom(tag, json_file_path):
    json_file = load_json(json_file_path)
    for i in range(len(json_file)):
        if json_file[i]["tag1"] == tag:
            return json_file[i]
    else:
        return None



"""
This function allow the user store one object in an archive json
"""
def save_json(subject, path):
    string_json = json.dumps(subject, default=lambda o: o.__dict__,
         sort_keys=True)
    try:
        f = open(path, "w")
    except IOError:
        f = open(path, "a")
    f.write(string_json)
    f.close()


"""
This function allow the user obtain one object from an archive json

Return the struct dict json
"""
def load_json(path):
    f = open(path, "r")
    json_string = f.read()
    f.close()
    return json.loads(json_string)
