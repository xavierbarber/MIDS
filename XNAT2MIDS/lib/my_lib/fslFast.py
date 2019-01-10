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
#FAST (FMRIB's Automated Segmentation Tool) segments a 3D image of the brain into different tissue types (Grey Matter, White Matter, CSF, etc.), 
#whilst also correcting for spatial intensity variations (also known as bias field or RF inhomogeneities). 
#The underlying method is based on a hidden Markov random field model and an associated Expectation-Maximization algorithm. 
#The whole process is fully automated and can also produce a bias field-corrected input image and a probabilistic and/or partial volume tissue segmentation. 
#It is robust and reliable, compared to most finite mixture model-based methods, which are sensitive to noise.
#If you use FAST in your research, please quote the article:
#Zhang, Y. and Brady, M. and Smith, S. Segmentation of brain MR images through a hidden Markov random field model and the expectation-maximization algorithm. IEEE Trans Med Imag, 20(1):45-57, 2001.

###############################################################################
###############################################################################

# Modulos importados
#Modulos que se importan

from nipype.interfaces import fsl
fsl.FSLCommand.set_default_output_type('NIFTI')
# https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FAST

path_Dir = '/home/ceib/test_Colum/MIDASds02/158392553766483608981196288097467395188/129220888561355109979285669911264684387/scans/2/NIFTI/'
file_sagT2_nii = '12840113619218210808617256132145330550394123-2-1-1fkhesxLUMBAR2012s002a1001'
ext = '.nii'


fastr = fsl.FAST()
fastr.inputs.in_files = str(path_Dir + file_sagT2_nii + ext)
fastr.inputs.img_type = 2 #type of image (n=1 for T1, n=2 for T2, n=3 for PD)
fastr.inputs.bias_iters = 4 # Loop iterations during initial bias-field removal phase
fastr.inputs.number_classes = 4 # number of tissue-type classes
#fastr.inputs.out_basename = str(path_Dir + file_sagT2_nii + '_corrected' + ext)
fastr.inputs.output_biasfield = True #Output estimated bias field
fastr.inputs.output_biascorrected = True # Output bias field correction image (reciprocal of the estimated bias field)
fastr.cmdline
fastr.run()



