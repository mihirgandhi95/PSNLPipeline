#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:27:53 2020

@author: mjgandhi
"""

# Question 1-----------------------------------------------------------------
# Which pieces of the pipeline do you want to implement?
# Answers
# Option 1 - Preprocessing - Yes or No
# Option 2 - Smoothing - Yes or No
# Option 3 - GLM - Yes or No
# Option 4 - Analysis 1- ANOVA - yes or no
# Option 5 - Analysis 2- ISC - yes or no
# Option 6 - Analysis 3 - RSA - yes or no
# Option 7 - Are you running your data through this pipeline the first time? - yes or no
# Option 8 - If option 7 is yes - Display Note that Heudiconv is mandatory the first time - If no display user must make sure
# data is input in correct format. 
# Option 9 - Do you want to run MRIQC? - yes or no
# Option 10 -  Do you want to run MRIQC on single subject or multiple subjects? - single /multiple
# Option 11 - Do you want to run FMRIPREP? - yes or no
# Option 12 - Do you want to run fMRIPREP on single subject or multiple subjects? - single/multiple
# Option 13 - Do you want to run GLM ? - yes or no?
# Option 14 - Do you want to run Analysis - ANOVA? yes or no?
# Option 15 - Do you want to run Analysis - ISC? yes or no?
# Option 16 - Do you want to run Analysis - RSA? yes or no?

# Store into JSON Structure

# Standard Section of the Pipeline-----------------------------------------------------------------
# This section includes standard information that will always be used in the 
# pipeline. For more advanced instructions there will be a separate section. 

#PARSE JSON OBJECT TO CREATE CONTROL FLOWGRAPH AND ACCESS SPECIFIC SECTION ON CODE REQUIRED. 

# ADDITONAL STANDARD INPUT SECTION CONTROL FLOW GRAPH

# PREPROCESSING CONTROL FLOWGRAPH
# Option 1 - Yes Section
# Preprocessing is going to be performed using the pipeline 
    # Option 7 First Time - Yes SubSection
        # Option 9 MRIQC- Yes Subsection 
            # Option 10 MRIQC - single Subsection
                # Option 11 - FMRIPREP - yes subsection
                    #Option 12 - FMRIPREP - single subsection
                    #Option 12- FMRIPREP - multiple subsection
                # Option 11 - FMRIPREP - no subsection 
            # Option 10 MRIQC - multiple subsection
                # Option 11 - FMRIPREP - yes subsection
                    #Option 12 - FMRIPREP - single subsection
                    #Option 12- FMRIPREP - multiple subsection
                # Option 11 - FMRIPREP - no subsection
        # Option 9 MRIQC - No Subsection
            # Option 11 - FMRIPREP - yes subsection
                #Option 12 - FMRIPREP - single subsection
                #Option 12- FMRIPREP - multiple subsection
            # Option 11 - FMRIPREP - no subsection            
    # Option 7 First Time - No Subsection
        # Option 9 MRIQC- Yes Subsection 
            # Option 10 MRIQC - single Subsection
                # Option 11 - FMRIPREP - yes subsection
                    #Option 12 - FMRIPREP - single subsection
                    #Option 12- FMRIPREP - multiple subsection
                # Option 11 - FMRIPREP - no subsection 
            # Option 10 MRIQC - multiple subsection
                # Option 11 - FMRIPREP - yes subsection
                    #Option 12 - FMRIPREP - single subsection
                    #Option 12- FMRIPREP - multiple subsection
                # Option 11 - FMRIPREP - no subsection
        # Option 9 MRIQC - No Subsection
            # Option 11 - FMRIPREP - yes subsection
                #Option 12 - FMRIPREP - single subsection
                #Option 12- FMRIPREP - multiple subsection
            # Option 11 - FMRIPREP - no subsection

# GLM And Analysis Control Flow - Will require modification 
# Option 13 - yes Section 
    # Option 14 - yes subsection
        #Option 15 yes Subsection
            #Option 16 yes Subsection 
            #Option 16 No Subsection
        #Option 15 no Subsection
            #Option 16 yes Subsection
            #Option 16 no Subsection
    # Option 14 - no subsection
        #Option 15 yes Subsection
            #Option 16 yes Subsection 
            #Option 16 No Subsection
        #Option 15 no Subsection
            #Option 16 yes Subsection
            #Option 16 no Subsection
# Option 13 - No Section
    # Option 14 - yes subsection
        #Option 15 yes Subsection
            #Option 16 yes Subsection 
            #Option 16 No Subsection
        #Option 15 no Subsection
            #Option 16 yes Subsection
            #Option 16 no Subsection
    # Option 14 - no subsection
        #Option 15 yes Subsection
            #Option 16 yes Subsection 
            #Option 16 No Subsection
        #Option 15 no Subsection
            #Option 16 yes Subsection
            #Option 16 no Subsection





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


#Folder Code Structure 
# =============================================================================
# $ tree
# 
# └── new_study_template               # copy this directory to setup the entire directory structure for a new project
#     └── code
#         └── preprocessing            # this is where heudiconv, fmriprep, mriqc scripts live
#             └── license.txt          # SEE NOTE!
#         └── analysis                 # [example] any other code can live at this level
#         └── task                     # [example]
#     └── data
#         └── bids                     # this is where raw BIDS data will be saved by HeuDiConv
#             └── sub-001
#             └── sub-002
#             └── etc.
#             └── derivatives          # this is where all your BIDS derivatives will be
#                 └── deface           # defaced T1 images go here SEE NOTE!
#                     └── logs         # slurm logs will go here
#                 └── fmriprep         # fmriprep-preprocessed data will go here
#                     └── logs         # slurm logs will go here
#                 └── freesurfer       # fmriprep will also run freesurfer reconstruction and output goes here
#                 └── mriqc            # mriqc output will go here
#                     └── logs         # slurm logs will go here
#             └── .bidsignore          # similar to .gitignore, list all files/directories you don’t want to be checked by the bids-validator
#         └── dicom                    # raw dicoms copied from the scanner go here
#             └── check_volumes        # outputs checking that all dicoms transferred
#         └── behavioral               # [example] any other data can live at this level
# =============================================================================


# JSON structure to export all the field values for debugging 
completeCommandList = {
    
    "heudiconv":{
            
    },
    "mriqc":{
        
    },
    "fmriprep":{
        
    },
    "smoothing":{
        
    },
    "GLM":{
        
    },
    "Analysis_ANOVA":{
        
    },
    "Analysis_ISC":{
        
    },
    "Analysis_RSA":{
        
    }

}

####################################---1---####################################
# 1)  globals_Scanner_Directory = ""
# Globals.sh variables required 
# scanner_directory - Directory where the files on the scanner are stored. 
# project directory - Directory where your project is 
globals_Scanner_Directory = ""
print(globals_Scanner_Directory);


# 2) globals_Project_Directory = "" 
globals_ProjectDirectory = ""
print(globals_ProjectDirectory);


####################################---2---####################################
# run_heudiconv.py variables required 
# heudiconv_version - version of heudiconv you want to use 

heudiconv_version = ""
print(heudiconv_version);



####################################---3---####################################
# step1_preproc.sh variables required 
# List of subjects you want to run heudiconv on - [01,02,03,...] 
# SessionID - default will be 01 for all subjects unless you want to include 
# multiple day studies
# List of directory names for the folders that contain the raw data for the subjects
# Make sure the data directories are properly arranged in the list according to the subject numbers

heudiconv_Subject_List = [];
print(heudiconv_Subject_List);

sessionId = ""
print(sessionId);

heudiconv_directory_names = []
print(heudiconv_directory_names);



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
 
fieldmaps_used ="";
print(fieldmaps_used);

intendedForFieldBeginning = []
print(intendedForFieldBeginning);

intendedForFieldInsert = []
print(intendedForFieldInsert);




####################################---5---####################################
# Current default single subject for MRIQC 
# run_mriqc.sh variables required Default mriqc version will be used 
# bids_dir = Directory where the bids folder is located 
# e.g. bids_dir=/jukebox/tamir/mjgandhi/heudiconv/HEUDICONV/MRIQC_checker/mriqc_3/data/bids

runMriqcBidsDir = ""
print(runMriqcBidsDir);


####################################---6---####################################
# Current default single subject subject for MRIQC 
# slurm_mriqc.sh variables required
# subjectIdNumber = subject number to run
# Email for slurm messages - Enter email for the messages when the task begins, ends and if it fails

slurmMriqcSubjectID = "";
print(slurmMriqcSubjectID);

slurmMriqcEmailID = ""
print(slurmMriqcEmailID);


####################################---7---####################################
# Current default single subject for FMRIPREP
# run_fmriprep.sh variables required Default fmriprep version will be used 
# fieldmaps_considered: If fieldmaps are to be considered leave as empty 
# if you don't want to use fieldmaps - enter '--ignore fieldmaps' in this field
# longitudinal - if you want to use 2 T1W images or more set this field to 'longitudinal'
# else leave this field empty

runFmriprepFieldmaps = ""
print(runFmriprepFieldmaps);

runFmriprepLongitudinal = "";
print(runFmriprepLongitudinal);



####################################---8---####################################
# Current default single subject subject for FMRIPREP 
# slurm_fmriprep.sh variables required
# subjectIdNumber = subject number to run
# Email for slurm messages - Enter email for the messages when the task begins, ends and if it fails
# cpus-per-task will be set to default- 12
# --mem-per-cpu will be set to default - 24000
#  time per job will be set to 34 hours

slurmFmriprepSubjectIdNumber = ""
print(slurmFmriprepSubjectIdNumber);

slurmFmriprepEmailID = ""
print(slurmFmriprepEmailID);




