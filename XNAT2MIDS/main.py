#!/usr/bin/env  python   #iniciaize enviroment
# -*- coding: utf-8 -*-.
u"""
Subdirección General de Sistemas de Información para la Salud

Centro de Excelencia e Innovación Tecnológica de Bioimagen de la Conselleria de Sanitat

http://ceib.san.gva.es/

María de la Iglesia Vayá -> delaiglesia_mar@gva.es or miglesia@cipf.es

Jose Manuel Saborit Torres -> jmsaborit@cipf.es

Jhon Jairo Saenz Gamboa ->jsaenz@cipf.es

Joaquim Ángel Montell Serrano -> jamontell@cipf.es

---

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.

---

Prerequisites

Python --version >= 3.5

Description:
    This aplication allow the user to download one project on XNAT and
    transform these project in MIDS format

    There are 2 funtions in this code:
        download one project from xnat aplicatión:
        arguments:
            Prefix  -w --web PAGE_WEB        1) The ULR page where XNAT is.
            Prefix	-p --project [PROJECTS]  2) The project name to download
            Prefix	-i --input PATH	         3) the directfory where the files
                                                will be downloaded
            Prefix  -u --user [USER]         4) The username to loggin in XNAT
                                                If not write a username, It
                                                loggin as guest.

        Convert the xnat directories of the project in MIDS format:
        arguments:
            Prefix	-i --input	PATH   1) the directfory where the files will
                                        be downloaded
            Prefix	-o --output	PATH   2) Directory where the MIDS model
                                        is applied.
"""

###############################################################################
# Imports
###############################################################################

import os
import errno
import time
import numpy as np
import sys
import getpass
import argparse
import time
import chardet

from collections import defaultdict
from datetime import datetime
from calendar import isleap
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import Bash_functions.bash_exe as bash
import IO_Functions.file_class as file_funtions
import IO_Functions.io_json as io_json
import IO_Functions.io_objects as io_objects
import download_from_xnat as dfx
# # Next step recognize the modality
# from lib.scan_tagger.scans_tagger_v2 import tagger
###############################################################################
# Global Variables
###############################################################################

# GLOBAL statement of the path where the main program is executed
path_programme = file_funtions.FileInfo(os.path.realpath(__file__))

# GLOBAL statement of the path where the objects python and csv's is stored
dictionary_path = path_programme.path + ".python_objects" + os.sep
log_path = path_programme.path + ".log/"
# GLOBAL statement of the project which is download
project_id_list = []

# Path where xnat files are stored
xnat_data_path = ""

# Path where the BIDS model is applied with xnat cases
mids_data_path = ""

# GLOBAL statement of dictionaries used for management
scans_dict = dict()

# GLOBAL statement that store user of xnat session
user = ""


###############################################################################
# objects
###############################################################################

class procedures(object):
    """
        Python object that collects the procedures to take an element and place
        it where it corresponds.
    """

    def __init__(self):
        r"""Function init to procedures class."""
        super(procedures, self).__init__()
        self.dict_indexes = {
            "T2w": 1, "T1w": 1, "T2*_Spine": 1, "angio": 1,
            "pwi": 1, "SWI": 1, "PDT2": 1, "T2star": 1,
            "PD": 1, "flair": 1, "gre": 1, "stir": 1, "tse": 1,
            "mprage": 1, "haste": 1, "flash": 1, "dwi": 1, "unknow": 1
        }


    def unknow_procedure(self, subject_name, num_session, scan, iop, mids_path,
                         subject_path, dicom_json):
        """
            Function that copies the elements to the unknown folder of the
            mids derivatives folder.
        """
        # This is a counter for several nifties in one adquisition
        acq_index=1
        # mount the name of dicom file.
        dicom_name = (subject_name + "_" + num_session
                      + "_acq-" + str(acq_index)
                      + "_run-" + str(self.dict_indexes["unknow"])
                      + (("_vp-" + iop) if iop is not None else "")
                      + "_" + scan + ".json")
        # Mount the new path to copy the files and create it if not exist
        new_path_mids = (mids_path.filepath
                         + os.sep + subject_path + num_session + os.sep
                         + "unkonw" + os.sep)
        if not os.path.exists(new_path_mids):
            bash.bash_command("mkdir -p " + new_path_mids)
        # Copy dicom file in new path
        bash.bash_command("cp " + dicom_json.filepath + " " + new_path_mids
                          + dicom_name)
        # Search all nifti files in the old folder and sort them
        out, err = bash.bash_command("find " + dicom_json.path
                                     + ' -type f -not -iname "*.json"')
        nifti_files = sorted(out.split('\n'))
        # for each nifti file...
        for nifti_file in nifti_files[1:]:
            # mount the new name
            nii_name = (subject_name + "_" + num_session
                        + "_acq-" + str(acq_index)
                        + "_run-" + str(self.dict_indexes["unknow"])
                        + (("_vp-" + iop) if iop is not None else "")
                        + "_" + scan + ".nii.gz")
            # copy the nifti file in the new path
            bash.bash_command("cp " + nifti_file + " " + new_path_mids
                              + nii_name)

            acq_index += 1
        # Aumnent in one unit the run of unknow modality
        self.dict_indexes["unknow"] += 1

    def anatomic_procedure(self, subject_name, num_session, modality_label,
                           iop, mids_path, subject_path, dicom_json):
        """
            Function that copies the elements to the anatomical folder of
            the mids.
        """
        # This is a counter for several nifties in one adquisition
        acq_index = 1
        # mount the name of dicom file.
        dicom_name = (
            subject_name + "_" + num_session + "_acq-"
            + str(acq_index) + "_run-"
            + str(self.dict_indexes[modality_label])
            + (("_vp-" + iop) if iop is not None else "")
            + "_"+modality_label+".json"
            )
        # Mount the new path to copy the files and create it if not exist
        new_path_mids = (
            mids_path.filepath + subject_path + num_session + os.sep
            + "anat" + os.sep
            )
        if not os.path.exists(new_path_mids):
            bash.bash_command("mkdir -p " + new_path_mids)
        # Copy dicom file in new path
        bash.bash_command("cp " + dicom_json.filepath + " " + new_path_mids
                          + dicom_name)
        # Search all nifti files in the old folder and sort them
        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
        nifti_files = sorted(out.split('\n'))
        # Copy nifty files in new path with their correct names
        for nifti_file in nifti_files[1:]:
            # mount the new name
            nii_name = (
                subject_name + "_" + num_session + "_acq-"
                + str(acq_index)
                + "_run-" + str(self.dict_indexes[modality_label])
                + (("_vp-" + iop) if iop is not None else "")
                + "_" + modality_label+".nii.gz"
                )
            # copy the nifti file in the new path
            bash.bash_command("cp " + nifti_file + " " + new_path_mids
                              + nii_name)

            acq_index += 1
        # Aumnent in one unit the run of one modality
        self.dict_indexes[modality_label] += 1

    def perfusion_procedure(self, subject_name, num_session, modality_label,
                            iop, mids_path, subject_path, dicom_json):
        """Copy the elements to the perfusion folder of the mids."""
        # This is a counter for several nifties in one adquisition
        acq_index = 1
        # mount the new dicom name.
        dicom_name = (subject_name + "_" + num_session + "_acq-"
                      + str(acq_index) + "_run-"
                      + str(self.dict_indexes[modality_label])
                      + (("_vp-" + iop) if iop is not None else "")
                      + "_" + modality_label+".json")
        # Mount the new path to copy the files and create it if not exist
        new_path_mids = (mids_path.filepath + subject_path
                         + num_session + os.sep + "perfusion" + os.sep)
        if not os.path.exists(new_path_mids):
            bash.bash_command("mkdir -p " + new_path_mids)
        # copy the json file in the new path
        bash.bash_command("cp " + dicom_json.filepath + " " + new_path_mids
                          + dicom_name)
        # list all nifti files in the old path and sort them
        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
        nifti_files = sorted(out.split('\n'))
        # for each nifti...
        for nifti_file in nifti_files[1:]:
            # mount the new name
            nii_name = (subject_name + "_" + num_session + "_acq-"
                        + str(acq_index) + "_run-"
                        + str(self.dict_indexes[modality_label])
                        + (("_vp-" + iop) if iop is not None else "")
                        + "_" + modality_label + ".nii.gz")
            # copy the nifti file in the new path
            bash.bash_command("cp " + nifti_file + " " + new_path_mids
                              + nii_name)
            # add in one unit the acq variable
            acq_index += 1
        # add in one unit the run of one modality
        self.dict_indexes[modality_label] += 1

    def diffusion_procedure(self, subject_name, num_session, modality_label,
                            scan, iop, mids_path, subject_path, dicom_json):
        """Copy the elements to the diffusion folder of the mids."""
        # This is a counter for several nifties in one adquisition
        acq_index = 1
        # search the bval file
        out, err = bash.bash_command("ls " + dicom_json.path + "*.bval")
        bval_file = out.replace('\n', '')
        # if not exist bval file...
        if not os.path.exists(bval_file):
            # call the method "unknow_procedure"
            self.unknow_procedure(subject_name, num_session, scan,
                                  iop, mids_path, subject_path, dicom_json)
        else:
            # open the bval file
            with open(bval_file, "r") as handle:
                value = handle.readline().replace('\n', '')
                while ' ' in value:
                    value = value.replace(' ', '')
                if value == '0':
                    # call the method "unknow_procedure"
                    self.unknow_procedure(subject_name, num_session,
                                          scan, iop, mids_path, subject_path,
                                          dicom_json)
        out, err = bash.bash_command("ls " + dicom_json.path + "*.bvec")
        bvec_file = out.replace('\n', '')
        if not os.path.exists(bvec_file):
            # call the method "unknow_procedure"
            self.unknow_procedure(subject_name, num_session, scan,
                                  iop, mids_path, subject_path, dicom_json)
        # mount the new dicom name.
        dicom_name = (subject_name + "_" + num_session + "_acq-"
                      + str(acq_index) + "_run-"
                      + str(self.dict_indexes[modality_label])
                      + (("_vp-" + iop) if iop is not None else "")
                      + "_" + modality_label + "_dwi.json")
        bval_name = (subject_name + "_" + num_session
                     + "_acq-" + str(acq_index)
                     + "_run-" + str(self.dict_indexes[modality_label])
                     + (("_vp-" + iop) if iop is not None else "")
                     + "_" + modality_label + "_dwi.bval")
        bvec_name = (subject_name + "_" + num_session
                     + "_acq-" + str(acq_index)
                     + "_run-" + str(self.dict_indexes[modality_label])
                     + (("_vp-" + iop) if iop is not None else "")
                     + "_"+modality_label + "_dwi.bvec")
        new_path_mids = (mids_path.filepath + subject_path
                         + num_session + os.sep + "dwi" + os.sep)
        if not os.path.exists(new_path_mids):
            bash.bash_command("mkdir -p " + new_path_mids)
        bash.bash_command("cp " + dicom_json.filepath + " " + new_path_mids
                          + dicom_name)
        bash.bash_command("cp " + bval_file + " " + new_path_mids + bval_name)
        bash.bash_command("cp " + bvec_file + " " + new_path_mids + bvec_name)
        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
        nifti_files = sorted(out.split('\n'))
        for nifti_file in nifti_files[1:]:
            nii_name = (subject_name + "_" + num_session
                        + "_acq-" + str(acq_index)
                        + "_run-" + str(self.dict_indexes[modality_label])
                        + (("_vp-" + iop) if iop is not None else "")
                        + "_" + modality_label + ".nii.gz")
            bash.bash_command("cp " + nifti_file + " " + new_path_mids + nii_name)
            acq_index += 1
        # Aumnent in one unit the run of one modality
        self.dict_indexes[modality_label] += 1

    def reset_indexes(self):
        """Reset all values in dictionary of the atribute "dict_indexes"."""
        # self.dict_indexes={
        # "T2_Spine":1, "T1_Spine":1, "T2*_Spine":1, "T1flair_Spine":1,
        # "STIR_Spine":1, "T2_brain":1, "T1_brain":1, "T1flair_ brain":1,
        # "T1 MT":1, "T2star_brain":1, "FAST T2":1, "Perfusion":1, "3D TOF":1,
        # "T2-IR":1, "3DT1-IR":1, "PD":1, "3D PC Art/Ven":1, "3DT1":1,
        # "3DT2":1, "T2_RM":1, "T1_RM":1, "STIR_RM":1, "HASTE":1,
        #  "PD_":1, "STIR_Spine_Midas	":1, "T2flair_ brain":1, "Diffusion":1
        # }

        self.dict_indexes = {
            "T2w": 1, "T1w": 1, "T2*_Spine": 1, "angio": 1,
            "pwi": 1, "SWI": 1, "PDT2": 1, "T2star": 1,
            "PD": 1, "flair": 1, "gre": 1, "stir": 1, "tse": 1,
            "mprage": 1, "haste": 1, "flash": 1, "dwi": 1, "unknow": 1
        }

###############################################################################
# Functions
###############################################################################

def load_dictionary():
    """
    This function allows the user to load dictionary of clasificatión images
    """
    # the path where all data to create dictionary are stored
    path_dicc = (".python_objects/")
    # check if the dictionary exists. If exists ...
    if not os.path.exists(path_dicc+"etiquetadoMIDS.dict"):
        # Save the last modification and return the new dictionary
        print("The dictionary is being created...")
        last_modified = time.ctime(
            os.path.getmtime(path_dicc + "etiquetadoMIDS.csv")
            )
        io_objects.save_pickle(last_modified, path_dicc + "last_modify.ctime")
        return io_objects.csv_2_dict(path_dicc + "etiquetadoMIDS.csv", 1, ';')
    # If the dictionary exists ...
    else:
        # Check the last modify date in the file csv and the last storage
        last_modified = time.ctime(
            os.path.getmtime(path_dicc + "etiquetadoMIDS.csv")
            )
        last_modified_save = io_objects.load_pickle(path_dicc
                                                    + "last_modify.ctime")
        # If they are the same ...
        # print(str(last_modified) + "  <----->  " + str(last_modified_save))
        if last_modified == last_modified_save:
            # Return the dictionary
            print("The dictionary is being loaded...")
            return io_objects.load_pickle(path_dicc + "etiquetadoMIDS.dict")
        else:
            # Save the last modification and return the new dictionary
            print("The dictionary is being update...")
            last_modified = time.ctime(
                os.path.getmtime(path_dicc + "etiquetadoMIDS.csv")
                )
            io_objects.save_pickle(last_modified, path_dicc
                                   + "last_modify.ctime")
            return io_objects.csv_2_dict(path_dicc + "etiquetadoMIDS.csv",
                                         1, ';')

def file_plane(iop):
    """
        Calculate the type of plane with the tag image orientation patient
        in dicom metadata.
    """
    try:
        iop_int = list(map(float, iop.split("\\")))
    except ValueError as e:
        return None
    iop_round = [round(x) for x in iop_int]
    plane = np.cross(iop_round[0:3], iop_round[3:6])
    plane = [abs(x) for x in plane]
    if plane[0] == 1:
        # Sagittal
        return "sag"
    elif plane[1] == 1:
        # Coronal
        return "cor"
    elif plane[2] == 1:
        # Transverse / Axial
        return "ax"


def create_directorio_MIDS():
    """
    This function allows the user to convert the xnat directory to
    mids directory
    """

    procedure_class = procedures()
    global xnat_data_path, mids_data_path
    depth_path_xnat = xnat_data_path.depth + 2
    subject_id_count = 1
    for subjects_xnat in file_funtions.get_dirs(xnat_data_path.filepath):
        if depth_path_xnat == subjects_xnat.depth:
            # print(subjects_xnat.filepath)
            procedure_class.reset_indexes()
            subject_name = 'sub-' + str(subject_id_count)
            subject_id_count += 1
            for dicom_json in file_funtions.get_files(subjects_xnat.filepath):
                if dicom_json.match("*.json") and dicom_json.is_file:
                    linea = dicom_json.filepath.replace(
                        xnat_data_path.filepath, '')
                    nii_gz_list_path = linea.split('/')
                    department_path = nii_gz_list_path[0]
                    session = nii_gz_list_path[2]
                    scan = nii_gz_list_path[4].split('-')[1:]
                    scan = str.join('-', scan).lower()
                    subject_path = (department_path + os.sep
                                    + subject_name + os.sep)
                    session_number = session.split('-')
                    if len(session_number) == 1:
                        num_session = "ses-1"
                    else:
                        num_session = "ses-" + session_number[1]
                    values = scans_dict.get(scan, "unknow")
                    if values['Secuence_label'] != '':
                        value = values['Secuence_label']
                    elif values['modality_label_rm']:
                        value = values['modality_label_rm']
                    else:
                        value = 'unknow'

                    ###########################################################
                    # # Next step recognize the modality
                    # scanning_sequence = io_json.get_tag_dicom("(0018,0020)",
                    # dicom_json.filepath)["value"]
                    # repetition_time = io_json.get_tag_dicom("(0018,0080)",
                    # dicom_json.filepath)["value"]
                    # echo_time = io_json.get_tag_dicom("(0018,0081)",
                    # dicom_json.filepath)["value"]
                    # inversion_time = io_json.get_tag_dicom("(0018,0082)",
                    # dicom_json.filepath)["value"]
                    # flip_angle = io_json.get_tag_dicom("(0018,1314)",
                    # dicom_json.filepath)["value"]
                    # modality_label = tagger(scanning_sequence,
                    # repetition_time, echo_time, inversion_time, flip_angle)
                    ###########################################################

                    iop = io_json.get_tag_dicom("(0020,0037)",
                                                dicom_json.filepath)["value"]
                    # dicom_json.filepath)["value"]

                    print(scan+" <-> "+value + " <-> " + str(file_plane(iop)))

                    if value == "dwi":
                        print("dwi")
                        procedure_class.diffusion_procedure(
                            subject_name, num_session, value, scan,
                            file_plane(iop), mids_data_path, subject_path,
                            dicom_json)
                    elif value == "pwi":
                        print("pwi")
                        procedure_class.perfusion_procedure(
                            subject_name, num_session, value, file_plane(iop),
                            mids_data_path, subject_path, dicom_json)
                    elif value == "unknow":
                        print("unknow")
                        subject_path = (department_path + os.sep
                                        + "derivatives" + os.sep
                                        + subject_name + os.sep)
                        procedure_class.unknow_procedure(
                            subject_name, num_session, scan, file_plane(iop),
                            mids_data_path, subject_path, dicom_json)
                    else:
                        print("anat")
                        procedure_class.anatomic_procedure(
                            subject_name, num_session, value, file_plane(iop),
                            mids_data_path, subject_path, dicom_json)




def create_participants_tsv():
    """
    This function allows the user to create a table in format ".tsv"
    whit a information of subject
    """
    depth_path_ceib = mids_data_path.depth + 1
    depth_path_subject = mids_data_path.depth + 2
    for projects in file_funtions.get_dirs(mids_data_path.filepath):
        if depth_path_ceib == projects.depth:
            # department_path = projects.filename
            csv_file = "participant\tid_pseudoanonymization\thealth_areas\tmodality_dicom\tbody_parts\tage\tgender\n"
            print ((projects.filepath))
            for subjects in file_funtions.get_dirs(projects.filepath + os.sep):
                if "sub-" in subjects.filename: # and depth_path_subject == subject.depth:
                    list_age = list([float("inf")])
                    sex = 'U'
                    id_pseudo=None
                    health_areas=None
                    modality_dicom_list=["MR"]
                    body_parts_list=[["HEAD"]]
                    # accession = ''
                    # print((subjects.filename))
                    for json_files in file_funtions.get_files(
                            subjects.filepath + os.sep):
                        if "json" in json_files.extension:
                            #print(json_files)
                            # accession = (io_json.get_tag_dicom(
                            #     "(0008,0050)", json_files.filepath)["value"])
                            # print("No hay edad: " + json_files.filepath)
                            birtday = (
                                io_json.get_tag_dicom(
                                    "(0010,0030)",
                                    json_files.filepath)["value"]
                                )
                            study_date = (
                                io_json.get_tag_dicom(
                                    "(0008,0020)",
                                    json_files.filepath)["value"])
                            try:
                                birtday_list = [int(birtday[0:4]),
                                                int(birtday[4:6]),
                                                int(birtday[-2:])]
                                study_list = [int(study_date[0:4]),
                                              int(study_date[4:6]),
                                              int(study_date[-2:])]
                                start_date = datetime(birtday_list[0],
                                                      birtday_list[1],
                                                      birtday_list[2],
                                                      12,
                                                      33)
                                end_date = datetime(study_list[0],
                                                    study_list[1],
                                                    study_list[2],
                                                    12,
                                                    33)
                                diffyears = end_date.year - start_date.year
                                diffmonths = end_date.month - start_date.month
                                diffdays = end_date.day - start_date.day
                                if diffdays < 0: diffmonths -= 1
                                if diffmonths < 0: diffyears -= 1
                            except ValueError as e:
                                try:
                                    age_str = (io_json.get_tag_dicom(
                                        "(0010,1010)",
                                        json_files.filepath)["value"]
                                    )
                                    isYorM=age_str[-1]
                                    if "Y" == isYorM: diffyears=int(age_str[:-2])
                                    else: diffyears=int(int(age_str[:-2])/12)
                                except ValueError as e:
                                    diffyears = -1

                            list_age.append(diffyears)
                            if sex == "U":
                                sex = (
                                    io_json.get_tag_dicom(
                                        "(0010,0040)",
                                        json_files.filepath)["value"]
                                    )
                            id_pseudo=(
                                    io_json.get_tag_dicom(
                                        "(0010,0010)",
                                        json_files.filepath)["value"]
                                    )
                            health_areas=(
                                    io_json.get_tag_dicom(
                                        "(0008,1030)",
                                        json_files.filepath)["value"]
                                    )[-4:]
                    print(type(id_pseudo),health_areas,str(modality_dicom_list),str(body_parts_list),str(min(list_age)),sex)
                    if id_pseudo==None: continue
                    csv_file += (subjects.filename
                                 + '\t' + id_pseudo
                                 + '\t' + health_areas
                                 + '\t' + str(modality_dicom_list)
                                 + '\t' + str(body_parts_list)
                                 + '\t' + str(min(list_age))
                                 + '\t' + sex
                                 + '\n')
            with open(projects.filepath + os.sep
                      + "participants.tsv", 'w') as csv_input:
                csv_input.write(csv_file)

def create_sessions_tsv():
    depth_path_subject = xnat_data_path.depth + 2
    header_tsv="session\tmedical_evaluation"
    for subjects in file_funtions.get_dirs(xnat_data_path.filepath):
        if depth_path_subject == subjects.depth and "_S" in subjects.filename:
            print(subjects.filepath)
            department = subjects.filepath.split("/")[6]
            print(subjects.filepath.split("/")[7])
            subject = "sub-" + subjects.filepath.split("/")[7].split("_")[1]
            path_mids = os.path.join(mids_data_path.filepath, department, subject)
            path_mids_deriv = os.path.join(
                mids_data_path.filepath, "derivatives", department, subject
                )
            print(path_mids)
            print(path_mids_deriv)
            corpus=""
            for resource in file_funtions.get_files(subjects.filepath):
                if ".txt" in resource.filepath:
                    session = "ses-" + resource.filepath.split("/")[8].split("_")[1]
                    print(resource.filepath)
                    #/mnt/cabinaData/openmind/xnat_download_10k/all_2/10kdscv15_2016/ceibcs03_S11343/ceibcs03_E11396/resources/sr/files/sr_ea4632391e_for_184830671267436751733081759737723892659.txt

                    encoding = chardet.detect(open(resource.filepath, "rb").read())['encoding']
                    f = open(resource.filepath, "r",encoding=encoding)
                    eval=f.read().replace("\t", "    ")
                    f.close()
                    corpus += "\t".join([session,eval]) + "\n"
            if corpus:
                if os.path.exists(path_mids):
                    f = open(os.path.join(path_mids,subject + "_sessions.tsv"), "w")
                else:
                    os.makedirs(path_mids_deriv, exist_ok=True)
                    f = open(os.path.join(path_mids_deriv,subject + "_sessions.tsv"), "w")
                f.write(header_tsv + "\n" + corpus)
                f.close()


def create_scans_tsv():
    for sessions in file_funtions.get_dirs(mids_data_path.filepath):
        if "ses-" in sessions.filename:
            tags_list = ["(0010,0020)",
                "(0008,0070)", "(0008,103E)", "(0008,1090)",
                "(0010,0040)", "(0010,1010)", "(0010,1030)", "(0018,0020)",
                "(0018,0021)", "(0018,0022)", "(0018,0023)", "(0018,0050)",
                "(0018,0080)", "(0018,0081)", "(0018,0082)", "(0018,0084)",
                "(0018,0087)", "(0008,1090)", "(0018,0088)", "(0018,0091)",
                "(0018,0093)", "(0018,0095)", "(0018,1314)", "(0018,5100)",
                "(0020,0032)", "(0020,0037)", "(0020,1040)", "(0020,1041)",
                "(0028,0010)", "(0028,0011)", "(0028,0030)", "(0028,0100)",
                "(0018,0083)", "(0018,0086)", "(0018,9461)"
                ]
            tsv_cab_list = ["filename", "session_id_pseudo"] + tags_list[1:]
            tsv = ""
            subject = sessions.filepath.split(os.sep)[-2]
            session = sessions.filename
            for dicom in file_funtions.get_files(sessions.filepath):
                if ".json" == dicom.extension:
                    print(dicom.filepath)
                    # accession = (
                    #     io_json.get_tag_dicom("(0008,0050)",
                    #                           dicom.filepath)["value"]
                    #     )
                    # project = (
                    #     io_json.get_tag_dicom("(0008,1030)",
                    #                           dicom.filepath)["value"]
                    #     )
                    # name_scan = (
                    #     io_json.get_tag_dicom("(0008,103E)",
                    #                           dicom.filepath)["value"])
                    tsv_list = [None] * len(tags_list)
                    for tag_iter, tag in enumerate(tags_list):
                        if io_json.get_tag_dicom(
                                tag, dicom.filepath):
                            if (tsv_cab_list[tag_iter + 1]
                                    == tags_list[tag_iter]) and tag_iter !=0:
                                tsv_cab_list[tag_iter + 1] = (
                                    io_json.get_tag_dicom(
                                        tag,
                                        dicom.filepath)["desc"].replace("&rsquo;","'")
                                    + ' ' + tag)
                            tsv_list[tag_iter] = (
                                io_json.get_tag_dicom(tag,
                                                      dicom.filepath)["value"].replace("&rsquo;","'")
                                )
                        else:
                            tsv_list[tag_iter] = None
                    nifti_pattern = (
                        dicom.filename[dicom.filename.find("_run"):]
                        + ".nii.gz"
                        )
                    nifti_list = []
                    print(nifti_pattern)
                    for nifti in file_funtions.get_files(dicom.path):
                        if nifti_pattern in nifti.filename + nifti.extension:
                            print(nifti.filename + nifti.extension)
                            nifti_list.append(
                                "/".join(nifti.filepath.split("/")[-2:])
                                )
                    tsv += (",".join(nifti_list) + '\t'
                            + '\t'.join([(str(x)) for x in tsv_list])+'\n')
            with open(sessions.filepath + os.sep + subject + "_"
                      + session + "_scans.tsv", 'w') as tsv_input:
                tsv_input.write(
                    '\t'.join([str(x) for x in tsv_cab_list]) + '\n'
                    )
                tsv_input.write(tsv)




def main():
    """
    This Fuction is de main programme
    """

    ## global variables declaration
    global project_id_list, xnat_data_path, mids_data_path
    global user, path_programme, scans_dict

    # Contropl of arguments of programme
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description="""
This sorfware allow the user to Download one project into XNAT platform
of BIMCV and convert the XNAT directory images in a MIDS directory.

The aplication execution need Python --version >= 3.5.

there are 2 funtions in this code:

  Download one project from xnat aplicatión:

     arguments:
      + Prefix    -w --web PAGE_WEB         1) The ULR page where XNAT is.

      + Prefix    -u --user [USER]          2) The username to loggin in XNAT
                                            If not write a username, It loggin
                                            as guest.

      + Prefix    -p --project [PROJECT]    3) The project name to download,
                                            if the project is omitted, the
                                            aplication show all projects in
                                            xnat to choice.

      + Prefix    -i --input INPUT          4) the directory where the
                                            files will be downloaded.

  Convert the xnat directories of the project in MIDS format:

    arguments:

      + Prefix    -i --input INPUT          1) the directory where the files
                                            will be downloaded.

      + Prefix    -o --output OUTPUT        2) Directory where the MIDS model
                                            is applied.
    """
    )
    parser.add_argument('-w', '--web', type=str, default="",
                        help='The ULR page where XNAT is.')
    parser.add_argument('-u', '--user', type=str, default="",
                        help="""The username to loggin in XNAT
                                If not write a username, It loggin
                                as guest.""")
    parser.add_argument('-i ', '--input', type=str,
                        help="""the directory where the files will
                        be downloaded.""")
    parser.add_argument('-o ', '--output', type=str,
                        help='Directory where the MIDS model is applied.')
    parser.add_argument('-p ', '--project', nargs='*', default="", type=str,
                        help="""The project name to download, if the project is
                        omitted,the aplication show all projects in xnat
                        to choice.""")
    want_dicom = False
    want_nifti = True
    want_bids = False
    args = parser.parse_args()
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    # Depends of the option, funtions are activated
    if not args.project == "" and args.input and args.web:
        page = args.web
        user = args.user
        # if user != "":
        #     password = getpass.getpass("Password of XNAT: ")
        xnat_data_path = args.input
        try:
            os.mkdir(xnat_data_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        if args.project:
            project_id_list += args.project.split(' ')
        else:
            project_id_list = dfx.show_projects(page, user)
            dfx.download_projects(page, user, project_id_list, xnat_data_path,
                                  want_dicom, want_nifti, want_bids)
    if args.input and args.output:
        xnat_data_path = file_funtions.FileInfo(args.input)
        if not os.path.isdir(args.output):
            os.mkdir(args.output)
        mids_data_path = file_funtions.FileInfo(args.output)
        print("MIDS are generating...")
        time.sleep(2)
        scans_dict = load_dictionary()
        # for i in scans_dict.items():
        #     print(i)
        # #print(len(dictionary_scans.items()))
        # #for i in dictionary_scans.items():
        # #    print(i)
        #create_directorio_MIDS()
        print("participats tsv are generating...")
        #create_participants_tsv()
        print("scan tsv are generating...")
        #create_scans_tsv()
        print("session tsv are generating...")
        create_sessions_tsv()




    exit(0)



###############################################################################
# Main corpus
###############################################################################

if __name__ == '__main__':
    main()
