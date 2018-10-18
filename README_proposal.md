
<div class="clearfix" style="padding: 0px; padding-left: 100px; display: flex; flex-wrap: nowrap; justify-content: space-evenly; align-items:center">
<a href="http://bimcv.cipf.es/"><img src="https://github.com/BIMCV-CSUSP/MIDS/blob/master/images/logotipo-fisabio_tauv.png?raw=true""./images/logotipo-fisabio_tauv.png" width="300px" style="display: inline-block; "></a><a href="http://ceib.san.gva.es"><img src="https://github.com/BIMCV-CSUSP/MIDS/blob/master/images/logo_CEIB.png?raw=true" width="200px" class="pull-right" style="display: inline-block;"></a><a href="http://www.eurobioimaging.eu/"><img src="http://www.eurobioimaging.eu/sites/all/themes/eurobio/images/euro_bio_imaging_logo.jpg" width="250px" class="center-block" style=" display: inline-block;"></a>
</div>
<br></br>

<center> <h1>Medical Imaging Bank Valencia Region</h1> </center>
<!--<h1 style="text-align:center">Medical Imaging Bank Valencia Region</h1>-->
<h2 style="text-align:center">Medical Imaging Data Structure</h2>
<!--<h4 style="text-align:center">BIDS Extension Proposal 20 (BEP020)</h4>-->

# Index

>[1. Preliminary clarifications](#clarifications)
>
>[2. Medical Population Imaging Data Structure ](#mids)
>
> > 2.1. [Introduction](#introduction)
> >
> > 2.2. [Directory structure](#dirstruc)
> >
> > 2.3. [Longitudinal studies with multiple sessions example](#lstu)
> >
> > > 2.3.1. [Label modality_label for MRI](#mod)
> > >
> > > 2.3.2. [Label sequence_label for MRI](#seq)
> > >
> > > 2.3.3. [Labels for Medical Imaging Modalities](#labels)
> >
> > 2.4. [Tabular files](#tab)
> >
> > > 2.4.1. [Participants description table (Sub-*.tsv)](#parti)
> > >
> > > 2.4.2. [Session description table (Sub-*.tsv)](#ses)
> > >
> > > 2.4.3. [Scans description table](#scans)
>
>[4. References](#references)

<a id='clarifications'></a>

# 1. Preliminary clarifications

This specification expands the specification of the brain image data structure (BIDS) to other medical imaging modalities, as well as to include different parts of the body. If you wish to know the context and general guidelines (definitions, units, directory structure, etc.), consult the [BIDS specifications document](https://docs.google.com/document/d/1HFUkAEE-pB-angVcYe6pf_-fVf4sCpOHKesUvfb8Grc)


The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this  document are to be interpreted as described in [RFC2119](https://www.ietf.org/rfc/rfc2119.txt).

Terminology that will be used in the following includes:

+  Subject	= human being (or phantom, etc) from whom the data is being acquired
+  Session	= a logical grouping of imaging that is consistent across subjects. One session is not limited to one set of scans but rather can be data obtained over several visits that are grouped into one session. Multiple sessions is appropriate when a large group of the subjects follow identical or similar data acquisition steps (often with some sort of intervention in between sessions)
+ Run 	= a non-intermittent period during which data for the subject(s) is continuously being acquired
+ Task 	= instructions (and corresponding stimulus material) that is performed by the subject
+ Pseudonymization = the processing of personal data in such a way that it can no longer be attributed to an interested party without using additional information, provided that such additional information appears separately and is subject to technical and organizational measures designed to guarantee that personal data are not attributed to an identified or identifiable natural person; PROTECTION OF PERSONAL DATA, 7 European Data Protection Regulation, CHAPTER I General Provisions.
+ Modalities of medical images = Type of equipment that  acquired the original data used to create the images in this Series. See Section [C.7.3.1.1.1](http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.3.html#sect_C.7.3.1.1.1) for Defined Terms.
+ Body Part = denoting the Defined Terms for Body Part Examined ,Dicom tag (0018,0015), see [Correspondence of Anatomic Region Codes and Body Part Examined DefinedTerms](http://dicom.nema.org/medical/dicom/current/output/chtml/part16/chapter_L.html#chapter_L)
+ Patient Position = specifies the position of the patient relative to the imaging equipment space. This attribute is intended for annotational purposes only. It does not provide an exact mathematical relationship between the patient and the imaging equipment,  tag Dicom, Patient Position (0018,5100) ,  See Section [C.7.3.1.1.2](http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.3.html#sect_C.7.3.1.1.2) in DICOM PS3.3 for Defined Terms and further explanation.


<a id='mids'></a>

# 2. Medical Population Imaging Data Structure

<p style="text-align:justify">
In order to add to the scientific knowledge, methods that yield reliable and reproducible results must be used. High test-retest reliability of the applied methods is the foundation of research, irrespective of the scientific discipline. It is in the prime interest of every scientist that results are reproducible. While such reproducibility was considered of utmost importance in the positron emitting tomography (PET) field [Adams et al., 2010], the quantitative assessment of reproducibility has largely been neglected in the fMRI community, or as Bennett and Miller described it: “Reliability is not a typical topic of conversation” between fMRI investigators [Bennett and Miller, 2010]. This situation changed significantly in 2016, following the establishment of the Committee on Best Practices in Data Analysis and Sharing ([COBIDAS](www.humanbrainmapping.org/cobidas/)) by the most important neuroimaging society - the Organisation for Human Brain Mapping (OHBM).
</p>

<p style="text-align:justify">
The objective of BIMCV (Medical Imaging Bank of the Valencia Region) is that all this scientific knowledge be collected in a correct and efficient way. More concretely, all that knowledge refers to imaging data. Finding a way to organize this information is crucial.
</p>

<p style="text-align:justify">
Currently, distinct forms to store images and medical information exist, but there is not a standard that indicates how this information should be organized and shared. CEIB’s idea is to use a simple organisation that any researcher can understand the distribution of data.
</p>

<p style="text-align:justify">
The organisational structure is called MIDS (Medical Imaging Data Structure). MIDS is a new standard that contains every type of medical information and images in simple hierarchical folders. It is born as an extension of the standard BIDS (Brain Imaging Data Structure). BIDS [Gorgolewski et al.] is a structure that collects medical brain images, but MIDS pretends to expand this further, and not confine it to brain images. The idea is to create the same structure with brain, spinal, torso, etc images , with Magnetic Resonance, Computed tomography, ecography, etc. This structure will follow the same process regardless of the type and shape of the image.
</p>
<a id='introduction'></a>

## 2.1. Introduction

<p style="text-align:justify">
Presently, many studies focused on obtaining a dataset of medical images. Since the use of these datasets, the qualitative improvements have been enormous for these studies. However, the management and control of the images and metadata added to the datasets is an added effort. Furthermore, during the study, more data is generated that needs to be relocated. Each study searchers for a way to organize all the data that best suits it, which makes it more difficult to understand the collected data and results.
At present, many studies based on obtaining a dataset of medical images for its process of study. The qualitative improvement has been enormous for these studies since its use. Management and control all images and metadata added to them is a extra hard work. Furthermore, during the study, more data is generated where it is necessary to relocate. Each study search the way to organize these data in the way that best suits. This makes it more difficult to understand the data collected and results.
</p>
<p style="text-align:justify">
There are a couple studies that propose a standard to store this type of data. One of them is BIDS ([Brain Imaging Data Structure](http://bids.neuroimaging.io/,[1]). BIDS is a proposed standard to store a magnetic resonance imaging and data in a structural folder hierarchy. The structure is very clear and easy to use. BIDS is supported by several programs and libraries dedicated to the study of medical images (i.e. c-pacs, freesurfer, xnat, BIDSValidator...) and it is often used by researcher groups. In Figure 1, a example of the BIDS structure is presented, the left directory is a folder with dicom images (Mildenberger, Eichelberg & Martin,2002) and the right directory is a BIDS structure.
</p>

<p style="text-align:center">
<img src="./images/dicom2bids.png" >
</p>
<div style='text-align:center;'>
figure 1: DICOM to BIDS conversion with the tool Dcm2Bids
</div>


<p style="text-align:justify">
Unfortunately, BIDS only supports MRIs and only brain images. For example, if a project need lumbar MRI, BIDS would not support these images. However, by taking this structure and expanding it, other  imaging techniques can be integrated. For that, MIDS was created.
Currently, BIDS is a potential standard to store MRI and there is a little difference between BIDS and MIDS. However, MIDS pretends to incorporate, within epidemiological studies based on Population Image (BIMCV), any type of modality of medical images (i.e. Computed Radiography,Computed Tomography, Ultrasound, Mammography, ...).
</p>

<a id='dirstruc'></a>

## 2.2. Directory structure

MIDS is trying to establish itself as an ampliation to BIDS. The structural format is highly similar to BIDS in MRI. The paper of [standar BIDS](http://www.nature.com/articles/sdata201644) or [BIDS specification](http://bids.neuroimaging.io/bids_spec1.0.2.pdf) provides more detail.

Below is the directory hierarchy<sup id="a1">[1](#f1)</sup> provided by BIDS standard:

<div>
<pre>
<code>
Data/
├── sub-&ltparticipant_label&gt[_ses-&ltsesion-label&gt]
├── [code/]
├── [derivatives/]
├── [stimuli/]
└── [sourcedata/]
</code>
</pre>
</div>
<b id="f1">1</b>  "[ ]" indicates optional: no warning if missing (i.e. MAY as per RFC2199)[↩](#a1)

#### BIDS, Template of  brain  mri.

This template keeps the tags used in BIDS, in the cases of brain MRI:

<div>
<pre>
<code>
Data/
└──sub-&ltparticipant_label&gt[_ses-&ltsesion-label&gt]
   └── anat/
       └──sub- &ltparticipant_label&gt[_ses-&ltsesion-label&gt][_acq-&ltlabel&gt]
          [_ac-&ltlabel&gt][_rec-&ltlabel&gt][_run-&ltindex&gt]
          _&ltmodality_label&gt.nii[.gz]
</code>
</pre>
</div>
MIDS adds a new level to the directory hierarchy of the BIDS standard. The new level describes the modalities of medical images used for a particular session.

Below is the new directory hierarchy:

<div>
<pre>
<code>
Data/
└──sub-&ltparticipant_label&gt[_ses-&ltsesion-label&gt]
   └── [/mod-&ltmodality_medical_image_label&gt]
       └──sub- &ltparticipant_label&gt[_ses-&ltsesion-label&gt][_acq-&ltlabel&gt]
          [_ac-&ltlabel&gt][_rec-&ltlabel&gt][_run-&ltindex&gt]
          _&ltdata_type&gt.nii[.gz]
</code>
</pre>
</div>

<!--<span style="color:#33cc00"></span>-->
The added level corresponds to the different modalities of medical imaging, which can be classified by the energy used in the acquisition, together with the functional or tomographic adjectives to allow these images to be generated. In table 1. we can see the classifications:




<table class="tg">
  <tr>
    <th class="tg-us36">Modality of medical image<br></th>
    <th class="tg-c3ow">Technique<br></th>
    <th class="tg-us36">Energy</th>
    <th class="tg-us36">Functional<br></th>
    <th class="tg-us36">Tomography<br></th>
  </tr>
  <tr>
    <td class="tg-us36" rowspan="3">General Radiology</td>
    <td class="tg-us36">radiography</td>
    <td class="tg-dvpl">X-rays</td>
    <td class="tg-dvpl">No</td>
    <td class="tg-dvpl">No</td>
  </tr>
  <tr>
    <td class="tg-us36">Radioscopy</td>
    <td class="tg-dvpl">X-rays</td>
    <td class="tg-dvpl">No</td>
    <td class="tg-dvpl">No</td>
  </tr>
  <tr>
    <td class="tg-us36">Computerized Tomographic, CT<br></td>
    <td class="tg-dvpl">X-rays</td>
    <td class="tg-dvpl">No</td>
    <td class="tg-dvpl">Yes</td>
  </tr>
  <tr>
    <td class="tg-us36" rowspan="2">Nuclear Medicine<br></td>
    <td class="tg-us36">Single Photon Emission <br>Computed Tomography, SPECT<br></td>
    <td class="tg-dvpl">Ɣ-rays</td>
    <td class="tg-dvpl">Yes</td>
    <td class="tg-dvpl">Yes</td>
  </tr>
  <tr>
    <td class="tg-us36">Positron Emission <br>Tomography, PET<br></td>
    <td class="tg-dvpl">Ɣ-rays</td>
    <td class="tg-dvpl">Yes</td>
    <td class="tg-dvpl">Yes</td>
  </tr>
  <tr>
    <td class="tg-us36">Ultrasound</td>
    <td class="tg-us36">Ultrasound</td>
    <td class="tg-dvpl">ultrasound</td>
    <td class="tg-dvpl">No</td>
    <td class="tg-dvpl">Yes</td>
  </tr>
  <tr>
    <td class="tg-us36" rowspan="2">Magnetic Resonance<br></td>
    <td class="tg-us36">Magnetic resonance <br>imaging, MRI<br></td>
    <td class="tg-dvpl">radiofrequency</td>
    <td class="tg-dvpl">No</td>
    <td class="tg-dvpl">Yes</td>
  </tr>
  <tr>
    <td class="tg-us36">functional MRI (fMRI)<br></td>
    <td class="tg-dvpl">radiofrequency</td>
    <td class="tg-dvpl">Yes</td>
    <td class="tg-dvpl">Yes</td>
  </tr>
  <tr>
    <td class="tg-us36">Endoscopy</td>
    <td class="tg-us36">Endoscopy</td>
    <td class="tg-dvpl">light</td>
    <td class="tg-dvpl">No</td>
    <td class="tg-dvpl">No</td>
  </tr>
  <tr>
    <td class="tg-us36">Microscopy</td>
    <td class="tg-us36">Microscopy</td>
    <td class="tg-dvpl">light</td>
    <td class="tg-dvpl">No</td>
    <td class="tg-dvpl">Yes</td>
  </tr>
</table>
<div style='text-align:center;'>
Table 1: Classification by the energy that is used in the acquisition along with its functional or tomographic adjectives.
</div>

Source: [Cloud CEIB I+D
Sistema de gestión y extracción de
conocimiento de la imagen médica]( http://ceib.san.gva.es/documents/55625/c800abcc-00da-4122-8ff9-8d6575ca2ef3) page : 37


#### MIDS, General template for other parts of the body in MRI

This template maintains the tags used in BIDS and adds filename keys:


<div>
<pre>
<code>
Data/
└──sub-&ltparticipant_label&gt[_ses-&ltsesion-label&gt]
   └── rm
       └── anat
            └──sub- &ltparticipant_label&gt[_ses-&ltsesion-label&gt]
                [_acq-&ltlabel&gt][_ac-&ltlabel&gt][_rec-&ltlabel&gt][_run-&ltindex&gt]
                [_bp-&ltBodyPartExamined_label&gt][_vp-&ltviewPosition_label&gt]
                _&ltmodality_label&gt.nii[.gz]
</code>
</pre>
</div>

#### MIDS, General template for other medical imaging equipment

This template includes the new level that describes other modalities of medical images besides  MRI.
It is the investigators decision to determine whether particular filename keys are used or not. This will depend on the modality of each medical image. For example, you can use the filename key [ _ce-\<label\> ] in the Computed Tomography, but that key will not be necessary in Bone Densitometry (X-Ray).

<div>
<pre>
<code>
Data/
└──sub-&ltparticipant_label&gt[_ses-&ltsesion-label&gt]
   └── &ltmod&gt
        └──sub- &ltparticipant_label&gt[_ses-&ltsesion-label&gt]
                [_acq-&ltlabel&gt][_ac-&ltlabel&gt][_rec-&ltlabel&gt][_run-&ltindex&gt]
                [_bp-&ltBodyPartExamined_label&gt][_vp-&ltviewPosition_label&gt]
                _&ltmodality_dicom&gt.nii[.gz]
</code>
</pre>
</div>

See in Table 2 image modalities supported by MIDS, the relationship of the modalities of medical image with the Dicom modality, and its corresponding label.

Breakdown of filename keys:

+ acq-\<label\> - denoting which set of acquisition parameters was used ( - optional)
+ rec-\<label\> - denoting which reconstruction was used; “norm” corresponds to normalized images (optional)
+ run-\<index\> - denotes a repetition of identical acquisition with identical scanning parameters
	(optional)
+ bp-<BodyPartExamined_label> - ( - optional) denoting the Defined Terms for Body Part Examined ,Dicom tag (0018,0015) , see:  Correspondence of Anatomic Region Codes and Body Part Examined Defined Terms
+ vp-<viewPosition_label> which describes the section, view, planes, direction or projection in the acquisition, (- optional).
Possible labels:

    - Planes:  sag = Sagittal plane, cor = Coronal plane, ax = Axial plane.
    - projections: ap = Anterior/Posterior, pa = Posterior/Anterior, ll = Left Lateral, rl = Right Lateral, rld = Right Lateral Decubitus, lld = Left Lateral Decubitus, rlo = Right Lateral Oblique, llo = Left Lateral Oblique .

  Examples by type of medical imaging modality:

      - In the case of radiography, the terms for View Position are defined in the tag dicom (0018,5101)
      - In the case of mammography, the terms for Partial View Description are defined in the tag dicom (0028,1351), See Section C.8.11.7.1.3. And CID 4014 View for Mammography , can include laterality of the region examined. Right = r, Left = l , both (e.g., cleavage) = b, Dicom tag, Image Laterality (0020,0062).
      - In the case of mri, the plane can be calculated from the DICOM tag: Image Orientation (0020,0037)

+ <modality_Dicom>: Type of equipment that acquired the original data used to create the images in this Series. Dicom tag (0008,0060), See Section C.7.3.1.1.1 in DICOM PS3.3 for Defined Terms.

<a id='lstu'></a>
## 2.3. Longitudinal studies with multiple sessions example

This is an example of the folder and file structure. Because there is only one session, the session level is not required by the format. For details on individual files see descriptions in the next section:

<div>
<pre>
<code>
Data/
├── sub-01
│  ├──  ses-01
│  │   ├── rm
│  │   │   ├── anat
│  │   │   │   ├── sub-01_ses-01_bp-lsspine_vp-ax_T1w.nii.gz
│  │   │   │   └── sub-01_ses-01_bp-lsspine_vp-ax_T1w.json
│  │   │   ├── func
│  │   │   │   ├── sub-01_ses-01_task-nback_bp-heart_vp-fourChamber_bold.nii.gz
│  │   │   │   ├── sub-01_ses-01_task-nback_bp-heart_vp-fourChamber_bold.json
│  │   │   │   ├── sub-01_ses-01_task-nback_bp-heart_vp-fourChamber_events.tsv
│  │   │   │   ├── sub-01_ses-01_task-nback_bp-heart_vp-fourChamber_physio.tsv.gz
│  │   │   │   ├── sub-01_ses-01_task-nback_bp-heart_vp-fourChamber_physio.json
│  │   │   │   └── sub-01_ses-01_task-nback_bp-heart_vp-fourChamber_sbref.nii.gz
│  │   │   ├── dwi
│  │   │   │   ├── sub-control01_ses-01_bp-brain_vp-ax_dwi.nii.gz
│  │   │   │   ├── sub-control01_ses-01_bp-brain_vp-ax_dwi.bval
│  │   │   │   └── sub-control01_ses-01_bp-brain_vp-ax_dwi.bvec
│  │   │   ├── fmap
│  │   │   │   ├── sub-control01_ses-01_bp-brain_vp-sag_phasediff.nii.gz
│  │   │   │   ├── sub-control01_ses-01_bp-brain_vp-sag_phasediff.json
│  │   │   │   └── sub-control01_ses-01_bp-brain_vp-sag_magnitude1.nii.gz
│  │   │   └── pwi
│  │   │       ├── sub-control01_ses-01_bp-brain_vp-ax_pwi.nii.gz
│  │   │       └── sub-control01_ses-01_bp-brain_vp-ax_pwi.json
│  │   ├── mg
│  │   │   ├── Sub-control01_ses-01_bp-breast_vp-cc_mg.nii.gz
│  │   │   └── Sub-control01_ses-01_bp-breast_vp-mlo_mg.nii.gz
│  │   ├── rx
│  │   │   ├── Sub-control01_ses-01_bp-chest_vp-ap_dx.nii.gz
│  │   │   └── Sub-control01_ses-01_bp-chest_vp-ll_dx.nii.gz
│  │   ├── ct
│  │   │   ¦
│  │   │   └── ...
│  │   └── eco
│  │   │   ¦
│  │   │   └── ...
│  │   ├── "others files and folder. OPTIONAL"
│  │   └── sub-control01_scans.tsv
│  ├── ses-02
│  │   ├── ...
├── sub-02
│   ¦
│   └── ...
├── code
│   ├── Deface.py
│   ¦
│   └── segmentationSpinalCord.py
├── derivatives
├── README
├── participants.tsv
├── dataset_description.json
└── CHANGES
</code>
</pre>
</div>

<a id='mod'></a>
## 2.3.1.Label modality_label for MRI
Anatomical (structural) data acquired for a participant. In brain imaging, the modalities currently supported by BIDS are used, they include:


<table class="tg">
  
  <tr>
    <th class="tg-us36">Name</th>
    <th class="tg-c3ow">modality_label</th>
    <th class="tg-us36">Description</th>
  </tr>
  <tr>
    <td class="tg-dc35">T1 weighted<br></td>
    <td class="tg-abip">T1w</td>
    <td class="tg-dc35"></td>
  </tr>
  <tr>
    <td class="tg-us36">T2 weighted<br></td>
    <td class="tg-c3ow">T2w</td>
    <td class="tg-us36"></td>
  </tr>
  <tr>
    <td class="tg-dc35">T1 Rho map<br></td>
    <td class="tg-abip">T1rho<br></td>
    <td class="tg-dc35">Quantitative T1rho brain imaging <br><a href="http://www.ncbi.nlm.nih.gov/pubmed/24474423)">[URL 1]</a> and <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4346383/)">[URL 2]</a><br></td>
  </tr>
  <tr>
    <td class="tg-us36">T1 map<br></td>
    <td class="tg-c3ow">T1map</td>
    <td class="tg-us36">quantitative T1 map<br></td>
  </tr>
  <tr>
    <td class="tg-dc35">T2 map<br></td>
    <td class="tg-abip">T2map</td>
    <td class="tg-dc35">quantitative T2 map<br></td>
  </tr>
  <tr>
    <td class="tg-us36">T2*</td>
    <td class="tg-c3ow">T2star</td>
    <td class="tg-us36">High resolution T2* image<br></td>
  </tr>
  <tr>
    <td class="tg-dc35">FLAIR</td>
    <td class="tg-abip">FLAIR</td>
    <td class="tg-dc35"></td>
  </tr>
  <tr>
    <td class="tg-us36">Proton density<br></td>
    <td class="tg-c3ow">PD</td>
    <td class="tg-us36"></td>
  </tr>
  <tr>
    <td class="tg-dc35">Proton density map<br></td>
    <td class="tg-abip">PDmap<br><br></td>
    <td class="tg-dc35"></td>
  </tr>
  <tr>
    <td class="tg-us36">Combined PD/T2<br></td>
    <td class="tg-c3ow">PDT2</td>
    <td class="tg-us36"></td>
  </tr>
  <tr>
    <td class="tg-dc35">Inplane T1<br></td>
    <td class="tg-dc35">inplaneT1</td>
    <td class="tg-dc35">T1-weighted anatomical image matched to functional acquisition<br></td>
  </tr>
  <tr>
    <td class="tg-us36">Inplane T2<br></td>
    <td class="tg-us36">inplaneT2</td>
    <td class="tg-us36">T2-weighted anatomical image matched to functional acquisition<br></td>
  </tr>
  <tr>
    <td class="tg-dc35">Angiography<br></td>
    <td class="tg-dc35">angio</td>
    <td class="tg-dc35"></td>
  </tr>
</table>
<div style='text-align:center;'>
Table 2:  The modalities currently admitted in BIDS.
</div>

<a id='seq'></a>
## 2.3.2. Label sequence_label for MRI

MR structural data can be acquired with different parameter values. To represent said data, the Extension Proposal BIDS 1 ([BEP001](https://docs.google.com/document/d/1QwfHyBzOyFWOLO4u_kkojLpUhW0-4_M7Ubafu9Gf4Gg/edit#)) is used: Structural acquisitions that include multiple contrasts (multiple echo, investment angle, investment time), in this document you can find the keywords and the syntax used.

Next, Possible sequences of labels describing the sequences used in obtaining images included in BEP001:


<table class="tg">
  <tr>
    <th class="tg-us36">Name</th>
    <th class="tg-c3ow">Sequence_label<br></th>
    <th class="tg-us36">Description</th>
  </tr>
  <tr>
    <td class="tg-dc35">Driven Equilibrium Single-Pulse Observation of T1<br></td>
    <td class="tg-abip">despot1</td>
    <td class="tg-dc35"><br><br>Also known as the Variable Flip-Angle (VFA)<br><br> <br><br></td>
  </tr>
  <tr>
    <td class="tg-us36">Driven Equilibrium Single-Pulse Observation of T2<br></td>
    <td class="tg-c3ow">despot2<br></td>
    <td class="tg-us36"></td>
  </tr>
  <tr>
    <td class="tg-dc35">(Multi-echo) Flash <br></td>
    <td class="tg-abip">flash</td>
    <td class="tg-dc35"></td>
  </tr>
  <tr>
    <td class="tg-us36">(Multi-echo) Magnetization Prepared (2) Rapid Acquisition Gradient-Echo(es)<br></td>
    <td class="tg-c3ow">mprage</td>
    <td class="tg-us36"></td>
  </tr>
  <tr>
    <td class="tg-dc35">Fluid Attenuation Inversion Recovery<br></td>
    <td class="tg-abip">flair</td>
    <td class="tg-dc35"></td>
  </tr>
  <tr>
    <td class="tg-us36">Fast Spin-Echo<br></td>
    <td class="tg-c3ow">tse<br></td>
    <td class="tg-us36">(Includes Spin-Echo techniques like SPACE/CUBE/VISTA)<br></td>
  </tr>
  <tr>
    <td class="tg-dc35">Spin Echo<br></td>
    <td class="tg-abip">se</td>
    <td class="tg-dc35"></td>
  </tr>
</table>
<div style='text-align:center;'>
Table 3:  The sequences currently admitted in BEP001
</div>

MIDS incorporates the following sequences and techniques:


<table class="tg">
  <tr>
    <th class="tg-us36">Name</th>
    <th class="tg-c3ow">Sequence_label / Techniques_label <br></th>
    <th class="tg-us36">Description</th>
  </tr>
  <tr>
    <td class="tg-dc35">Short-TI Inversion Recovery<br></td>
    <td class="tg-abip">stir</td>
    <td class="tg-dc35"></td>
  </tr>
  <tr>
    <td class="tg-us36">HASTE/SS-FSE<br></td>
    <td class="tg-c3ow">haste</td>
    <td class="tg-us36"><a href="http://mriquestions.com/hastess-fse.html)">SSFSE or HASTE</a> sequence is one of the ultrafast sequences and it enables us to<br>acquire whole MR data (k-space) in a single rf excitation or single shot.<br><br><br><br></td>
  </tr>
  <tr>
    <td class="tg-dc35">Magnetization transfer<br></td>
    <td class="tg-abip">T1mt, T2mt<br></td>
    <td class="tg-dc35">Magnetization transfer imaging (<a href="http://mriquestions.com/mt-imagingcontrast.html)">MTI</a>) is a technique by which radiofrequency (RF) energy is applied exclusively to the bound pool using specially designed MT pulse(s).<br><br><br>The relative difference in signal between two adjacent tissues (A and B) is known as magnetization transfer contrast (MTC).<br><br><br><br><br></td>
  </tr>
</table>
<div style='text-align:center;'>
Table 4:  The sequences and techniques currently admitted in MIDS
</div>

<a id='labels'></a>
## 2.3.3. Labels for Medical Imaging Modalities

Below the different modalities of medical images, classified by the energy used in the acquisition, together with the DICOM Modes that belong to said categories:


<table class="tg">
  <tr>
    <th class="tg-us36">Modality of medical image<br></th>
    <th class="tg-c3ow">Modality label of Medical image<br>/mod-&lt;modality_medical_image_label&gt;</th>
    <th class="tg-us36">DICOM Modality.<br>See Section <a href="http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.3.html#sect_C.7.3.1.1.100">[C.7.3.1.1.1]</a> <br>Modality (0008,0060)<br></th>
    <th class="tg-us36">DICOM Modality label<br>&lt;modality_Dicom&gt;<br></th>
  </tr>
  <tr>
    <td class="tg-abip" rowspan="15">General_Radiology<br><br></td>
    <td class="tg-abip" rowspan="15">rx</td>
    <td class="tg-dc35">Computed Radiography<br></td>
    <td class="tg-dc35">cr<br></td>
  </tr>
  <tr>
    <td class="tg-us36">Bone Densitometry (X-Ray)<br></td>
    <td class="tg-us36">bmd</td>
  </tr>
  <tr>
    <td class="tg-dc35">X-Ray Angiography<br></td>
    <td class="tg-dc35">xa</td>
  </tr>
  <tr>
    <td class="tg-us36">Digital Radiography<br></td>
    <td class="tg-us36">dx<br></td>
  </tr>
  <tr>
    <td class="tg-dc35">Computed Tomography<br></td>
    <td class="tg-dc35">ct</td>
  </tr>
  <tr>
    <td class="tg-us36">Intra-Oral Radiography<br></td>
    <td class="tg-us36">io</td>
  </tr>
  <tr>
    <td class="tg-dc35">Mammography<br></td>
    <td class="tg-dc35">mg</td>
  </tr>
  <tr>
    <td class="tg-us36">Videofluorography - (VF)**<br></td>
    <td class="tg-us36">rf</td>
  </tr>
  <tr>
    <td class="tg-dc35">Radio Fluoroscopy<br></td>
    <td class="tg-dc35">rf</td>
  </tr>
  <tr>
    <td class="tg-us36">Cinefluorography - (CF)**<br></td>
    <td class="tg-us36">rf</td>
  </tr>
  <tr>
    <td class="tg-dc35">Digital fluoroscopy - (DF)**<br></td>
    <td class="tg-dc35">rf</td>
  </tr>
  <tr>
    <td class="tg-us36">Panoramic X-Ray<br></td>
    <td class="tg-us36">px</td>
  </tr>
  <tr>
    <td class="tg-dc35">Radiographic imaging (conventional film/screen)<br></td>
    <td class="tg-dc35">rg</td>
  </tr>
  <tr>
    <td class="tg-us36">X-Ray Angiography<br></td>
    <td class="tg-us36">xa</td>
  </tr>
  <tr>
    <td class="tg-dc35">Digital Subtraction Angiography - (DS)**<br></td>
    <td class="tg-dc35">xa</td>
  </tr>
  <tr>
    <td class="tg-us36" rowspan="5">Radiotherapy<br></td>
    <td class="tg-c3ow" rowspan="5">rt<br></td>
    <td class="tg-us36">Radiotherapy Image<br></td>
    <td class="tg-us36">rtimage</td>
  </tr>
  <tr>
    <td class="tg-dc35">Radiotherapy Plan<br></td>
    <td class="tg-dc35">rtplan</td>
  </tr>
  <tr>
    <td class="tg-us36">RT Treatment Record<br></td>
    <td class="tg-us36">rtrecord</td>
  </tr>
  <tr>
    <td class="tg-dc35">Radiotherapy Structure Set<br></td>
    <td class="tg-dc35">rtstruct</td>
  </tr>
  <tr>
    <td class="tg-us36">Radiotherapy Dose<br></td>
    <td class="tg-us36">rtdose</td>
  </tr>
  <tr>
    <td class="tg-dc35" rowspan="2">Magnetic Resonance<br></td>
    <td class="tg-abip" rowspan="2">mr<br></td>
    <td class="tg-dc35">Magnetic resonance angiography-<br> (MA)**<br></td>
    <td class="tg-dc35">mr*<br></td>
  </tr>
  <tr>
    <td class="tg-us36">Magnetic resonance spectroscopy- <br>(MS)**<br></td>
    <td class="tg-us36">mr<br></td>
  </tr>
  <tr>
    <td class="tg-dc35" rowspan="5">Ultrasound<br></td>
    <td class="tg-abip" rowspan="5">us<br></td>
    <td class="tg-dc35">Echocardiography  - (EC)**<br></td>
    <td class="tg-dc35">us</td>
  </tr>
  <tr>
    <td class="tg-us36">Color flow Doppler - (CD)**<br></td>
    <td class="tg-us36">us</td>
  </tr>
  <tr>
    <td class="tg-dc35">Cystoscopy<br></td>
    <td class="tg-dc35">cs</td>
  </tr>
  <tr>
    <td class="tg-us36">Duplex Doppler - (DD)**<br></td>
    <td class="tg-us36">us</td>
  </tr>
  <tr>
    <td class="tg-dc35">Intravascular Ultrasound<br></td>
    <td class="tg-dc35">ivus</td>
  </tr>
  <tr>
    <td class="tg-us36" rowspan="8">Ophthalmic</td>
    <td class="tg-us36" rowspan="8">oph</td>
    <td class="tg-us36">Autorefraction</td>
    <td class="tg-us36">ar</td>
  </tr>
  <tr>
    <td class="tg-dc35">Ophthalmic Axial Measurements<br></td>
    <td class="tg-dc35">oam</td>
  </tr>
  <tr>
    <td class="tg-us36">Ophthalmic Photography<br></td>
    <td class="tg-us36">op<br></td>
  </tr>
  <tr>
    <td class="tg-dc35">Ophthalmic Mapping<br></td>
    <td class="tg-dc35">opm<br></td>
  </tr>
  <tr>
    <td class="tg-us36">Ophthalmic Tomography<br></td>
    <td class="tg-us36">opt<br></td>
  </tr>
  <tr>
    <td class="tg-dc35">Ophthalmic Visual Field<br></td>
    <td class="tg-dc35">opv</td>
  </tr>
  <tr>
    <td class="tg-us36">Visual Acuity<br></td>
    <td class="tg-us36">va</td>
  </tr>
  <tr>
    <td class="tg-dc35">Optical Coherence Tomography (non-Ophthalmic)<br></td>
    <td class="tg-dc35">oct<br></td>
  </tr>
  <tr>
    <td class="tg-yw4l" rowspan="4">Light</td>
    <td class="tg-yw4l" rowspan="4">light</td>
    <td class="tg-yw4l">Intravascular Optical Coherence Tomography<br></td>
    <td class="tg-yw4l">ivoct</td>
  </tr>
  <tr>
    <td class="tg-b7b8">Endoscopy</td>
    <td class="tg-b7b8">es</td>
  </tr>
  <tr>
    <td class="tg-yw4l">Slide Microscopy<br></td>
    <td class="tg-yw4l">sm</td>
  </tr>
  <tr>
    <td class="tg-b7b8">General Microscopy<br></td>
    <td class="tg-b7b8">gm</td>
  </tr>
  <tr>
    <td class="tg-yw4l" rowspan="2">Electrical activities<br></td>
    <td class="tg-yw4l" rowspan="2">elect</td>
    <td class="tg-yw4l">Electrocardiography<br></td>
    <td class="tg-yw4l">ecg*<br></td>
  </tr>
  <tr>
    <td class="tg-b7b8">Cardiac Electrophysiology<br></td>
    <td class="tg-b7b8">eps</td>
  </tr>
</table>

<div style='text-align:center;'>
Table 5:  Classification of the equipment used to acquire the images, according to the classification of the medical image modalities.
</div>


<b id="f1">2</b>  "[ * ]" MRI modalities existing in BIDS and expanded in MIDS for MRI, the <modality_label> tags must be placed for these cases [↩](#a1)

<b id="f1">3</b>  "[ ** ]" Retired modalities incorporated in the DICOM modality label [↩](#a1)
<a id='tab'></a>
## 2.4 Tabular files
<a id='parti'></a>
#### 2.4.1. Participants description table (Sub-\<participant_label\>.tsv)

<div>
<pre>
<code>
Data/
├── sub-&ltparticipant_label&gt[_ses-&ltsesion-label&gt]
├── sub- ...
¦
└── Participants.tsv

</code>
</pre>
</div>

This file is REQUIRED. The purpose of this file is to describe properties of the participants such as age, handedness, sex, etc. In the case of single session studies, this file has one compulsory column participant_id that consists of sub-<participant_label>, followed by a list of optional columns describing participants. Each participant needs to be described by one and only one row.

The columns of the participants description table stored in “participants.Tsv” are:


<table class="tg">
  <tr>
    <th class="tg-us36">Participant</th>
    <th class="tg-c3ow">REQUIRED. Tag for a patient in MIDS. Cases where the pseudonymization is a long and confusing identification are possible. This would make it necessary to generate a more compact identifier (Participant)<br></th>
  </tr>
  <tr>
    <td class="tg-b7b8">ID Pseudonymization<br></td>
    <td class="tg-b7b8">REQUIRED. Unique identifier of a patient's properly pseudonymized data <br></td>
  </tr>
  <tr>
    <td class="tg-yw4l">Health area<br></td>
    <td class="tg-yw4l">OPTIONAL. The Health Area is the administrative district that groups a group of health centers and primary care professionals under their organizational and functional dependency.<br>You can combine data from all sites/centers into one dataset. To identify which site each subjects comes from; in this case, it lists all health centers in which a patient has had a medical image acquired.<br><br>See: <a href="http://www.msc.es/ciudadanos/prestaciones/centrosServiciosSNS/hospitales/introduccionCentro.htm">Basic information of the primary care centers available to the National Health System, Spain.</a> <br></td>
  </tr>
  <tr>
    <td class="tg-b7b8">Modality Dicom<br></td>
    <td class="tg-b7b8">OPTIONAL. List all types of equipment that acquired the original data used to create the images for this patient. (Tag Dicom (0008,0060))<br></td>
  </tr>
  <tr>
    <td class="tg-yw4l">Body Parts<br></td>
    <td class="tg-yw4l">OPTIONAL. List all Terms for Body Part Examined in this patient,Dicom (0018,0015)<br></td>
  </tr>
  <tr>
    <td class="tg-b7b8">Age<br></td>
    <td class="tg-b7b8">OPTIONAL. Age at which the last session was performed<br></td>
  </tr>
  <tr>
    <td class="tg-yw4l">Patient's Sex<br></td>
    <td class="tg-yw4l">OPTIONAL. Sex of the patient<br></td>
  </tr>
  <tr>
    <td class="tg-rm6r">...<br></td>
    <td class="tg-rm6r">...</td>
  </tr>
</table>

Example:


<table class="tg">
  <tr>
    <th class="tg-us36">Participant<br></th>
    <th class="tg-us36">ID_</th>
    <th class="tg-yw4l">Health areas</th>
    <th class="tg-yw4l">Modality Dicom <br></th>
    <th class="tg-yw4l">Body parts </th>
  </tr>
  <tr>
    <td class="tg-b7b8">participant_label<br></td>
    <td class="tg-b7b8">123…</td>
    <td class="tg-b7b8">ds05</td>
    <td class="tg-b7b8">[MG, MR]<br></td>
    <td class="tg-b7b8">[ [BREAST],[LSSPINE,BRAIN] ]<br></td>
  </tr>
  <tr>
    <td class="tg-hjji">...<br></td>
    <td class="tg-hjji">...</td>
    <td class="tg-24i8">...</td>
    <td class="tg-24i8">...</td>
    <td class="tg-24i8">...</td>
  </tr>
</table>
<a id='ses'></a>
#### 2.4.2. Session description table (sub-\<tparticipant_label\>_sessions.tsv)
<div>
<pre>
<code>
Data/
├── sub-&ltparticipant_label&gt/
│   ├──[_ses-&ltsesion-label&gt]/
¦   ¦
¦   ¦
│   └──sub-&ltparticipant_label&gt_sessions.tsv
└── Participants.tsv

</code>
</pre>
</div>

This file is RECOMMENDED as it provides the information referring to all the sessions of the patient, such as age at which the session was performed, procedures, and diagnoses made. Missing values MUST be indicated with “n/a”.

The columns of the session description table stored in “sub-\<tparticipant_label\>.tsv” are:


<table class="tg">
  <tr>
    <th class="tg-us36">Session<br>	<br><br></th>
    <th class="tg-us36">REQUIRED.<br></th>
  </tr>
  <tr>
    <td class="tg-b7b8">Age</td>
    <td class="tg-b7b8">OPTIONAL. Age at which the session was performed.<br></td>
  </tr>
  <tr>
    <td class="tg-yw4l">ICD version<br><br></td>
    <td class="tg-yw4l">REQUIRED if “all diagnostics” or “all procedures” are filled. The ICD is the acronym of the “International Classification of Diseases”.  We currently use the electronic version eCIE10ES, corresponding to the Spanish version<br><br>You can check the current classification in: <a href="https://eciemaps.msssi.gob.es/ecieMaps/browser/metabuscador.html">Electronic edition search engine of the ICD-10-ES.</a></br> <br>For more information: <a href="http://www.who.int/classifications/icd/en/">Classification of Diseases (ICD), World Health Organization. </a></br></td>
  </tr>
  <tr>
    <td class="tg-b7b8">All diagnostics<br></td>
    <td class="tg-b7b8">OPTIONAL. Tag or list of tags that represents a patient diagnosis code in the ICD version. <br><br>(e.g., [[M80.08XA], [C34.90],[C79.51],[F17.210]] represents, osteoporosis related to age with current pathological fracture, vertebrae (s), initial contact for fracture and other secondary diagnosis)<br><br><br><br><br><br></td>
  </tr>
  <tr>
    <td class="tg-yw4l">All procedures<br></td>
    <td class="tg-yw4l">OPTIONAL. Tags or list of tags of the procedures in ICD version represented during recognition.<br><br>(e.g.[[BR39ZZZ],[0BJ08ZZ],[BW25Y0Z],[BR39ZZZ]], represents, magnetic resonance image without contrast to the lumbar spine and other secondary probes)<br><br><br><br><br><br></td>
  </tr>
  <tr>
    <td class="tg-rm6r">...<br></td>
    <td class="tg-rm6r">...</td>
  </tr>
</table>

Example:

<table class="tg">
  <tr>
    <th class="tg-us36">Session<br><br></th>
    <th class="tg-us36">Age<br></th>
    <th class="tg-yw4l">ICD version<br></th>
    <th class="tg-yw4l">All diagnostics<br><br></th>
    <th class="tg-yw4l">All procedures<br></th>
  </tr>
  <tr>
    <td class="tg-b7b8">Ses-1</td>
    <td class="tg-b7b8">70</td>
    <td class="tg-b7b8">CIE-10-MCv33.0<br></td>
    <td class="tg-b7b8">[[G12.20],[E11.9], [I10],[E78.5]]<br></td>
    <td class="tg-b7b8">[[009U3ZX],[BR39ZZZ]]</td>
  </tr>
  <tr>
    <td class="tg-yw4l">Ses-2</td>
    <td class="tg-yw4l">70</td>
    <td class="tg-yw4l">CIE-10-MCv33.0</td>
    <td class="tg-yw4l">[[M51.16],[G82.22]]<br></td>
    <td class="tg-yw4l">[[009U3ZX],[BR39ZZZ]]</td>
  </tr>
  <tr>
    <td class="tg-b7b8">Ses-3</td>
    <td class="tg-b7b8">71</td>
    <td class="tg-b7b8">CIE-10-MCv33.0</td>
    <td class="tg-b7b8">[[C34.90],[C79.51],[F17.210]]</td>
    <td class="tg-b7b8">[[0BJ08ZZ],[BW25Y0Z], [BR39ZZZ]]<br></td>
  </tr>
  <tr>
    <td class="tg-yw4l">Ses-4</td>
    <td class="tg-yw4l">72</td>
    <td class="tg-yw4l">CIE-10-MCv33.0<br></td>
    <td class="tg-yw4l">[S32.028A],[X58.XXXA]]</td>
    <td class="tg-yw4l">[[0QS004Z],[0RGA0A1], [BR39ZZZ]]<br></td>
  </tr>
  <tr>
    <td class="tg-rm6r">...<br></td>
    <td class="tg-rm6r">...</td>
    <td class="tg-0t3l">...</td>
    <td class="tg-0t3l">...</td>
    <td class="tg-0t3l">...</td>
  </tr>
</table>

<a id='scans'></a>
#### 2.4.3. Scans description table(Sub-<participant_label>_scans.tsv)

This file is REQUIRED. In this tsv, all concerned data at the scan can be refilled in this table. One option is complete the table with more relevant DICOM tags for this study. The only required column is an identification that is the relative directory to the image.

<div>
<pre>
<code>
Data/
├── sub-&ltparticipant_label&gt/
│   ├──[_ses-&ltsesion-label&gt]/
│   │   ├──[mod/]
¦   ¦   ¦
¦   ¦   └── sub-&ltparticipant_label&gt_scans.tsv
│   └──sub-&ltparticipant_label&gt.tsv
└── Participants.tsv

</code>
</pre>
</div>

example:


<table class="tg">
  <tr>
    <th class="tg-us36">Filename<br></th>
    <th class="tg-us36">body part slides plane<br><br></th>
    <th class="tg-us36">ICD Series Description (0008,103E)<br></th>
    <th class="tg-us36">Patient's Age (0010,1010)<br></th>
    <th class="tg-us36">Magnetic Field Strength (0018,0087)<br></th>
    <th class="tg-n1qb">...</th>
  </tr>
  <tr>
    <td class="tg-dc35">rm/anat/sub-control01_ses-1_acq-1_run-2_sag_T1.nii.gz<br></td>
    <td class="tg-dc35">lsspine</td>
    <td class="tg-dc35">SAGT1<br></td>
    <td class="tg-dc35">90<br></td>
    <td class="tg-dc35">1.5<br></td>
    <td class="tg-7e76">...</td>
  </tr>
  <tr>
    <td class="tg-us36">rx/sub-control01_ses-1_acq-1_run-1_dx.nii.gz<br></td>
    <td class="tg-n1qb">...</td>
    <td class="tg-n1qb">...</td>
    <td class="tg-n1qb">...</td>
    <td class="tg-n1qb">...</td>
    <td class="tg-n1qb">...</td>
  </tr>
  <tr>
    <td class="tg-z5wk">...<br></td>
    <td class="tg-z5wk">...</td>
    <td class="tg-7e76">...</td>
    <td class="tg-7e76">...</td>
    <td class="tg-7e76">...</td>
    <td class="tg-7e76">...</td>
  </tr>
</table>


<a id='references'></a>
# References

Adams MC., Turkington TG., Wilson JM., Wong TZ. (2010). A systematic review of the factors affecting accuracy of SUV measurements. AJR American journal of roentgenology 195:310-320.

Bennett CM., Miller MB. (2010) How reliable are the results from functional magnetic resonance imaging? Annals of the New York Academy of Sciences 1191:133-155.

Mildenberger, P., Eichelberg, M., & Martin, E. (2002). Introduction to the DICOM standard. European radiology, 12(4), 920-927.

Gorgolewski, K. J., Auer, T., Calhoun, V. D., Craddock, R. C., Das, S., Duff, E. P., ... & Handwerker, D. A. (2016). The brain imaging data structure, a format for organizing and describing outputs of neuroimaging experiments. Scientific Data, 3, 160044.

Elmaoğlu, M., & Çelik, A. (2011). MRI handbook: MR physics, patient positioning, and protocols. Springer Science & Business Media.

DE ESPAÑA, J. C. I. R. (1999). Ley Orgánica 15/1999, de 13 de diciembre, de Protección de Datos de Carácter Personal. Bol Del Estado, 404

Serrano, J. M. S. (2013). CLOUD CEIB I+ D. Sistema de gestión y extracción de conocimiento de la imágen médica (Doctoral dissertation, Universitat d'Alacant-Universidad de Alicante).

## Code availability.

 All software for building and running the BIMCV and reading metadata of the BIMCV data sets is open source and available at https://github.com/BIMCV-CSUSP/MIDS. The custom scripts used to combine metadata into a MIDS files structure are available at https://github.com/BIMCV-CSUSP/MIDS/tree/master/XNAT2MIDS.

 ## Data availability.

 All data sets described in this paper are available at https://github.com/BIMCV-CSUSP/MIDS/tree/master/data

 ## Acknowledgement.

 The MIDS project was funded by the Regional Ministry of Health (FEDER), and Horizon 2020 Framework Programme of the European Union under grant agreement 688945 (Euro-BioImaging Prep Phase II) Euro Bioimaging WP6. D6.3. Task 6.4.


 ## Rights and permissions.

 <a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>., which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license, and indicate if changes were made. The images or other third party material in this article are included in the article's Creative Commons license, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons license and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
