#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 13:30:27 2020

@author: mjgandhi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 13:11:27 2020

@author: mjgandhi
"""

#!/usr/bin/env python
# make sure anacondapy/5.3.1 is loaded before running (otherwise run will not be imported from subprocess)
import logging
# logging.basicConfig(filename='doEverythingTrial1.log',level=logging.DEBUG)




import sys
import subprocess
from glob import glob
from os.path import exists, join
import json

# Logging 
# https://www.toptal.com/python/in-depth-python-logging
from logging.handlers import TimedRotatingFileHandler
FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "DoEverything_05_15_2020.log"

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler
def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger


my_logger = get_logger("HeudiConvModule")
my_logger.debug("Starting the DoEverything Script")



# Top Section 
# 3 things 
# Smoothing
# GLM 
# Analysis



# Which pieces for the pipeline do you want to implement?
# 1) BIDS Conversion heudiconv Mandatory first time 
# Different GLM not run heudiconv again--- Set flag
# Comments has to be done the first time 


# 2) MRIQC - Separate - input different - Set Flag 
# 3) fRMIPREP -  Separate - input different -- Set flag
# Options to turn on /off 
# 1) Aroma - Never used don't include give control advanced part of
# script 
# 2) recommendations for standard 
# 3) [--fd-spike-threshold FD_SPIKE_THRESHOLD]
#    [--dvars-spike-threshold DVARS_SPIKE_THRESHOLD]
# 4) Change the number of threads + omp-threads Note the defaults
# 5) --mem_mb MEM_MB modify
# 7) Output Spaces 
# 8) default slice timing - use fmriprep - advanced options
# slice timing - mriqc - default don't use it
# --fd_thres motion threshold for FD computation same options as slice timing

# Default Dummy scan = 0  
# dummyscan = 3
# Dummy Scan Question - MultiBand Not an issue
# Smoothing AFNI Smoothing - Option to turn on and off



#Running scripts via shell
# just executes the command doesn't print anything out 

# ls = 'ls'

# subprocess.call([ls, '-l'], shell=False);

# var = subprocess.call(['ls', '-l'], shell=True);
# print(var)


# Input the parameter values required for the code to run. Script0.py is the 
# base script that affects all the other scripts in the base folder.


####################################---1---####################################
# Globals.sh variables required 
# scanner_directory - Directory where the files on the scanner are stored. 
# project directory - Directory where your project is 


####################################---2---####################################
# run_heudiconv.py variables required 
# heudiconv_version - version of heudiconv you want to use 


####################################---3---####################################
# step1_preproc.sh variables required 
# List of subjects you want to run heudiconv on - [01,02,03,...] 
# SessionID - default will be 01 for all subjects unless you want to include 
# multiple day studies
# List of directory names for the folders that contain the raw data for the subjects
# Make sure the data directories are properly arranged in the list according to the subject numbers


####################################---4---####################################
# step2_preproc variables required 
# Are you using fieldmaps? Yes or no
# default is one session only and no multiple day experiments
# If you want to use fieldmaps for susceptibility distortion correction, 
# enter the IntendedFor field
# e.g.
#
# SESSION 1: list all run filenames
# =============================================================================
# beginning='"IntendedFor": ['
# run1="\""ses-01/func/sub-${subj}_ses-01_task-Black_run-01_bold.nii.gz"\","
# run2="\""ses-01/func/sub-${subj}_ses-01_task-Conv_run-01_bold.nii.gz"\","
# run3="\""ses-01/func/sub-${subj}_ses-01_task-Conv_run-02_bold.nii.gz"\","
# run4="\""ses-01/func/sub-${subj}_ses-01_task-Conv_run-03_bold.nii.gz"\","
# run5="\""ses-01/func/sub-${subj}_ses-01_task-Conv_run-04_bold.nii.gz"\","
# run6="\""ses-01/func/sub-${subj}_ses-01_task-Conv_run-05_bold.nii.gz"\""
# end="],"
# 
# insert="${beginning}${run1} ${run2} ${run3} ${run4} ${run5} ${run6}${end}"
# 
# # insert IntendedFor field after line 35 (i.e., it becomes the new line 36)
# sed -i "35 a \ \ ${insert}" $bids_dir/sub-$subj/ses-01/fmap/sub-${subj}_ses-01_dir-AP_epi.json
# sed -i "35 a \ \ ${insert}" $bids_dir/sub-$subj/ses-01/fmap/sub-${subj}_ses-01_dir-PA_epi.json
# =============================================================================
 


####################################---5---####################################
# Current default single subject for MRIQC 
# run_mriqc.sh variables required Default mriqc version will be used 
# bids_dir = Directory where the bids folder is located 
# e.g. bids_dir=/jukebox/tamir/mjgandhi/heudiconv/HEUDICONV/MRIQC_checker/mriqc_3/data/bids



####################################---6---####################################
# Current default single subject subject for MRIQC 
# slurm_mriqc.sh variables required
# subjectIdNumber = subject number to run
# Email for slurm messages - Enter email for the messages when the task begins, ends and if it fails



####################################---7---####################################
# Current default single subject for FMRIPREP
# run_fmriprep.sh variables required Default fmriprep version will be used 
# fieldmaps_considered: If fieldmaps are to be considered leave as empty 
# if you don't want to use fieldmaps - enter '--ignore fieldmaps' in this field
# longitudinal - if you want to use 2 T1W images or more set this field to 'longitudinal'
# else leave this field empty



####################################---8---####################################
# Current default single subject subject for FMRIPREP 
# slurm_fmriprep.sh variables required
# subjectIdNumber = subject number to run
# Email for slurm messages - Enter email for the messages when the task begins, ends and if it fails
# cpus-per-task will be set to default- 12
# --mem-per-cpu will be set to default - 24000
#  time per job will be set to 34 hours




#Unique values to be set before we run the files:
# =============================================================================
# 1)  globals_Scanner_Directory = ""

globals_Scanner_Directory = ""
print(globals_Scanner_Directory);


# 2)  globals_Project_Directory = "" 
# 3)  heudiconv_version = "0.7.0" # "0.6.0", "0.7.0", ......
# 4)  heudiconv_Subject_List = ['01', '02', '03']
# 5)  sessionId = '01' 
# 6)  heudiconv_directory_names = [] # ['647467_sub_conv_02'............]
# 7)  fieldmaps_used = 'yes' # yes or no
# 8)  intendedForFieldBeginning = ['Black', 'Conv', 'Conv', 'Conv', 'Conv', 'Conv'] 
# BlackRunCount = 3 # translates to run01 - run-02 run-03
# ConvRunCount = 3
# 9)  intendedForFieldInsert = ['run1', 'run2', 'run3', 'run4', 'run5', 'run6'];
# 10) runMriqcBidsDir = "" # bids_dir=/jukebox/tamir/mjgandhi/heudiconv/HEUDICONV/MRIQC_checker/mriqc_3/data/bids
# 11) slurmMriqcSubjectID = "" # "007"
# 12) slurmMriqcEmailID = "" # "mjgandhi@xyz.com"
# 13) runFmriprepFieldmaps = "" # If yes - leave blank if no enter "--ignore fieldmaps"
# 14) runFmriprepLongitudinal = "" # If no - leave blank if yes enter "--longitudinal"
# 15) slurmFmriprepSubjectIdNumber = "" # "007"
# 16) slurmFmriprepEmailID = "" # "mjgandhi@xyz.com"
# 
# =============================================================================


# JSON structure to export all the field values for debugging 
completeCommandList = {
  "globals_Scanner_Directory": "",
  "globals_ProjectDirectory": "",
  "heudiconv_version": "",
  "heudiconv_Subject_List": [],
  "sessionId": "",
  "heudiconv_directory_names": [],
  "fieldmaps_used" : "",
  "intendedForFieldBeginning" : [],
  "intendedForFieldInsert" : [],
  "runMriqcBidsDir" : "",
  "slurmMriqcSubjectID" : "",
  "slurmMriqcEmailID": "",
  "runFmriprepFieldmaps" : "",
  "runFmriprepLongitudinal" : "",
  "slurmFmriprepSubjectIdNumber" : "",
  "slurmFmriprepEmailID": ""
}

my_logger.warning("Taking input from user about the different fields required to run the script")



globals_ProjectDirectory = ""
print(globals_ProjectDirectory);

heudiconv_version = ""
print(heudiconv_version);

heudiconv_Subject_List = [];
print(heudiconv_Subject_List);

sessionId = ""
print(sessionId);

heudiconv_directory_names = []
print(heudiconv_directory_names);

fieldmaps_used ="";
print(fieldmaps_used);

intendedForFieldBeginning = []
print(intendedForFieldBeginning);

intendedForFieldInsert = []
print(intendedForFieldInsert);

runMriqcBidsDir = ""
print(runMriqcBidsDir);

slurmMriqcSubjectID = "";
print(slurmMriqcSubjectID);

slurmMriqcEmailID = ""
print(slurmMriqcEmailID);

runFmriprepFieldmaps = ""
print(runFmriprepFieldmaps);

runFmriprepLongitudinal = "";
print(runFmriprepLongitudinal);

slurmFmriprepSubjectIdNumber = ""
print(slurmFmriprepSubjectIdNumber);

slurmFmriprepEmailID = ""
print(slurmFmriprepEmailID);

my_logger.info("Writing the values for the different variables to the JSON Object")

# Append Everything to the JSON Object 
completeCommandList["globals_Scanner_Directory"] = globals_Scanner_Directory
completeCommandList["globals_ProjectDirectory"] = globals_ProjectDirectory
completeCommandList["heudiconv_version"] = heudiconv_version
completeCommandList["heudiconv_Subject_List"] = heudiconv_Subject_List
completeCommandList["sessionId"] = sessionId
completeCommandList["heudiconv_directory_names"] = heudiconv_directory_names
completeCommandList["fieldmaps_used"] = fieldmaps_used
completeCommandList["intendedForFieldBeginning"] = intendedForFieldBeginning
completeCommandList["intendedForFieldInsert"] = intendedForFieldInsert
completeCommandList["runMriqcBidsDir"] = runMriqcBidsDir
completeCommandList["slurmMriqcSubjectID"] = slurmMriqcSubjectID
completeCommandList["slurmMriqcEmailID"] = slurmMriqcEmailID
completeCommandList["runFmriprepFieldmaps"] = runFmriprepFieldmaps
completeCommandList["runFmriprepLongitudinal"] = runFmriprepLongitudinal
completeCommandList["slurmFmriprepSubjectIdNumber"] = slurmFmriprepSubjectIdNumber


# my_logger = get_logger("MRIQCModule")
my_logger.debug("starting MRIQC Running")

# Writing JSON Object to a file
with open('completeCommandListJSON.json', 'w', encoding='utf-8') as f:
    json.dump(completeCommandList, f, ensure_ascii=False, indent=4)   


# my_logger = get_logger("fMRIPrepModule")
my_logger.debug("starting fMRIPrep Running")



# Different folders for different tasks
# Preprocessing Work - Multiple Stages
# Separate for which section you want to do
# parameters for the step 
# More Local Less Centralized  --- Instructions where the files are 

