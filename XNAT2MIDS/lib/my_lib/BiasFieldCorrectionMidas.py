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
# creation_date: 14/11/2017
#
# Last_modification: 23/11/2017
#
# Description:



###############################################################################
###############################################################################

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pandas import DataFrame
import nibabel as nib
import sys,os,os.path
import glob
#from time import time 
import threading
import time
import random

from nipype.interfaces import fsl
#from nipype.interfaces.fsl import SUSAN

fsl.FSLCommand.set_default_output_type('NIFTI')
# https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FAST

# What is the location of your experiment folder
#experiment_dir = ('/home/ceib/Projects/MIDAS/training_wheels_Spine') # in data node 02
experiment_dir = ('/mnt/cabinaData/openmind/Midas/training_wheels_Spine') # in cabina
#----
# What is the location of your data folder, uncomment #newLocation, if your native images are in the cabin
location = '/data/3/input_Midas/'
#newLocation = '/data/3/input_Midas/'
newLocation = '/mnt/cabinaData/openmind/Midas/'    
#----

work_dir = experiment_dir +'/io/input/Stage_1_dataCollection/labeled_scans/'
sys.path.append(experiment_dir + '/lib/my_lib/')
from search_dirs import listdirs, listdirs_fullnames, listFiles_regex
proyect = ['GlioHabitats/', 'Midas/' ]
numProyect=1
ext='.nii'

# select the type of image
typeMRI = 3 #type of image (1 for T1, 2 for T2, 3 for PD)
## The following protocols are used for the Midas project 
protocol = 4 # (1 = Sagittal T1 FSE, 2 = Sagittal T2 FSE, 3 = Axial T2 FSE, 4 = Sagittal STIR)


def strtolist (words,location = '/data/3/input_Midas/',newLocation = '/data/3/input_Midas/'):
    
    #newLocation = '/mnt/cabinaData/openmind/Midas/'
    #location = '/data/3/input_Midas/'
    
    w = words.split(',')    
    for n in range(0,len(w)):
        w[n]=w[n].replace("'",'').replace("[",'').replace("]",'').replace(location,newLocation).lstrip()
    return w
    

def load_join_scans(files):
    sorted(files)
    slices = [nib.load(files[s]) for s in range(0,len(files))]
    img_data = np.concatenate([img.dataobj for img in slices], axis=2)
    
    equal_header_test = True
    header = slices[0].header     
    for n in range(0,len(slices)):
        img = slices[n]
        #print(img.header)
        equal_header_test = equal_header_test and img.header == header
        #print(equal_header_test)
    imgs = nib.Nifti1Image(img_data, slices[0].affine, header=header)
    
    if not equal_header_test:
        print("WARNING: Not all headers were equal!")
    return imgs

def biasField_FSL(imgTemp,tI):
    # time_ini= time()
    ext='.nii'
    fastr = fsl.FAST()
    fastr.inputs.in_files = imgTemp+ext
    fastr.inputs.img_type = tI #type of image (n=1 for T1, n=2 for T2, n=3 for PD)
    fastr.inputs.bias_iters = 4 # Loop iterations during initial bias-field removal phase
    fastr.inputs.number_classes = 4 # number of tissue-type classes
# fastr.inputs.out_basename = str(imgTemp + '_BiasField' + ext)
    fastr.inputs.output_biasfield = True #Output estimated bias field
    fastr.inputs.output_biascorrected = True # Output bias field correction image (reciprocal of the estimated bias field)
    fastr.cmdline
    fastr.run()
# time_fin= time()
    print ('End bias field = '+ imgTemp)

def susan_FSL(imgRestore):
    # Smoothing (FSL)

	ext2='.nii.gz'
 
	sus = fsl.SUSAN()
	sus.inputs.in_file = imgRestore # 
	#sus.inputs.brightness_threshold = 50.0 # brightness threshold and should be greater than noise level and less than contrast of edges to be preserved.
	sus.inputs.fwhm = 1.0  # fwhm of smoothing, in mm, gets converted using sqrt(8*log(2))
	result = sus.run() 

	#print ('time = '+ str(time_fin- time_ini))

## Define a function to get the brightness threshold for SUSAN    
def getbtthresh(medianvals):
    return [0.75 * val for val in medianvals]
def getusans(x):
    return [[tuple([val[0], 0.75 * val[1]])] for val in x]    
    


def worker(w,c):
    print ("Work number: " + str(w))
    #We load the file to create a nibabel image object:
    listSlice = strtolist(file_nii.iloc[w],location,newLocation)
    currentDir = listSlice[0].split('/')
    nameScan='/'.join(currentDir[len(currentDir)-1:len(currentDir)])
    derivativesDir=[]
    if protocol == 4: # Sagittal STIR
        derivativesDir.append('/'.join(currentDir[0:len(currentDir)-4])+'/derivatives/biasField/' + '/'.join(currentDir[len(currentDir)-4:len(currentDir)-1])+'/stir_t1')
        derivativesDir.append('/'.join(currentDir[0:len(currentDir)-4])+'/derivatives/biasField/' + '/'.join(currentDir[len(currentDir)-4:len(currentDir)-1])+'/stir_t2')
        derivativesDir.append('/'.join(currentDir[0:len(currentDir)-4])+'/derivatives/biasField/' + '/'.join(currentDir[len(currentDir)-4:len(currentDir)-1])+'/stir_dp')
    else:
        derivativesDir.append('/'.join(currentDir[0:len(currentDir)-4])+'/derivatives/biasField/' + '/'.join(currentDir[len(currentDir)-4:len(currentDir)-1]))
    for t in range(1,len(derivativesDir)+1):
        if not(os.path.exists(derivativesDir[t-1])): 
            os.makedirs(derivativesDir[t-1])
            print(derivativesDir[t-1])
        else: print(derivativesDir[t-1])

        if len(listSlice) != 1: img_SagT2FSE_nii = load_join_scans(listSlice)
        else: img_SagT2FSE_nii = nib.load(listSlice[0])

        nameTemp=derivativesDir[t-1] + '/'+ nameScan.split('.')[0]

        img_SagT2FSE_nii.to_filename(os.path.join(derivativesDir[t-1] + '/', nameScan.split('.')[0]+ext))
        if len(derivativesDir)>1:
            typeMRI = t
            #print(typeMRI)

        biasField_FSL(nameTemp,typeMRI)
        
    print("completed work: " + str(w) + 'total Scans' + str(c))
    return

def stopWork(nw):
    print('************* assets :'+ str(threading.active_count())+' **************')
    while threading.active_count() > nw+1:
        time.sleep(30)
        print ('******waiting,   '+str(threading.active_count()))
    print('*************** continue ***************')


scan_csv = glob.glob(work_dir+proyect[numProyect] + "*_filt.csv")
df=pd.DataFrame()
df=pd.read_csv(scan_csv[0], sep='\t',low_memory=False)
del df['Unnamed: 0']
df.reset_index()

## The following protocols are used for the Midas project: Axial T2 FSE, Sagittal T1 FSE, Sagittal T2 FSE, Sagittal STIR
df_SagStir=df[(df['plane'] == 'Sag')&((df['label'] == 'STIR_RM') | (df['label'] == 'STIR_Spine') |(df['label'] == 'STIR_Spine_Midas'))]
df_SagT2FSE=df[(df['plane'] == 'Sag')&((df['label'] == 'T2_Spine') | (df['label'] == 'T2_brain') | (df['label'] == 'T2_RM'))]
df_SagT1FSE=df[(df['plane'] == 'Sag')&((df['label'] == 'T1_Spine') | (df['label'] == 'T1_brain') | (df['label'] == 'T1_RM'))]
df_AxT2FSE=df[(df['plane'] == 'Tra')&((df['label'] == 'T2_Spine') | (df['label'] == 'T2_brain') | (df['label'] == 'T2_RM'))]

print('Midas SagT2 SagT1 SagStir AxT2FSE Scans = ') 
print(len(df), len(df_SagT2FSE), len(df_SagT1FSE), len(df_SagStir), len(df_AxT2FSE))
print('Midas + SagT2 + SagT1 + SagStir + AxT2FSE Scans = ' + str(len(df_SagT2FSE+df_SagT1FSE+df_SagStir+df_AxT2FSE)))

## select the type of image (1 = Sagittal T1 FSE, 2 = Sagittal T2 FSE, 3 = Axial T2 FSE, 4 = Sagittal STIR)

if protocol == 1: 
    file_nii = df_SagT1FSE['filename'] # Sagittal T1 FSE
    print('Protocol = Sagittal T1 FSE ' + str(len(df_SagT1FSE)))
elif protocol == 2: 
    file_nii = df_SagT2FSE['filename'] # Sagittal T2 FSE
    print('Protocol = Sagittal T2 FSE ' + str(len(df_SagT2FSE)))
elif protocol == 3: 
    file_nii = df_AxT2FSE['filename']  # Axial T2 FSE
    print('Protocol = Axial T2 FSE ' + str(len(df_AxT2FSE)))
elif protocol == 4: 
    file_nii = df_SagStir['filename']  # Sagittal STIR
    typeMRI=0
    print('Protocol = Sagittal STIR ' + str(len(df_SagStir)))

## paralelización

cant=len(file_nii)
#cant = 2
nWorker = 50
print ("Scans Number "+ str(cant)+" Number of workers "+str(nWorker))
time.sleep(30)
wanting =(cant) % nWorker
n1=0
threads = list()

if wanting > 0:
    for n in range(0,(cant-wanting),nWorker):
        for n1 in range(n, n+nWorker):
            stopWork(nWorker)
            t = threading.Thread(target=worker, args=(n1,cant,))
            threads.append(t)
            print ('n1= '+ str(n1)+'*****impar****** ')
            t.start()

    for n in range(n1+1,(cant),wanting):
        for n2 in range(n, n+wanting):
            stopWork(nWorker)
            t=threading.Thread(target=worker, args=(n2,cant,))
            threads.append(t)
            t.start()
            print('n2= '+str(n2)+'***sobra****')

else: 
    for n in range(0,cant,nWorker):
        for n1 in range(n,n+nWorker):
            stopWork(nWorker)
            t = threading.Thread(target=worker, args=(n1,cant,))
            threads.append(t)
            t.start()
            print ('n1= '+ str(n1)+'*****par**** ')
