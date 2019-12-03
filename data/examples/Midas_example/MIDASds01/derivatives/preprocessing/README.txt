
/////////////////////////////////// BiasField - FSL INFO ///////////////////////////////////

biasField_FSL

FAST (FMRIB's Automated Segmentation Tool) segments a 3D image of the brain into different tissue types (Grey Matter, White Matter, CSF, etc.), whilst also correcting for spatial intensity variations (also known as bias field or RF inhomogeneities). The underlying method is based on a hidden Markov random field model and an associated Expectation-Maximization algorithm. The whole process is fully automated and can also produce a bias field-corrected input image and a probabilistic and/or partial volume tissue segmentation. It is robust and reliable, compared to most finite mixture model-based methods, which are sensitive to noise.

If you use FAST in your research, please quote the article:

Zhang, Y. and Brady, M. and Smith, S. Segmentation of brain MR images through a hidden Markov random field model and the expectation-maximization algorithm. IEEE Trans Med Imag, 20(1):45-57, 2001.


config

FSL FAST wrapper for segmentation and bias correction
BIAS_ITERS = 4 # Loop iterations during initial bias-field removal phase
NUMBER_CLASSES = 4 # number of tissue-type classes



The various output images are:

_pve_   Partial volume maps: A (non-binary) partial volume image for each class, where each voxel contains a value in the range 0-1 that represents the proportion of that class's tissue present in that voxel. This is the default output.

_pveseg file contains the best hard segmentation that follows from the partial volume segmentation results.

_mixeltype  mixeltype volume file  (output from brain segmentation using FAST) The mixeltype file represents the classification of each voxel's tissue mixture. That is, voxels containing only one tissue type have a different mixeltype from that containing mixtures of two tissues, which is different again from those containing mixtures of all three tissues.

_seg    Binary segmentation: single image: This is the "hard" (binary) segmentation, where each voxel is classified into only one class. A single image contains all the necessary information, with the first class taking intensity value 1 in the image, etc.

_restore Restored input: This is the estimated restored input image after correction for bias field.

_bias   Bias field: This is the estimated bias field.


/////////////////////////////////// Registration - Ants INFO ///////////////////////////////////

antsRegistration 

Registration (sometimes called "Normalization") brings one image to match another image, such that the same voxels refers roughly to the same structure in both brains. Often the fixed (or target) image is a template, but you can register any two images with each other, there is nothing special in a template from the computation perspective.

Avants, Brian B et al. “The Insight ToolKit image registration framework.” Frontiers in neuroinformatics vol. 8 44. 28 Apr. 2014, doi:10.3389/fninf.2014.00044

config

transforms = ['Affine', 'SyN']
transform_parameters = [(2.0,), (0.25, 3.0, 0.0)]
number_of_iterations = [[1500, 200], [100, 50, 30]]
dimension = 3
write_composite_transform = True
collapse_output_transforms = False
initialize_transforms_per_stage = False
metric = ['Mattes']*2
metric_weight = [1]*2 # Default (value ignored currently by ANTs)
radius_or_number_of_bins = [32]*2
sampling_strategy = ['Random', None]
sampling_percentage = [0.05, None]
convergence_threshold = [1.e-8, 1.e-9]
convergence_window_size = [20]*2
smoothing_sigmas = [[1,0], [2,1,0]]
sigma_units = ['vox'] * 2
shrink_factors = [[2,1], [3,2,1]]
use_estimate_learning_rate_once = [True, True]
use_histogram_matching = [False, False] # This is the default

output

inverse_composite_transform:    (output_nverseComposite.h5) Inverse composite transform file
composite_transform:    (output_Composite.h5 file) Composite transform file
warped_image:   (reg file) Outputs warped image