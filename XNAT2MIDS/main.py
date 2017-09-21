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
            io_objects.load_pickle(dictionary_path + "dictionary_session.dic"))
    # this dictionary contains all word of scans for classifying all
    # images in MIDS
    if not os.path.exists(dictionary_path + "dictionary_scans.dic"):
        print(('no existe diccionario'))
        exit(0)
    else:
        dictionary_scans = dict(
            io_objects.load_pickle(dictionary_path + "dictionary_scans.dic"))


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
            perfusion_index=1
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

                    #import pdb; pdb.set_trace().
                    group = dictionary_sessions[department_path + '-' + accession][0].split('_')

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
                    else:
                        print(("no found"))#############stir
                        unassigned_index += 1



"""
This function allows the user to create a table in format ".tsv"
whit a information of subject
"""


def crear_participants_tsv():
    global dictionary_sessions, dictionary_scans
    depth_path_ceib = mids_data_path.depth + 1
    for projects in file_funtions.get_dirs(mids_data_path.filepath):
        if depth_path_ceib == projects.depth:
            department_path = projects.filename
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
                            control_group=int(dictionary_sessions[department_path + '-' + accession][0].split('_')[0])
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
                "(0018,0083)", "(0018,0086)"
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

"""
This Fuction is de main programme
"""


def main():

    ## global variables declaration
    global project_id, path_csv, xnat_data_path, mids_data_path
    global user, password, path_programme, dictionary_sessions
    global dictionary_scans

    opt_w = False
    opt_i = False
    opt_o = False
    opt_l = False

    # Contropl of arguments of programme
    if len(sys.argv) < 2:

        exit(0)

    # the arguments are obtained
    arg = sys.argv[1:len(sys.argv)]
    for i in range(0, len(arg), 2):
        if '-' not in arg[i]:
            print (("Error of number of parametres"))
            exit(0)
        if arg[i].lower() == "-p" or arg[i].lower() == "--project":
            opt_w = True
            project_id = str(arg[i + 1])
        elif arg[i].lower() == "-i" or arg[i].lower() == "--input":
            opt_i = True
            if not(os.path.isdir(str(arg[i + 1]))):
                bash.bash_command("mkdir -p " + str(arg[i + 1]))
            xnat_data_path = file_funtions.FileInfo(str(arg[i + 1]))
        elif arg[i].lower() == "-o" or arg[i].lower() == "--output":
            opt_o = True
            if not(os.path.isdir(str(arg[i + 1]))):
                bash.bash_command("mkdir -p " + str(arg[i + 1]))
            mids_data_path = file_funtions.FileInfo(str(arg[i + 1]))
        elif arg[i].lower() == "-l" or arg[i].lower() == "--list":
            opt_l=True
        elif arg[i].lower() == "-c" or arg[i].lower() == "--csv":
            io_objects.save_pickle(
                io_objects.csv_2_dict(
                    dictionary_path + "dictionary_scan.csv"
                ), dictionary_path + "dictionary_scans.dic"
            )
        else:
            print(("invalid option"))

            print (("this programme needs at least a group of parametres\n"
                + " to execute:"))

            print (("""    dowload  images of a one project
                --> -p \"project_id\" -i \"dir_xnat\""""))

            print (("""    create directory MIDS
                --> -p \"project_id\" -i \"dir_xnat\" -o \"dir_CEIB\""""))

            print((path_programme.path))
            exit(0)

    #Depends of the option, any funtions are activated
    if (opt_w or opt_l) and opt_i:
        print(("Download dataset: " + project_id))
        time.sleep(2)
        #the user and password is asked
        user = input('User of XNAT: ')
        password = getpass.getpass("Password of XNAT: ")
        if opt_l:
            project_id = dfx.catalog_projects(user, password)
        dfx.download_from_xnat(
            project_id, xnat_data_path.filepath, user, password
            )

    if opt_i and opt_o:
        print(("MIDS are generating..."))
        time.sleep(2)
        load_dictionary()
        #crear_directorio_MIDS()
        #crear_participants_tsv()
        create_scans_tsv()

    exit(0)


###############################################################################
# Main corpus
###############################################################################

if __name__ == '__main__':
    main()
