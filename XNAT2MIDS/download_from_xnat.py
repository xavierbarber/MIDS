
# -*- coding: utf-8 -*-

###############################################################################
# Imports
###############################################################################
import xnat
import os, errno
from time import sleep
import pydicom
import json
import lib.Bash_functions.bash_exe as bash
import lib.IO_Functions.file_class as file_funtions
import lib.IO_Functions.io_json as io_json
import lib.IO_Functions.io_objects as io_objects

page = "https://central.xnat.org" #"https://central.xnat.org"#"https://xnat.bmia.nl/"
user = "josator2"
path_download = '/home/josator2/Escritorio/prueba'
want_dicom=False
want_nifti=True
want_bids=False

def get_projects(page, user):
    project_dict = []
    if(user):
        with xnat.connect(page, user=user, verify=False) as session:
            for p in session.projects.keys():
                project_dict.append(p)
    else:
        with xnat.connect(page, verify=False) as session:
            for p in session.projects.keys():
                project_dict.append(p)

    return project_dict


def show_projects(page, user):
    project_dict = get_projects(page, user)
    loop = True
    while loop:
        for i, project_item in enumerate(project_dict):
            if not i % 3:
                print((""))
            string = str(i+1) + ") " + project_item
            print("{0:20s}".format(string), end=" ", flush=True)
        answer = input("\nChosee the project: ")
        answer = str(answer)
        answer_list = []
        answer_list_aux = answer.split(' ')
        m = 0
        for ans in answer_list_aux:
            if ans.isdigit():
                ans = int(ans) - 1
                if ans >= len(project_dict):
                    print("the number "+ ans +" is not corrected, try again")
                    break
                else:
                    answer_list.append(project_dict[ans])
            else:
                if not (ans in project_dict):
                    if ans is "exit":
                        exit(1)
                        print("the proyect " + ans
                               + " is not corrected, try again")
                        continue
                    else:
                        answer_list.append(ans)
            m += 1
        print(answer_list)
        if m >= len(answer_list):
            loop = False
    return answer_list

#def return_slides(json_dict):
#    json_dict["children"][0]["field"][0]["children"][][][][][][]
def download_projects(page, user, project_list, path_download,want_dicom,
                      want_nifti,wnat_bids):
    if(user):
        session = xnat.connect(page, user=user, verify=False)
    else:
        session = xnat.connect(page, verify=False)
    print(path_download)
    for project in project_list:
        try:
            os.mkdir(path_download + project)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open(path_download + project +"/"+project+".log", "w") as f:
            f.write("log error for project "+ project)
        d=session.projects.get(project).subjects
        for enum,subject in enumerate(d.values()):
            subject_label = subject.label
            sleep(0.05)
            print("subject id "+str(enum)+": " + subject_label)
            #if enum<44:continue
            experiments=subject.experiments.values()
            for experiment in experiments:
                experiment_label = experiment.label
                print("Experiment_label: " + experiment_label)
                scans=experiment.scans.values()
                for scan in scans:
                    try:
                        desc="" + scan.type
                    except TypeError as e:
                        print("scans series description is None")
                        desc="unknown"
                        pass

                    scan_label = scan.id + "-" + desc
                    print("Scan label: "+scan_label)
                    resources=scan.resources.values()
                    for resource in resources:
                        if "BIDS" in resource.fulluri and want_bids:
                            print("downloaded BIDS session: "+ experiment_label)
                            i=0
                            while i<10:
                                try:
                                    resource.download_dir(path_download
                                                          + project + "/"
                                                          + subject_label+"/"
                                                          )
                                    with open(path_download + project + "/"
                                              + project + ".log", "a") as f:
                                        f.write("subject " + experiment_label
                                                + " BIDS: success download"
                                                )
                                    break
                                except xnat.exceptions.XNATResponseError as e:
                                    sleep(0.05)
                                    print("subject " + experiment_label
                                          + ": error to download DICOM "
                                          + "files by " + e
                                          )
                                    with open(path_download + project + "/"
                                              + project + ".log", "a") as f:
                                        f.write("subject " + experiment_label
                                                + ": error to download DICOM "
                                                + "files by " + e
                                                )
                                    i+=1
                        if "DICOM" in resource.fulluri and want_dicom:
                            print("downloaded DICOM session: "
                                  + experiment_label)
                            i=0
                            while i<10:
                                try:
                                    resource.download_dir(path_download
                                                          + project + "/"
                                                          + subject_label+"/"
                                                          )
                                    with open(path_download + project + "/"
                                              + project + ".log", "a") as f:
                                        f.write("subject "+ experiment_label
                                                + " DICOM: success download"
                                                )
                                    break
                                except xnat.exceptions.XNATResponseError as e:
                                    sleep(0.05)
                                    print("subject " + experiment_label
                                          + ": error to download DICOM "
                                          + "files by " + e
                                          )
                                    with open(path_download + project + "/"
                                              + project+".log", "a") as f:
                                        f.write("subject " + experiment_label
                                                + ": error to download DICOM "
                                                + "files by " + e
                                                )
                                    i+=1
                        if "NIFTI" in resource.fulluri and want_nifti:
                            print("download NIFTI session: "+ experiment_label)
                            i=0
                            while i<10:
                                try:
                                    resource.download_dir(path_download
                                                          + project + "/"
                                                          + subject_label+"/"
                                                          )
                                    with open(path_download + project + "/"
                                              + project+".log", "a") as f:
                                        f.write("subject " + experiment_label
                                                +" NIFTI: success download"
                                                )
                                    break
                                except xnat.exceptions.XNATResponseError as e:
                                    sleep(0.05)
                                    print("subject "+ experiment_label
                                          + ": error to download NIFTI "
                                          + "files by " + e
                                          )
                                    with open(path_download + project + "/"
                                              + project + ".log", "a") as f:
                                        f.write("subject " + experiment_label
                                                + ": error to download DICOM "
                                                + "files by " + e
                                                )
                                    i+=1
                            dicom=scan.dicom_dump()
                            #print(dicom)
                            file_json=(path_download + project+"/"
                                       +subject_label+"/"
                                       +experiment_label+"/"
                                       +"scans/"
                                       +scan_label+"/"
                                       +"resources/NIFTI/files/"
                                       +list(resource.files)[0][:-7]+".json"
                                      )
                            print("download DICOM METADATA session: "
                                  + experiment_label
                                  )

                            # with open(file_json, 'w') as f:
                            #     json.dump(dicom, f, ensure_ascii=False)
                            io_json.save_json(dicom, file_json)
#download_projects(page, user, show_projects(page,user), path_download,want_dicom,want_nifti)
"""a=pydicom.read_file("path\to\your\DICOM\file.IMA")
IOP = a.ImageOrientationPatient
plane = file_plane(IOP)
def file_plane(IOP):
    IOP_round = [round(x) for x in IOP]
    plane = np.cross(IOP_round[0:3], IOP_round[3:6])
    plane = [abs(x) for x in plane]
    if plane[0] == 1:
        return "Sagittal"
    elif plane[1] == 1:
        return "Coronal"
    elif plane[2] == 1:
        return "Transverse"""
