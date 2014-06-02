#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Constants for use by all modules
"""

import math
import logging
import os

# Party names
CON = "Conservative"
LAB = "Labour"
LD = "Lib-Dem"
SNP = "SNP"
PC = "PC"
GRN = "Green"
BNP = "BNP"
UKP = "UKIP"
OTH = "Other"

# Data CSV file paths
HARVARD_CSV = "harvard_election_results_2010.csv"
GUARDIAN_CSV = "guardian_election_results_2010.csv"

# Constituency numbers (only including those contested in 2010)
NUM_OF_CONSTITUENCIES = 649
NEEDED_FOR_MAJORITY = int(math.ceil(NUM_OF_CONSTITUENCIES / 2)) 

# Tuning parameters for the model
RESULT_TOLERANCE = 0.02 # In percentage points divided by 100
SUPPORT_VARIATION = 0.005 # Also in percentage points
SWING_SCALE_FACTOR = 1.5 # Scale the amount of variance in vote numbers by this

# Logging
LOGS_DIR = "logs"
LOG_FILE = os.path.join(LOGS_DIR, "electobot.log")
LOG_LEVEL = logging.INFO