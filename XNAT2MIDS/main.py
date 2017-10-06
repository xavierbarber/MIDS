#/usr/bin/env  python   #iniciaize enviroment
# -*- coding: utf-8 -*-.

"""
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

    there are 3 funtions in this code:
        download one project from xnat aplicatión:
        arguments:
            Prefix	-p --project	1) The project name to download
            Prefix	-i --input	2) the directfory where the files will
            be downloaded
        Convert the xnat directories of the project in MIDS format:
        arguments:
            Prefix	-i --input	2) the directfory where the files will
            be downloaded
            Prefix	-o --output	3) Directory where the MIDS model
            is applied
        Update the scans dictionary
            Prefix	-c --csv
"""


###############################################################################
# Imports
###############################################################################

import os
import time
import sys
import getpass
import argparse
import time
from datetime import datetime
from calendar import isleap
import Bash_functions.bash_exe as bash
import IO_Functions.file_class as file_funtions
import IO_Functions.io_json as io_json
import IO_Functions.io_objects as io_objects
import download_from_xnat as dfx
###############################################################################
# Global Variables
###############################################################################

# GLOBAL statement of the path where the main program is executed
path_programme = file_funtions.FileInfo(os.path.realpath(__file__))

# GLOBAL statement of the path where the objects and dictionaries
# python is stored
dictionary_path = path_programme.path + ".python_objects" + os.sep
log_path = path_programme.path + ".log/"
# GLOBAL statement of the project which is download
project_id_list = []

# Path where xnat files are stored
xnat_data_path = ""

# Path where the BIDS model is applied with xnat cases
mids_data_path = ""

# GLOBAL statement of dictionaries used for management
dictionary_sessions = dict()
dictionary_scans = dict()

# GLOBAL statement that store user and password of xnat session
user = ""
password = ""

###############################################################################
# Functions
###############################################################################


def load_dictionary():
    """
    This function allows the user to load dictionaries
    """

    # this dictinary contains information that is not included
    # in the dicom header
    global dictionary_sessions, dictionary_scans
    if not os.path.exists(dictionary_path + "dictionary_session.dic"):
        print(('no existe diccionario'))
        exit(0)
    else:
        dictionary_sessions = dict(
            io_objects.load_pickle(dictionary_path + "dictionary_session.dic"))
    # this dictionary contains all word of scans for classifying all
    # images in MIDS
    if not os.path.exists(dictionary_path + "dictionary_scan.dic"):
        print(('no existe diccionario'))
        exit(0)
    else:
        dictionary_scans = dict(
            io_objects.load_pickle(dictionary_path + "dictionary_scan.dic"))


def create_directorio_MIDS():
    """
    This function allows the user to convert the xnat directory to
    mids directory
    """
    error=0
    global dictionary_sessions, dictionary_scans
    depth_path_xnat = xnat_data_path.depth + 3
    for sessions_xnat in file_funtions.get_dirs(xnat_data_path.filepath):
        if depth_path_xnat == sessions_xnat.depth:
            T1w_index = 1
            T2w_index = 1
            T1rho_index = 1
            T1map_index = 1
            T2map_index = 1
            T2star_index = 1
            FLAIR_index = 1
            FLASH_index = 1
            PD_index = 1
            PDT2_index = 1
            inplaneT1_index = 1
            inplaneT2_index = 1
            angio_index = 1
            defacemask_index = 1
            SWImagandphase_index = 1
            task_index = 1
            rest_index = 1
            dwi_index = 1
            fmri_index = 1
            perfusion_index=1
            others_index=1
            unassigned_index = 1
            for dicom_json in file_funtions.get_files(sessions_xnat.filepath):
                if dicom_json.match("*.json") and dicom_json.is_file:
                    linea = dicom_json.filepath.replace(xnat_data_path.filepath, '')
                    nii_gz_list_path = linea.split('/')
                    department_path = nii_gz_list_path[0]
                    #subject = nii_gz_list_path[1]
                    session = nii_gz_list_path[2]
                    scan =nii_gz_list_path[4].split('-')[1:]
                    scan = str.join('-',scan)
                    #print((scan))
                    accession = (
                        io_json.get_tag_dicom("(0008,0050)",dicom_json.filepath)
                        )["value"]
                    #print(accession)
                    if accession == None:
                        print("error: no hay un accesion number en el dicom")
                        continue

                    #import pdb; pdb.set_trace().
                    try:
                        group = dictionary_sessions[department_path + '-' + accession][0].split('_')
                    except KeyError:
                        error+=1
                        print(error)
                        continue
						
                    #control_path = group[0] + '_' + group[1]
                    subject_name = 'sub-' + group[2]
                    session_number = session.split('-')
                    if len(session_number) == 1:
                        num_session = "ses-1"
                    else:
                        num_session = "ses-" + session_number[1]

                    modality_label = dictionary_scans[scan.lower()]["Modality_label"]
                    data_type = dictionary_scans[scan.lower()]["data_type"]
                    subject_path = (department_path + os.sep + subject_name + os.sep)
                    print(modality_label)
                    if "T1w" == modality_label:
                        print(("t1w"))
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(T1w_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)


                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.split('\n')

                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(T1w_index)  + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)

                            acq_index += 1
                        T1w_index += 1

                    elif "T1rho" == modality_label:
                        print(("t1rho"))
                    elif "T1map" == modality_label:
                        print(("t1map"))
                    elif "T2w" == modality_label:#############
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(T2w_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)
                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(T2w_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)
                            acq_index += 1
                        T2w_index += 1
                        print(("t2w"))
                    elif "T2star" == modality_label:
                        print(("t2star"))
                    elif "FLAIR" == modality_label:#############
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(FLAIR_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)


                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(FLAIR_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)
                            acq_index += 1
                        FLAIR_index += 1
                        print(("FLAIR"))
                    elif "FLASH" == modality_label:
                        print(("FLASH"))
                    elif "PD" == modality_label:
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(PD_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)


                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(PD_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)

                            acq_index += 1
                        PD_index += 1
                        print(("PD"))
                    elif "PDmap" == modality_label:
                        print(("PDmap"))
                    elif "PDt2" == modality_label:
                        print(("Combined DP/T2"))
                    elif "inplaneT1" == modality_label:
                        print(("inplaneT1"))
                    elif "inplaneT2" == modality_label:
                        print(("inplaneT2"))
                    elif "angio" == modality_label:#############
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(angio_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)


                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(angio_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)

                            acq_index += 1
                        FLAIR_index += 1
                        print(("angio"))
                    elif "defacemask" == modality_label:
                        print(("Defacing mask"))
                    elif "SWImagandphase" == modality_label:#############
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(SWImagandphase_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)


                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(SWImagandphase_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)

                            acq_index += 1
                        SWImagandphase_index += 1
                        print(("SWImagandphase"))
                    elif "dwi" == modality_label:
                        print(("dwi"))
                        out, err = bash.bash_command("ls " + dicom_json.path + "*.bval")
                        bval_file = out.replace('\n', '')
                        if not os.path.exists(bval_file):
                            continue
                        else:
                            with open (bval_file,"+r") as handle:
                                value=handle.readline().replace('\n','')
                                while ' ' in value: value = value.replace(' ','')
                                print((value))
                                if value == '0': continue
                        out, err = bash.bash_command("ls " + dicom_json.path + "*.bvec")
                        bvec_file = out.replace('\n', '')
                        if not os.path.exists(bvec_file):
                            continue
                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.split('\n')
                        nifti_file=bvec_file[:-4] + "nii.gz"
                        new_path_mids= mids_data_path.filepath+os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        dicom_name = subject_name + "_" + num_session + "_run-" + str(dwi_index) + "_dwi.json"
                        bval_name = subject_name + "_" + num_session + "_run-" + str(dwi_index) + "_dwi.bval"
                        bvec_name = subject_name + "_" + num_session + "_run-" + str(dwi_index) + "_dwi.bvec"
                        nii_name = subject_name + "_" + num_session + "_run-" + str(dwi_index) + "_dwi.nii.gz"
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + bval_file + " " +new_path_mids + bval_name)
                        bash.bash_command("cp " + bvec_file + " " +new_path_mids + bvec_name)
                        bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)

                        dwi_index = 1
                    elif "bold" == modality_label:
                        print(("bold"))
                    elif "perfusion" in modality_label:
                        print((modality_label))
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(perfusion_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)
                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session + "_acq-" + str(acq_index) + "_run-" + str(perfusion_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)

                            acq_index += 1
                        perfusion_index += 1
                    elif modality_label:
                        print((modality_label))
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-" + str(acq_index) + "_run-" + str(others_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)
                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session + "_acq-" + str(acq_index) + "_run-" + str(others_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)

                            acq_index += 1
                        others_index += 1
                    else:
                        print(("no found"))#############stir
                        unassigned_index += 1
    print(error)





def create_participants_tsv():
    """
    This function allows the user to create a table in format ".tsv"
    whit a information of subject
    """

    global dictionary_sessions, dictionary_scans
    depth_path_ceib = mids_data_path.depth + 1
    for projects in file_funtions.get_dirs(mids_data_path.filepath):
        if depth_path_ceib == projects.depth:
            department_path = projects.filename
            csv_file="participant_id\tage\tgender\tcontrol\n"
            print ((projects.filepath))

            for subjects in file_funtions.get_dirs(projects.filepath + os.sep):
                if "sub-" in subjects.filename:
                    list_age=list([float("inf")])
                    sex='U'
                    accession=''
                    control_group=0
                    #print((subjects.filename))
                    for json_files in file_funtions.get_files(subjects.filepath + os.sep):
                        if ".json" in json_files.filename + json_files.extension:
                            accession = (io_json.get_tag_dicom("(0008,0050)",json_files.filepath)["value"])
                            control_group=int(dictionary_sessions[department_path + '-' + accession][0].split('_')[0])
                            #print((json_files.filepath+"-----------------------------------------------------------------------"))
                            try:
                                list_age.append(int(io_json.get_tag_dicom("(0010,1010)",json_files.filepath)["value"][:-1]))
                            except TypeError:
                                print("No hay edad: " + json_files.filepath)
                                birtday = (io_json.get_tag_dicom("(0010,0030)",json_files.filepath)["value"])
                                study_date = (io_json.get_tag_dicom("(0008,0020)",json_files.filepath)["value"])
                                birtday_list=[int(birtday[0:4]),int(birtday[4:6]),int(birtday[-2:])]
                                study_list=[int(study_date[0:4]),int(study_date[4:6]),int(study_date[-2:])]
                                start_date = datetime(birtday_list[0],birtday_list[1],birtday_list[2],12,33)
                                end_date = datetime(study_list[0],study_list[1],study_list[2],12,33)
                                diffyears = end_date.year - start_date.year
                                difference  = end_date - start_date.replace(end_date.year)
                                days_in_year = isleap(end_date.year) and 366 or 365
                                difference_in_years = diffyears + (difference.days + difference.seconds/86400.0)/days_in_year
                                list_age.append(int(difference_in_years))
                            if sex == "U":
                                sex = (io_json.get_tag_dicom("(0010,0040)",json_files.filepath)["value"])
                    csv_file += subjects.filename+'\t'+str(min(list_age))+'\t'+sex+'\t'+str(control_group)+'\n'
            with open (projects.filepath+os.sep+"participants.tsv",'+w') as csv_input:
                csv_input.write(csv_file)


def create_scans_tsv():
    global dictionary_sessions
    for sessions in file_funtions.get_dirs(mids_data_path.filepath):
        if "ses-" in sessions.filename:
            tags_list = [
                "(0008,0070)", "(0008,103E)", "(0008,1090)", "(0010,0020)",
                "(0010,0040)", "(0010,1010)", "(0010,1030)", "(0018,0020)",
                "(0018,0021)", "(0018,0022)", "(0018,0023)", "(0018,0050)",
                "(0018,0080)", "(0018,0081)", "(0018,0082)", "(0018,0084)",
                "(0018,0087)", "(0008,1090)", "(0018,0088)", "(0018,0091)",
                "(0018,0093)", "(0018,0095)", "(0018,1314)", "(0018,5100)",
                "(0020,0032)", "(0020,0037)", "(0020,1040)", "(0020,1041)",
                "(0028,0010)", "(0028,0011)", "(0028,0030)", "(0028,0100)",
                "(0018,0083)", "(0018,0086)", "(0018,9461)"
                 ]
            tsv_cab_list = ["filename","slides","plane"] + tags_list
            tsv = ""
            subject = sessions.filepath.split(os.sep)[-2]
            session = sessions.filename
            for dicom in file_funtions.get_files(sessions.filepath):
                if ".json" in dicom.filename + dicom.extension:
                    print(dicom.filepath)
                    accession = (io_json.get_tag_dicom("(0008,0050)",dicom.filepath)["value"])
                    project = (io_json.get_tag_dicom("(0008,1030)",dicom.filepath)["value"])
                    name_scan = (io_json.get_tag_dicom("(0008,103E)",dicom.filepath)["value"])
                    slides, plane = None,None
                    try:
                        slides = dictionary_sessions[project + '-' + accession][1][name_scan][0]
                    except KeyError:
                        pass
                    try:
                        plane = dictionary_sessions[project + '-' + accession][1][name_scan][1]
                    except KeyError:
                        pass
                    tsv_list = [None] * len(tags_list)
                    for tag_iter in range(len(tags_list)):
                        if io_json.get_tag_dicom(tags_list[tag_iter],dicom.filepath):
                            if tsv_cab_list[tag_iter + 3]==tags_list[tag_iter]:
                                tsv_cab_list[tag_iter + 3] = (io_json.get_tag_dicom(tags_list[tag_iter],dicom.filepath)["desc"]
                                + ' ' + tags_list[tag_iter])
                            tsv_list[tag_iter]=(io_json.get_tag_dicom(tags_list[tag_iter],dicom.filepath)["value"])
                        else:
                            tsv_list[tag_iter]=None
                    nifti_pattern=dicom.filename[dicom.filename.find("_run"):]+ ".nii.gz"
                    nifti_list=[]
                    print((nifti_pattern))
                    for nifti in file_funtions.get_files(dicom.path):
                        if nifti_pattern in nifti.filename + nifti.extension:
                            print(nifti.filename + nifti.extension)
                            nifti_list.append("/".join(nifti.filepath.split("/")[-2:]))
                    tsv+=( ",".join(nifti_list) + '\t' + str(slides) + '\t'
                    + str(plane) + '\t' + '\t'.join([(str(x)) for x in tsv_list])+'\n')
            with open (sessions.filepath+ os.sep + subject + "_" + session + "_scans.tsv",'+w') as tsv_input:
                tsv_input.write('\t'.join([str(x) for x in tsv_cab_list]) + '\n')
                tsv_input.write(tsv)




def main():
    """
    This Fuction is de main programme
    """

    ## global variables declaration
    global project_id_list, path_csv, xnat_data_path, mids_data_path
    global user, password, path_programme, dictionary_sessions
    global dictionary_scans

    # Contropl of arguments of programme
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description="""
This sorfware allow the user to Download one project into XNAT platform
of BIMCV and convert the XNAT directory images in a MIDS directory.

The aplication execution need Python --version >= 3.5.

there are 3 funtions in this code:

  Download one project from xnat aplicatión:

     arguments:

      + Prefix    -p --project [PROJECT]    1) The project name to download,
                                            if the project is omitted, the
                                            aplication show all projects in
                                            xnat to choice

      + Prefix    -i --input INPUT          2) the directory where the
                                            files will be downloaded

  Update the dictionary of scans, it is use to clasificate any medical
  image in MIDS structure:

      + Prefix    -c --csv                  Scans dictionary is uploaded when
                                            this flag is appeared

  Convert the xnat directories of the project in MIDS format:

    arguments:

      + Prefix    -i --input INPUT          1) the directory where the files
                                            will be downloaded

      + Prefix    -o --output OUTPUT        2) Directory where the MIDS model
                                            is applied
    """
    )
    parser.add_argument('-c','--csv', action="store_true", default=False,
    help='Scans dictionary is uploaded when this flag is appeared')
    parser.add_argument('-i ', '--input',type=str,
    help='the directory where the files will be downloaded')
    parser.add_argument('-o ', '--output', type=str,
    help='Directory where the MIDS model is applied')
    parser.add_argument('-p ', '--project', nargs='*', default ="", type=str,
    help="""The project name to download, if the project is omitted,
    the aplication show all projects in xnat to choice""")
    args = parser.parse_args()
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    ##Depends of the option, any funtions are activated
    if not args.project is "" and args.input:
        user = input('User of XNAT: ')
        password = getpass.getpass("Password of XNAT: ")
        xnat_data_path=args.input
        if args.project:
			
            project_id_list+=args.project.split(' ')
        else:
            project_id_list = dfx.catalog_projects(user, password)
        for project_id in project_id_list:
            with open(log_path+project_id+".log","+w") as project_log:
                project_log.write("Current date & time " + time.strftime("%c"))
            print(project_id)
            dfx.download_from_xnat(
            project_id, xnat_data_path, user, password, log_path + project_id+".log"
            )
    if args.csv:
        io_objects.csv_2_dict(dictionary_path + "dictionary_scan.csv")
    if args.input and args.output:
        xnat_data_path = file_funtions.FileInfo(args.input)
       	if not os.path.isdir(args.output):
            os.mkdir(args.output)
        mids_data_path = file_funtions.FileInfo(args.output)
        print(("MIDS are generating..."))
        time.sleep(2)
        load_dictionary()
        #print(len(dictionary_scans.items()))
        #for i in dictionary_scans.items():
        #    print(i)
        create_directorio_MIDS()
        create_participants_tsv()
        create_scans_tsv()



    exit(0)


###############################################################################
# Main corpus
###############################################################################

if __name__ == '__main__':
    main()
