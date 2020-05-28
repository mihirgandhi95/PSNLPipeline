#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:27:53 2020

@author: mjgandhi
"""

# Standard Section of the Pipeline-----------------------------------------------------------------
# This section includes standard information that will always be used in the 
# pipeline. For more advanced instructions there will be a separate section. 


##@@@@@@@@@@@@@@---------OVERALL JSON STRUCTURE ---------------@@@@@@@@@@@@@@@##

# =============================================================================
# completeCommandList = {
#     "choices" : { },
#     "heudiconv": {},
#     "mriqc":{},
#     "fmriprep":{},
#     "smoothing":{},
#     "GLM":{},
#     "Analysis_ANOVA":{},
#     "Analysis_ISC":{},
#     "Analysis_RSA":{}
# }  
# =============================================================================

# PARSE JSON OBJECT TO CREATE CONTROL FLOWGRAPH AND ACCESS SPECIFIC SECTION ON CODE REQUIRED. 

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


# JSON structure to export all the field values for debugging Single Subject 
completeCommandList = {
    
    
# =============================================================================
#     # Which pieces of the pipeline do you want to implement?
#     # Answers
#     # Option 1 - Preprocessing - Yes or No
#     # Option 2 - Smoothing - Yes or No
#     # Option 3 - GLM - Yes or No
#     # Option 4 - Analysis 1- ANOVA - yes or no
#     # Option 5 - Analysis 2- ISC - yes or no
#     # Option 6 - Analysis 3 - RSA - yes or no
#     # Option 7 - Are you running your data through this pipeline the first time? - yes or no
#     # Option 8 - If option 7 is yes - Display Note that Heudiconv is mandatory the first time - If no display user must make sure
#     # data is input in correct format. 
#     # Option 9 - Do you want to run MRIQC? - yes or no
#     # Option 10 -  Do you want to run MRIQC on single subject or multiple subjects? - single /multiple
#     # Option 11 - Do you want to run FMRIPREP? - yes or no
#     # Option 12 - Do you want to run fMRIPREP on single subject or multiple subjects? - single/multiple
#     # Option 13 - Do you want to run GLM ? - yes or no?
#     # Option 14 - Do you want to run Analysis - ANOVA? yes or no?
#     # Option 15 - Do you want to run Analysis - ISC? yes or no?
#     # Option 16 - Do you want to run Analysis - RSA? yes or no?
# =============================================================================
    
    # Step0 - Choices
    "choices" : {
    
        "step0_Option1" : "",
        "step0_Option2" : "",
        "step0_Option3" : "",
        "step0_Option4" : "",
        "step0_Option5" : "",
        "step0_Option6" : "",
        "step0_Option7" : "",
        "step0_Option8" : "",
        "step0_Option9" : "",
        "step0_Option10" : "",
        "step0_Option11" : "",
        "step0_Option12" : "",
        "step0_Option13" : "",
        "step0_Option14" : "",
        "step0_Option15" : "",
        "step0_Option16" : "",
        "step0_Option17" : "",
        
    },
    
    
    #Step1 - Single Subject
    "heudiconv": {
        "step1_ScannerDir" : "",
        "step1_ProjectDir" : "",
        "step1_SubId" : 0,
        "step1_SessionID" : 1,
        "step1_RawDir" : "",
        "step1_FieldMaps" : "",
        "step1_IFFBeginning" : [],
        "step1_IFFInsert" : []
    },
    
   # -------------- BIDS Validator -----------------------------------------
   # -------------- Clarification ------------------------------------------ 
   # -------------- Defacing? --------------------
    
    
# =============================================================================
#     usage: mriqc [-h] [--version]
#              [--participant_label [PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]]
#              [--session-id [SESSION_ID [SESSION_ID ...]]]
#              [--run-id [RUN_ID [RUN_ID ...]]]
#              [--task-id [TASK_ID [TASK_ID ...]]]
#              [-m [{T1w,bold,T2w} [{T1w,bold,T2w} ...]]] [--dsname DSNAME]
#              [-w WORK_DIR] [--verbose-reports] [--write-graph] [--dry-run]
#              [--profile] [--use-plugin USE_PLUGIN] [--no-sub] [--email EMAIL]
#              [-v] [--webapi-url WEBAPI_URL] [--webapi-port WEBAPI_PORT]
#              [--upload-strict] [--n_procs N_PROCS] [--mem_gb MEM_GB]
#              [--testing] [-f] [--ica] [--hmc-afni] [--hmc-fsl]
#              [--fft-spikes-detector] [--fd_thres FD_THRES]
#              [--ants-nthreads ANTS_NTHREADS] [--ants-float]
#              [--ants-settings ANTS_SETTINGS] [--deoblique] [--despike]
#              [--start-idx START_IDX] [--stop-idx STOP_IDX]
#              [--correct-slice-timing]
#              bids_dir output_dir {participant,group} [{participant,group} ...]
# =============================================================================
    
    
    #Step2 - Single Subject
    # Advanced Options will only be available towards the end of the script 
    # at a later stage of development 
    # parameters that cannot be changed
    # 1) correct slice timing
    # 2) --no-sub
    "mriqc":{
        
        "step2_BidsDir" : "",
        "step2_WorkDir" : "",
        "step2_OutoutDir" : "",
        "step2_nprocs" : "",
        "step2_jobName": "",
        "step2_subjectNum": "",
        "step2_time": 180,
        "step2_CPUParam": 8,
        "step2_MemoryParam" : 10000,
        "step2_Email" : "", 
        "step2_LogfileOutput": ""
        
    },
    
# =============================================================================
#     usage: fmriprep [-h] [--version] [--skip_bids_validation]
#                 [--participant-label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
#                 [-t TASK_ID] [--echo-idx ECHO_IDX] [--bids-filter-file PATH]
#                 [--anat-derivatives PATH] [--nprocs NPROCS]
#                 [--omp-nthreads OMP_NTHREADS] [--mem MEMORY_GB] [--low-mem]
#                 [--use-plugin USE_PLUGIN] [--anat-only] [--boilerplate_only]
#                 [--md-only-boilerplate] [--error-on-aroma-warnings] [-v]
#                 [--ignore {fieldmaps,slicetiming,sbref} [{fieldmaps,slicetiming,sbref} ...]]
#                 [--longitudinal]
#                 [--output-spaces [OUTPUT_SPACES [OUTPUT_SPACES ...]]]
#                 [--bold2t1w-init {register,header}] [--bold2t1w-dof {6,9,12}]
#                 [--force-bbr] [--force-no-bbr] [--medial-surface-nan]
#                 [--dummy-scans DUMMY_SCANS] [--random-seed RANDOM_SEED]
#                 [--use-aroma]
#                 [--aroma-melodic-dimensionality AROMA_MELODIC_DIM]
#                 [--return-all-components]
#                 [--fd-spike-threshold REGRESSORS_FD_TH]
#                 [--dvars-spike-threshold REGRESSORS_DVARS_TH]
#                 [--skull-strip-template SKULL_STRIP_TEMPLATE]
#                 [--skull-strip-fixed-seed]
#                 [--skull-strip-t1w {auto,skip,force}] [--fmap-bspline]
#                 [--fmap-no-demean] [--use-syn-sdc] [--force-syn]
#                 [--fs-license-file PATH] [--fs-subjects-dir PATH]
#                 [--no-submm-recon] [--cifti-output [{91k,170k}] |
#                 --fs-no-reconall] [-w WORK_DIR] [--clean-workdir]
#                 [--resource-monitor] [--reports-only] [--run-uuid RUN_UUID]
#                 [--write-graph] [--stop-on-first-crash] [--notrack] [--sloppy]
#                 bids_dir output_dir {participant}
# =============================================================================
    
    
    #Step3 - Single Subject
    # Advanced Options will only be available towards the end of the script 
    # at a later stage of development
    # parameters that cannot be changed
    # 1) --skip_bids_validation 
    # 2) --bold2t1w-dof
    # 3) --medial-surface-nan
    # 4) --output-spaces
    # 5) --notrack
    "fmriprep":{
        
        "step3_BidsDir" : "",
        "step3_WorkDir" : "",
        "step3_OutoutDir" : "",
        "step3_licenseFile" : "",
        "step3_ompNthreads" : 8,
        "step3_nthreads" : 8,
        "step3_jobName": "",
        "step3_subjectNum": "",
        "step3_time": 180,
        "step3_CPUParam": 8,
        "step3_MemoryParam" : 10000,
        "step3_Email" : "",
        "step3_logFileOutput": ""
        
    },
    #Step4 - Single Subject
    "smoothing":{
        
    },
    #Step5 - Single Subject
    "GLM":{
        
    },
    #Step6 - Single Subject
    "Analysis_ANOVA":{
        
    },
    #Step7 - Single Subject
    "Analysis_ISC":{
        
    },
    #Step8 - Single Subject
    "Analysis_RSA":{
        
    }

}

############--------------CHOICES------------###############################

# =============================================================================
# # Option 1 - Preprocessing - Yes or No
# =============================================================================

step0_Option1 = "";

# =============================================================================
# # Option 2 - Smoothing - Yes or No
# =============================================================================

step0_Option2 = "";

# =============================================================================
# # Option 3 - GLM - Yes or No
# =============================================================================

step0_Option3 = "";

# =============================================================================
# # Option 4 - Analysis 1- ANOVA - yes or no
# =============================================================================

step0_Option4 = "";

# =============================================================================
# # Option 5 - Analysis 2- ISC - yes or no
# =============================================================================

step0_Option5 = "";

# =============================================================================
# # Option 6 - Analysis 3 - RSA - yes or no
# =============================================================================

step0_Option6 = "";

# =============================================================================
# # Option 7 - Are you running your data through this pipeline the first time? - yes or no
# =============================================================================

step0_Option7 = "";

# =============================================================================
# # Option 8 - If option 7 is yes - Display Note that Heudiconv is mandatory the first time - If no display user must make sure
# # data is input in correct format. 
# =============================================================================

step0_Option8 = "";

# =============================================================================
# # Option 9 - Do you want to run MRIQC? - yes or no
# =============================================================================

step0_Option9 = "";

# =============================================================================
# # Option 10 -  Do you want to run MRIQC on single subject or multiple subjects? - single /multiple
# =============================================================================

step0_Option10 = "";

# =============================================================================
# # Option 11 - Do you want to run FMRIPREP? - yes or no
# =============================================================================

step0_Option11 = "";

# =============================================================================
# # Option 12 - Do you want to run fMRIPREP on single subject or multiple subjects? - single/multiple
# =============================================================================

step0_Option12 = "";

# =============================================================================
# # Option 13 - Do you want to run GLM ? - yes or no?
# =============================================================================

step0_Option13 = "";

# =============================================================================
# # Option 14 - Do you want to run Analysis - ANOVA? yes or no?
# =============================================================================

step0_Option14 = "";

# =============================================================================
# # Option 15 - Do you want to run Analysis - ISC? yes or no?
# =============================================================================

step0_Option15 = "";


# =============================================================================
# # Option 16 - Do you want to run Analysis - RSA? yes or no?
# =============================================================================

step0_Option16 = "";

############--------------HEUDICONV------------###############################

# =============================================================================
# scanner_directory - Directory where the files on the scanner are stored. 
# =============================================================================
step1_ScannerDir = "";

# =============================================================================
# project directory - Directory where your project is 
# =============================================================================
step1_ProjectDir = "";

# =============================================================================
# Enter the subjectID fr the subject you want to run heudiconv on 
# =============================================================================
step1_SubId = 0;

# =============================================================================
# SessionID - default will be 01 for all subjects unless you want to include 
# =============================================================================
step1_SessionID = 1;

# =============================================================================
# List of directory names for the folders that contain the raw data for the subjects
# =============================================================================
step1_RawDir = "";

# =============================================================================
# # default is one session only and no multiple day experiments
# # If you want to use fieldmaps for susceptibility distortion correction, 
# # enter the IntendedFor field
# =============================================================================
step1_FieldMap= "";

# =============================================================================
# # SESSION 1: list all run filenames
# # =============================================================================
# # beginning='"IntendedFor": ['
# # run1="\""ses-01/func/sub-${subj}_ses-01_task-Black_run-01_bold.nii.gz"\","
# # run2="\""ses-01/func/sub-${subj}_ses-01_task-Conv_run-01_bold.nii.gz"\","
# # run3="\""ses-01/func/sub-${subj}_ses-01_task-Conv_run-02_bold.nii.gz"\","
# # run4="\""ses-01/func/sub-${subj}_ses-01_task-Conv_run-03_bold.nii.gz"\","
# # run5="\""ses-01/func/sub-${subj}_ses-01_task-Conv_run-04_bold.nii.gz"\","
# # run6="\""ses-01/func/sub-${subj}_ses-01_task-Conv_run-05_bold.nii.gz"\""
# # end="],"
# =============================================================================
step1_IFFBeginning = [];

# =============================================================================
# 
# # insert="${beginning}${run1} ${run2} ${run3} ${run4} ${run5} ${run6}${end}"
# # 
# # # insert IntendedFor field after line 35 (i.e., it becomes the new line 36)
# # sed -i "35 a \ \ ${insert}" $bids_dir/sub-$subj/ses-01/fmap/sub-${subj}_ses-01_dir-AP_epi.json
# # sed -i "35 a \ \ ${insert}" $bids_dir/sub-$subj/ses-01/fmap/sub-${subj}_ses-01_dir-PA_epi.json
# # =============================================================================
# =============================================================================
step1_IFFInsert = [];


############--------------MRIQC----------------###############################

# =============================================================================
# bids_dir	The directory with the input dataset formatted according to the BIDS standard.
# =============================================================================
step2_BidsDir = "";

# =============================================================================
# -w, --work-dir	change the folder to store intermediate results
# =============================================================================
step2_WorkDir = "";

# =============================================================================
# output_dir	The directory where the output files should be stored. If you are running group level analysis this folder should be prepopulated with the results of theparticipant level analysis.
# =============================================================================
step2_OutoutDir = "";


# =============================================================================
# --n_procs, --nprocs, --n_cpus, --nprocs
#  	number of threads
# =============================================================================
step2_nprocs = "";

# =============================================================================
# Enter the name that you want to give this job
# =============================================================================
step2_jobName = "";

# =============================================================================
# Enter the subject number for whom you want to run MRIQC
# =============================================================================
step2_subjectNum = "";

# =============================================================================
# Enter the time you think MRIQC will take to complete in minutes
# =============================================================================
step2_time = 180;

# =============================================================================
# Enter the CPUs per task you need 
# =============================================================================
step2_CPUParam = 8;

# =============================================================================
# Enter the Memory per CPU you want to request
# =============================================================================
step2_MemoryParam = 10000;

# =============================================================================
# Enter the email address where you want to be notified of jobs
# =============================================================================
step2_Email = "";

# =============================================================================
# Enter the location where you want the log files from MRIQC to be written
# =============================================================================
step2_LogfileOutput = "";


############--------------FMRIPREP------------###############################

# =============================================================================
# bids_dir	The directory with the input dataset formatted according to the BIDS standard.
# =============================================================================
step3_BidsDir = "";

# =============================================================================
# -w, --work-dir	change the folder to store intermediate results
# =============================================================================
step3_WorkDir = "";

# =============================================================================
# output_dir	The directory where the output files should be stored. If you are running group level analysis this folder should be prepopulated with the results of theparticipant level analysis.
# =============================================================================
step3_OutoutDir = "";

# =============================================================================
# --fs-license-file
# Path to FreeSurfer license key file. Get it (for free) by registering at https://surfer.nmr.mgh.harvard.edu/registration.html
# =============================================================================
step3_licenseFile = "";

# =============================================================================
# --omp-nthreads
# maximum number of threads per-process
# =============================================================================
step3_ompNthreads = 8;

# =============================================================================
# --nprocs, --nthreads, --n_cpus, --n-cpus
# maximum number of threads across all processes
# =============================================================================
step3_nthreads = 8;

# =============================================================================
# Enter the name that you want to give this job
# =============================================================================
step3_jobName = "";

# =============================================================================
# Enter the subject number for whom you want to run MRIQC
# =============================================================================
step3_subjectNum = "";

# =============================================================================
# Enter the time you think MRIQC will take to complete in minutes
# =============================================================================
step3_time = 180;

# =============================================================================
# Enter the CPUs per task you need 
# =============================================================================
step3_CPUParam = 8;

# =============================================================================
# Enter the Memory per CPU you want to request
# =============================================================================
step3_MemoryParam = 10000;

# =============================================================================
# Enter the email address where you want to be notified of jobs
# =============================================================================
step3_Email = "";

# =============================================================================
# Enter the location where you want the log files from MRIQC to be written
# =============================================================================
step3_logFileOutput = "";
        

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Append Everything to the JSON Object  Will be added once the data 
# structure is finalized
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
