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
# Last_modification: 23/08/2017
#
# Description:

# Loading the files
# DICOM is the de-facto file standar in medical imaging. these files contain a lot of metadata (such as the pixel size, 
# so how long one pixel is in every dimension in the real world). 
# The pixel size/coarseness of the scan to scan (e.g. the distance between slices may differ). 
# Below is code to load a scan, which consist of multiples slices, which we simply save in payton list. 
# Every folder in the dataset is one scan (so one patient). One metadata field is missing, 
# the pixel size in the Z direction, which is the slice thickness. Fortunately we can infer this, and we add ths to the metadata.

###############################################################################
###############################################################################

import sys,os,os.path
import dicom
import numpy as np # linear algebra

# Load the scans in given folder path
def load_scan(path):
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness       
    return slices

# search the scans in given the directory 
# input, search directory
# output, 
# 		fList, list the entire directory
# 		fnameindir, list all files in the directory
# 		dirDicom, list all directory 'DICOM'
# 		dirNifti, list all directory 'NIFTI'

def search(rootDir):
    fList=[]
    fnameindir=[]
    dirDicom=[]
    dirNifti=[]

    for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
        #print('Found directory: %s' % dirName)
        if dirName.find('DICOM') >=0:
            dirDicom.append(dirName)
        if dirName.find('NIFTI') >=0:
            dirNifti.append(dirName)
        fList.append(dirName)
  
        for fname in fileList:
            #print('\t%s' % fname)
            fnameindir.append(fname)
         
    return fList, fnameindir, dirDicom, dirNifti
	