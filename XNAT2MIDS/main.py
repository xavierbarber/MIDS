#/usr/bin/env  python   #iniciaize enviroment
# -*- coding: utf-8 -*-.

"""
Subdirección General de Sistemas de Información para la Salud

Centro de Excelencia e Innovación Tecnológica de Bioimagen de la Conselleria de Sanitat

http://ceib.san.gva.es/

María de la Iglesia Vayá -> delaiglesia_mar@gva.es or miiglesia@cipf.es

Jhon Jairo Saenz Gamboa ->jjsaenz@cipf

Jose Manuel Saborit Torres -> jmsaborit@cipf.es

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

Python --version >= 3.4

Description:
    This aplication allow the user to download one project on XNAT and
    transform these project in MIDS format

    there are 2 funtions in this code:
        download one project from xnat aplicatión:
        arguments:
        Prefix	-p	1) The project name to download
        Prefix	-i	2) the directfory where the files will be downloaded
    Convert the xnat directories of the project in MIDS format:
        arguments:
        Prefix	-p	1)The project name to download
        Prefix	-i	2) the directfory where the files will be downloaded
        Prefix	-o	3) Directory where the BIDS model is applied
"""


###############################################################################
# Imports
###############################################################################

import os
import time
import sys
import getpass

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

# GLOBAL statement of the project which is download
project_id = ""

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


"""
This function allows the user to load dictionaries
"""


def load_dictionary():
    # this dictinary contains information that is not included
    # in the dicom header
    global dictionary_sessions, dictionary_scans
    if not os.path.exists(dictionary_path + "dictionary_session.dic"):
        print(('no existe diccionario'))
        exit(0)
    else:
        dictionary_sessions = dict(
            io_objects.load_pickle(dictionary_path + "diccionary_session.dic"))
    # this dictionary contains all word of scans for classifying all
    # images in MIDS
    if not os.path.exists(dictionary_path + "dictionary_scans.dic"):
        print(('no existe diccionario'))
        exit(0)
    else:
        dictionary_scans = dict(
            io_objects.load_pickle(dictionary_path + "diccionary_scans.dic"))


"""
This function allows the user to convert the xnat directory to
mids directory
"""


def crear_directorio_MIDS():
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
            unassigned_index = 1
            for dicom_json in file_funtions.get_files(sessions_xnat.filepath):
                if dicom_json.match("*.json") and dicom_json.is_file:
                    linea = dicom_json.filepath.replace(xnat_data_path.filepath, '')
                    nii_gz_list_path = linea.split('/')
                    department_path = nii_gz_list_path[1]
                    #subject = nii_gz_list_path[2]
                    session = nii_gz_list_path[3]
                    scan =nii_gz_list_path[5].split('-')[1:]
                    scan = str.join('-',scan)
                    #print((scan))
                    accession = (
                        io_json.get_tag_dicom("(0008,0050)",dicom_json.filepath)
                        )["value"]
                    if accession == None:
                        print("error: no hay un accesion number en el dicom")
                        continue

                    group = dictionary_sessions[project_id + '-' + accession][0].split('_')

                    #control_path = group[0] + '_' + group[1]
                    subject_name = 'sub-' + group[2]
                    session_number = session.split('-')
                    if len(session_number) == 1:
                        num_session = "ses-1"
                    else:
                        num_session = "ses-" + session_number[1]

                    modality_label = dictionary_scans[scan]["Modality_label"]
                    data_type = dictionary_scans[scan]["data_type"]
                    subject_path = (department_path + os.sep + subject_name + os.sep)

                    if "T1w" == modality_label:
                        print(("t1w"))
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) +"_run-" + str(T1w_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)


                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.decode("utf-8").split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) + "_run-" + str(T1w_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)

                            acq_index += 1
                        T1w_index += 1

                    elif "T1rho" == modality_label:
                        print(("t1rho"))
                    elif "T1map" == modality_label:
                        print(("t1map"))
                    elif "T2w" == modality_label:#############
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) +"_run-" + str(T2w_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)
                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.decode("utf-8").split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) + "_run-" + str(T2w_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)
                            acq_index += 1
                        T2w_index += 1
                        print(("t2w"))
                    elif "T2star" == modality_label:
                        print(("t2star"))
                    elif "FLAIR" == modality_label:#############
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) +"_run-" + str(FLAIR_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)


                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.decode("utf-8").split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) + "_run-" + str(FLAIR_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)
                            acq_index += 1
                        FLAIR_index += 1
                        print(("FLAIR"))
                    elif "FLASH" == modality_label:
                        print(("FLASH"))
                    elif "PD" == modality_label:
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) +"_run-" + str(PD_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)


                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.decode("utf-8").split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) + "_run-" + str(PD_index) + "_"+modality_label+".nii.gz"
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
                        dicom_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) +"_run-" + str(angio_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)


                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.decode("utf-8").split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) + "_run-" + str(angio_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)

                            acq_index += 1
                        FLAIR_index += 1
                        print(("angio"))
                    elif "defacemask" == modality_label:
                        print(("Defacing mask"))
                    elif "SWImagandphase" == modality_label:#############
                        acq_index=1
                        dicom_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) +"_run-" + str(SWImagandphase_index) + "_"+modality_label+".json"
                        new_path_mids = mids_data_path.filepath + os.sep + subject_path + num_session + os.sep+ data_type + os.sep
                        if not os.path.exists(new_path_mids):
                            bash.bash_command("mkdir -p " + new_path_mids)
                        bash.bash_command("cp " + dicom_json.filepath + " " +new_path_mids + dicom_name)


                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.decode("utf-8").split('\n')
                        for nifti_file in nifti_files[:-1]:
                            nii_name = subject_name + "_" + num_session +"_acq-"+ str(acq_index) + "_run-" + str(SWImagandphase_index) + "_"+modality_label+".nii.gz"
                            bash.bash_command("cp " + nifti_file + " " +new_path_mids + nii_name)

                            acq_index += 1
                        SWImagandphase_index += 1
                        print(("SWImagandphase"))
                    elif "dwi" == modality_label:
                        print(("dwi"))
                        out, err = bash.bash_command("ls " + dicom_json.path + "*.bval")
                        bval_file = out.decode("utf-8").replace('\n', '')
                        if not os.path.exists(bval_file):
                            continue
                        out, err = bash.bash_command("ls " + dicom_json.path + "*.bvec")
                        bvec_file = out.decode("utf-8").replace('\n', '')
                        if not os.path.exists(bvec_file):
                            continue
                        out, err = bash.bash_command("ls " + dicom_json.path + "*nii.gz")
                        nifti_files = out.decode("utf-8").split('\n')
                        nifti_file=bvec_file[:-3] + "nii.gz"
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
                    else:
                        print(("no found"))#############stir,perfusion
                        unassigned_index += 1



"""
This function allows the user to create a table in format ".tsv" whit a information of subject
"""


def crear_participants_tsv():
    global dictionary_sessions, dictionary_scans
    depth_path_ceib = mids_data_path.depth + 1
    for projects in file_funtions.get_dirs(mids_data_path.filepath):
        if depth_path_ceib == projects.depth:
            csv_file="participant_id\tage\tgender\tcontrol\n"
            print ((projects.filepath))
            list_age=list([float("inf")])
            sex='U'
            accession=''
            control_group=0
            for subjects in file_funtions.get_dirs(projects.filepath + os.sep):
                if "sub-" in subjects.filename:
                    #print((subjects.filename))
                    for json_files in file_funtions.get_files(subjects.filepath + os.sep):
                        if ".json" in json_files.filename + json_files.extension:
                            accession = (io_json.get_tag_dicom("(0008,0050)",json_files.filepath)["value"])
                            control_group=int(dictionary_sessions[project_id + '-' + accession][0].split('_')[0])
                            #print((json_files.filepath+"-----------------------------------------------------------------------"))
                            try:
                                list_age.append(int(io_json.get_tag_dicom("(0010,1010)",json_files.filepath)["value"][:-1]))
                            except TypeError:
                                #print("No hay edad: " + json_files.filepath)
                                pass
                            if sex == "U":
                                sex = (io_json.get_tag_dicom("(0010,0040)",json_files.filepath)["value"])
                    csv_file += subjects.filename+'\t'+str(min(list_age))+'\t'+sex+'\t'+str(control_group)+'\n'
            with open (projects.filepath+os.sep+"participants.tsv",'+w') as csv_input:
                csv_input.write(csv_file)

"""
This Fuction is de main programme
"""


def main():

    ## global variables declaration
    global project_id, path_csv, xnat_data_path, mids_data_path
    global user,password,path_programme

    opt_w = False
    opt_i = False
    opt_o = False

    # Contropl of arguments of programme
    if len(sys.argv) < 2:
        print (("this programme needs at least a group of parametres\n"
                +" to execute:"))
        print (("""    dowload  images of a one project
            --> -p \"project_id\" -i \"dir_xnat\""""))

        print (("""    create directory MIDS
            --> -p \"project_id\" -i \"dir_xnat\" -o \"dir_CEIB\""""))
        print((path_programme.path))
        exit(0)

    elif len(sys.argv) % 2 == 0:
        print (("Error of number of parametres"))
        exit(0)

    # the arguments are obtained
    arg = sys.argv[1:len(sys.argv)]
    for i in range(0, len(arg), 2):
        if '-' not in arg[i]:
            print (("Error of number of parametres"))
            exit(0)
        if arg[i].lower() == "-p":
            opt_w = True
            project_id = str(arg[i + 1])
        elif arg[i].lower() == "-i":
            opt_i = True
            xnat_data_path = file_funtions.FileInfo(str(arg[i + 1]))
        elif arg[i].lower() == "-o":
            opt_o = True
            mids_data_path = file_funtions.FileInfo(str(arg[i + 1]))
        else:
            print(("invalid option"))
            exit(0)

    #the user and password is asked
    user=input('User of XNAT: ')
    password = getpass.getpass("Password of XNAT: ")

    #Depends of the option, any funtions are activated
    if opt_w and opt_i and not opt_o:
        print(("Download dataset: " + project_id))
        time.sleep(2)
        #dfx.catalog_projects()
        dfx.download_from_xnat(project_id, xnat_data_path.filepath,user,password)

    if opt_w and opt_i and opt_o:
        print(("MIDS are generating..."))
        time.sleep(2)
        load_dictionary()
        crear_directorio_MIDS()
        crear_participants_tsv()

    exit(0)


###############################################################################
# Main corpus
###############################################################################

if __name__ == '__main__':
    main()
