#/usr/bin/env  python   
# -*- coding: utf-8 -*-

###############################################################################
# AUTHOR: Jose  mod: Jhon
#
# E-MAIL: jhonasgamm@yahoo.com
#
# version:0.1
#
# creation_date: 24/08/2017
#
# Last_modification: 24/08/2017
#
# Description: Takes the series description and separates them according to the type
###############################################################################
###############################################################################


plane = ['ax', 'cor', 'sag']
sequence = ['t1', 't2', 'stir']
thrD = '3d'
settings1 = ['fs', 'fse', 'tse']
settings2 = ['fr', 'ss', 'difusion', 'dwi']

def Split_Text(serieDescrip):
	p = []
	s = []
	p1 = []
	p2 = []
	is_3D = False
	scan=serieDescrip.lower()
	for find_word in plane:
		if scan.find(find_word) >= 0:
			p.append(find_word)
	for find_word in sequence:
		if scan.find(find_word) >= 0:
			s.append(find_word)
	for find_word in settings1:
		if scan.find(find_word) >= 0:
			p1.append(find_word)
	for find_word in settings2:
		if scan.find(find_word) >= 0:
			p2.append(find_word)
	if scan.find(thrD) >= 0:
		 is_3D = True
	return [p,s,p1,p2,scan]