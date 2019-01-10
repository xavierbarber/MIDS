#/usr/bin/env  python   
# -*- coding: utf-8 -*-

###############################################################################

# AUTHOR: Jhon
#
# E-MAIL: jhonasgamm@yahoo.com
#
# version:0.1
#
# creation_date: 7/11/2017
#
# Last_modification: 09/11/2017
#
# Description: Takes the series description and separates them according to the type.
#				second version of scans_tagger this time is verified in the range of 
#				min and max values of the tags Repetition Time and Echo time.
#			
#
###############################################################################
###############################################################################
# Imports
###############################################################################
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pandas import DataFrame
import sys,os,os.path
import glob

# What is the location of your experiment folder
experiment_dir = ('/home/ceib/Projects/MIDAS/training_wheels_Spine')
work_dir = experiment_dir +'/io/input/Stage_1_dataCollection/labeled_scans/'

# load the tables with radiological protocols
protocol_csv = glob.glob(work_dir + "*.csv")
df_protocol=pd.read_csv(protocol_csv[0], sep='\t')
df_protocol.reset_index()
# Set index
df_protocol = df_protocol.set_index('Pot')

studyList = ['Scanning Sequence (0018,0020)','Repetition Time (0018,0080)','Echo Time (0018,0081)',
             'Inversion Time (0018,0082)', 'Flip Angle (0018,1314)','Echo Train Length (0018,0091)', 
             'plane','slides', 'Series Description (0008,103E)']

# Results DataFrame
addList = studyList[1:5]
df_add2= pd.DataFrame(0, index=df_protocol.index, columns=addList)
scan_intro=[['None', 0, 0, 0, 0, 0, None, 0, 'None']]
targetScan= pd.DataFrame(scan_intro, columns=studyList)
###############################################################################
# Functions
###############################################################################

def tagger(Scanning_Sequence, Repetition_Time, Echo_Time, Inversion_Time, Flip_Angle, Echo_Train_Length=0, plane='None', slides=0, Series_Description='None' ):
	global df_protocol
	
	scan_intro[0] =[Scanning_Sequence, Repetition_Time, Echo_Time, Inversion_Time, Flip_Angle, Echo_Train_Length, plane, slides, Series_Description]
	targetScan= pd.DataFrame(scan_intro, columns=studyList)
	
	#scan group
#               SE = Spin Echo          =====>>>> 'SE'
#               IR = Inversion Recovery =====>>>> 'IR' 'IR\\SE' 'SE\\IR'
#               GR = Gradient Recalled  =====>>>> 'GR'
#               EP = Echo Planar        =====>>>> 'EP\\SE' 'EP\\SE\\EP' 'EP\\S'
#               RM = Research Mode      =====>>>> 'RM'
	
	ScanSeq = [['SE'],['IR', 'IR\\SE', 'SE\\IR'],['GR'],['EP','EP\\SE', 'EP\\SE\\EP', 'EP\\S'],['RM']]
	
	# Verify to which scan group corresponds
	targetScanScanningSequence = '-'
	for ss in ScanSeq:
		for l in range(0,len(ss)):
			if all(targetScan['Scanning Sequence (0018,0020)'] == (ss[l])):
				targetScanScanningSequence = ss[0]
	# print(targetScanScanningSequence)		
	SS_protocol_index=df_protocol[(df_protocol['Scanning Sequence (0018,0020)'] == targetScanScanningSequence)].index

	# if you want to know if it's spin echo or fast spin echo, uncomment:
	# if (targetScanScanningSequence == 'RM') or (targetScanScanningSequence == 'SE'):        
		# if all((targetScan['Echo Train Length (0018,0091)'] <= 1)): print ('Spin Echo') #spin echo
		# else: print ('Fast Spin Echo') #fast spin echo
	
	# correction of incomplete and / or undefined values in the protocol table		
	df_protocol.replace('MinFull',10.0,inplace=True)
	df_protocol.replace('Min',10.0,inplace=True)
	df_protocol.replace('Auto',10.0,inplace=True)
	df_protocol=df_protocol.fillna(90)
	
	# calculating the closest distance between the values in the protocol table and the corresponding Dicom tag for the scan delivered
	for pix in SS_protocol_index:
		pters = []
		for p in range(0,len(addList)):
			pters.append(list(map(float,(str(df_protocol.loc[pix,addList[p]]).split(',')))))			
			val=[]
			temp=[]
			# for the search of the minimum value in the parameters Repetition Time and Echo time, 
			# it will be verified if the input value is within the range of these parameters [min, x, max], 
			# if so, it is valued as 0, otherwise value with the distance to the nearest end.
			if p<2:
				if len(pters[p])>1:
					if all((targetScan[addList[p]] >= min(pters[p])) & (targetScan[addList[p]] <= max(pters[p]))): temp = 0
					else: temp = min((abs(min(pters[p]) - targetScan[addList[p]])[0]),(abs(max(pters[p]) - targetScan[addList[p]])[0]))		
				else: temp = (abs((pters[p]) - targetScan[addList[p]])[0])
			else: 
				for n in range(0,len(pters[p])):val.append(abs((pters[p][n]) - targetScan[addList[p]])[0])
				temp = min(val)				
			df_add2.loc[pix,addList[p]] = temp			
#**********************************************				
	df_add2['Total']=df_add2[addList[0]]+df_add2[addList[1]]+df_add2[addList[2]]+df_add2[addList[3]]
			
	# # select the lowest value
	found2 = df_add2[(df_protocol['Scanning Sequence (0018,0020)'] == targetScanScanningSequence)]
	nFound2 = found2.Total.sort_values()	
	
	if len(nFound2) >= 2:
		target2 = [nFound2.index[0],nFound2.index[1]]#,nFound.index[2]]
		score2 = [round(nFound2[0],4),round(nFound2[1],4)]#,round(nFound[2],4)]
		#target = found[(found['Total'] <= nFound[2])].index
	else:
		counting2=found2.Total.min()
		target2 = df_add2[(df_add2['Total'] == counting2)].index
		score2=round(score2,4)
#**********************************************	
	#return found2,found, target2, target
	return target2[0]