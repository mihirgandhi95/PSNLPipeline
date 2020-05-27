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

