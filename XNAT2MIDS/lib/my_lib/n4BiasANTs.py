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
# creation_date: 15/08/2017
#
# Last_modification: 15/08/2017
#
# Description:
# 	N4BiasFieldCorrection
#	Wraps command N4BiasFieldCorrection
#	N4 is a variant of the popular N3 (nonparameteric nonuniform normalization) retrospective bias correction algorithm. 
#	Based on the assumption that the corruption of the low frequency bias field can be modeled as a convolution of the intensity histogram 
#	by a Gaussian, the basic algorithmic protocol is to iterate between deconvolving the intensity histogram by a Gaussian, 
#	remapping the intensities, and then spatially smoothing this result by a B-spline modeling of the bias field itself. 
#	The modifications from and improvements obtained over the original N3 algorithm are described in [Tustison2010].
#	[Tustison2010]	N. Tustison et al., N4ITK: Improved N3 Bias Correction, IEEE Transactions on Medical Imaging, 29(6):1310-1320, June 2010

###############################################################################
###############################################################################

# Modulos importados
#Modulos que se importan

import copy
import nipype.interfaces.ants as ants
from nipype.interfaces.ants import N4BiasFieldCorrection
import subprocess

def run_shell_cmd(cmd,cwd=[]):
    """ run a command in the shell using Popen
    """
    if cwd:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,cwd=cwd)
    else:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in process.stdout:
             print line.strip()
    process.wait()
    
def usage():
    """ print the docstring and exit"""
    sys.stdout.write(__doc__)
    sys.exit(2)
	
path_Dir = '/home/ceib/test_Colum/MIDASds02/158392553766483608981196288097467395188/129220888561355109979285669911264684387/scans/2/NIFTI/'
file_sagT2_nii = '12840113619218210808617256132145330550394123-2-1-1fkhesxLUMBAR2012s002a1001'

for bsfd in range(10,300,40):

	ext = '.nii'
	n4 = N4BiasFieldCorrection()
	n4.inputs.dimension = 3
	n4.inputs.input_image = str(path_Dir + file_sagT2_nii + ext)
	# n4.inputs.imageList = niifile
	n4.inputs.bspline_fitting_distance = bsfd #300
	n4.inputs.shrink_factor = 4
	n4.inputs.n_iterations = [100,100,50,25]
	# n4.cmdline
	n4.run()

	n4_2 = copy.deepcopy(n4)
	n4_2.inputs.convergence_threshold = 1e-6
	# n4_2.cmdline
	n4_2.run()

	n4_3 = copy.deepcopy(n4_2)
	n4_3.inputs.bspline_order = 4
	n4_3.inputs.output_image = 'ants_bspline_1_' + str(bsfd) + ext
	n4_3.inputs.save_bias = True
	# n4_3.cmdline
	n4_3.run()
	run_shell_cmd("cp ~/test_Colum/test_bias/bias_ants/"+file_sagT2_nii + "_bias" + ext +" "+ "~/test_Colum/test_bias/bias_ants/"+'ants_bspline_1_' + str(bsfd)+'_bias' + ext)

	n4_4 = N4BiasFieldCorrection()
	n4_4.inputs.input_image = str("~/test_Colum/test_bias/bias_ants/"+file_sagT2_nii +'_corrected'+ ext)
	n4_4.inputs.save_bias = True
	n4_4.inputs.output_image = 'ants_bspline_4_' + str(bsfd) + ext
	n4_4.inputs.dimension = 3
	# n4_4.cmdline
	n4_4.run()
	run_shell_cmd("cp ~/test_Colum/test_bias/bias_ants/"+file_sagT2_nii + "_corrected_bias" + ext +" "+ "~/test_Colum/test_bias/bias_ants/"+'ants_bspline_4_' + str(bsfd)+'_bias' + ext)

	
