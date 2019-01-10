#/usr/bin/env  python   
# -*- coding: utf-8 -*-

###############################################################################
###############################################################################
# AUTHOR: Jhon Jairo Saenz Gamboa
#
# E-MAIL: jhonasgamm@yahoo.com
#
# version:0.1
#
# creation_date: 23/08/2017
#
# Last_modification: 11/10/2017
#
# Description:


###############################################################################
###############################################################################

from os import walk, getcwd, path
import re
import sys,os,os.path

# List the directories in the specific folder

def listdirs(folder):
	return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]
 

# List the full path of the directories in the specific folder
 
def listdirs_fullnames(folder):
	return [
		d for d in (os.path.join(folder, d1) for d1 in os.listdir(folder))
		if os.path.isdir(d)
	]


# Find files with a regular expression (full path)
# Example : listFiles_regex( r'.tsv',input_dir)

def listFiles_regex(regex = '', folder = getcwd()):
    pat = re.compile(regex, re.I)
    result = []
    for (dir, _, files) in walk(folder):
        result.extend([ path.join(dir,arch) for arch in 
                              filter(pat.search, files) ])
        # break  # enable if subdirectories are not searched
    return result