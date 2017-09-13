
# -*- coding: utf-8 -*-

###############################################################################
# Imports
###############################################################################
import os

import Bash_functions.bash_exe as bash
import IO_Functions.file_class as file_funtions
import IO_Functions.io_json as io_json
import IO_Functions.io_objects as io_objects
import IO_Functions.file_class as file_funtions


###############################################################################
# Global Variables
###############################################################################
url = "https://ceib.cipf.es/xnat"
path_programme = file_funtions.FileInfo(os.path.realpath(__file__))
download_path = path_programme.path + ".download/"
dictionary_path=path_programme.path + ".python_objects/"


###############################################################################
# Functions
###############################################################################

"""
This functions allows the user to visualize al projects in xnat aplication
NOT IN USE, NEXT UPLOAD
"""

def catalog_projects():
    project_url = url + "/data/projects?format=csv"
    out, err = bash.bash_command(
        "curl --insecure --user " + user +":" + password + " " + project_url
        )
    csv_list = out.split('\n')
    list_project=[]
    for i in range(1,len(csv_list)-1):
        print((csv_list[i].split(',')[0]))
        list_project.append(csv_list[i].split(',')[0])
    list_project.sort()
    print((str(list_project)))

"""
This function allows the user to download all images from one project
"""


def download_from_xnat(project_id, input_xnat, user, password):
    subject_url = url + "/data/projects/" + project_id + "/subjects?format=csv"
    session_dictionary={}
    if os.path.isfile(dictionary_path + "diccionary_session.dic"):
        session_dictionary = io_objects.load_pickle(dictionary_path + "diccionary_session.dic")
    if not os.path.isdir(download_path):
        os.mkdir(download_path)
    if not os.path.isdir(dictionary_path):
        os.mkdir(dictionary_path)
    out, err = bash.bash_command(
        "curl --insecure --user " + user +":" + password + " "
        + "-o " + download_path + "xnat_subjects_temp.csv " + subject_url
        )
    print(("curl --insecure --user " + user +":" + password + " "
        + "-o " + download_path + "xnat_subjects_temp.csv " + subject_url))
    #print(("out: " + str(out)))
    #print(("err: " + str(err)))
    with open(download_path + "xnat_subjects_temp.csv", "+r") as subject_csv:
        list_line = subject_csv.readline().replace('\n', '').split(",")
        subject_id_pos = list_line.index("label")
        uri_id_pos = list_line.index("URI")
        for line in subject_csv:
            list_line = line.replace('\n', '').split(",")
            print((list_line))
            subject_id = list_line[subject_id_pos]
            uri_id = list_line[uri_id_pos]
            sessions_url = url + uri_id + "?format=json"
            #print((sessions_url))
            out, err = bash.bash_command(
                "curl --insecure --user " + user +":" + password + " "
                + "-o " + download_path + "xnat_sessions_temp.json " + sessions_url
                )
            session_json = io_json.load_json(download_path + "xnat_sessions_temp.json")
            group_id = session_json["items"][0]["data_fields"]["group"]
            tp = session_json["items"][0]["children"]
            for type_pos in range(len(tp)):
                if (tp[type_pos]["field"] == "experiments/experiment"):
                    for experiments_pos in range(len(tp[type_pos]["items"])):
                        accession_number = (tp[type_pos]["items"][experiments_pos]
                            ["data_fields"]["ID"])
                        project_real_id = tp[type_pos]["items"][experiments_pos]["data_fields"]["project"]
                        ssp=tp[type_pos]["items"][experiments_pos]["children"]
                        for scans_pos in range(len(ssp)):
                            if ssp[scans_pos]["field"] == "scans/scan":
                                sp = ssp[scans_pos]["items"]
                                dictionary_scans={}
                                for scan_pos in range(len(sp)):
                                    #print((sp[scan_pos]))
                                    number_scan = sp[scan_pos]["data_fields"]["ID"]
                                    frames_scan = sp[scan_pos]["data_fields"]["frames"]
                                    position_scan = (sp[scan_pos]
                                        ["data_fields"].get("parameters/orientation", ""))
                                    fp = sp[scan_pos]["children"][0]["items"]
                                    is_nifti = False
                                    for file_pos in range(len(fp)):
                                        #print((fp[file_pos]))
                                        if fp[file_pos]["data_fields"].get("label") == "NIFTI":
                                            is_nifti = True
                                            print((group_id + ", " + accession_number
                                            + ", " + str(number_scan) + ", " + str(frames_scan)
                                            + ", " + position_scan + ", " + str(is_nifti) + ', ' + subject_id))
                                            dictionary_scans[number_scan]=[frames_scan, position_scan]
                        session_dictionary[project_id
                            + "-" + accession_number] = (
                                [
                                    group_id, dictionary_scans, project_real_id
                                ]
                            )
    for item, value in session_dictionary.items():
        print ((value))
        for item_scan, value_scan in value[1].items():
            if not os.path.isdir(input_xnat):
                bash.bash_command("mkdir -p " + input_xnat)
            nifti_url= url + "/data/experiments/" + item.split('-')[1] + "/scans/" + item_scan + "/resources/NIFTI/files?format=zip&projectIncludedInPath=true&subjectIncludedInPath=true"
            out, err = bash.bash_command("wget --user=" + user +" --password=" + password + " --auth-no-challenge --no-check-certificate -P " + download_path + " " + nifti_url)
            print ((err))
            out, err = bash.bash_command("unzip -o -d " + download_path+' ' + download_path + "files*")
            out, err = bash.bash_command("find " + download_path + " -iname \"*.nii.gz\"")
            #for nii_files
            rename_path = out.split('\n')[0]
            #ut, err = bash.bash_command("mv " + out.split('\n')[0] +' '+ rename_path)
            dicom_url = ("https://ceib.cipf.es/xnat/REST/services/dicomdump?src="
                + "/archive/projects/" + value[2] + "/experiments/"
                + item.split('-')[1] + "/scans/" + item_scan
                + "&format=json")
            out, err = bash.bash_command("wget --user=" + user +" --password=" + password + " --auth-no-challenge --no-check-certificate -O " + rename_path[:-7]+".json" + " " + dicom_url)
            #bash.print_out_err("wget", out, err)
            print ((err))
            file_=file_funtions.FileInfo(rename_path[:-7]+".json")
            if file_.size < 100:
                #print("Error: dicom Header Void")
                #print("write exit or continue")
                import pdb
                pdb.set_trace()
            io_json.add_tag_dicom("(0008,0050)","Accesion Number",item.split('-')[1],file_.filepath)
            out, err = bash.bash_command("cp -r -d -f "+ download_path + value[0].split('_')[1] + ' ' + input_xnat)
            out, err = bash.bash_command("rm -r -d " + download_path +u'*')
            #bash.print_out_err("rm -r -d " + download_path +'*', out, err)
            #print ((err))
    io_objects.save_pickle(session_dictionary,dictionary_path + "dictionary_session.dic")
