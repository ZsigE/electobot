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

# List of all party names
PARTY_NAMES = [CON, LAB, LD, SNP, PC, GRN, BNP, UKP, OTH]

# Colours to represent each party, in matplotlib colour identifiers
PARTY_COLOURS = {CON: "b",
                 LAB: "r",
                 LD:  "Orange",
                 SNP: "Yellow",
                 PC:  "DarkGreen",
                 GRN: "g",
                 BNP: "Indigo",
                 UKP: "Purple",
                 OTH: "Gray"}

# Data CSV file paths
RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..",
                            "res")
HARVARD_CSV = os.path.join(RESOURCE_DIR, "harvard_election_results_2010.csv")
GUARDIAN_CSV = os.path.join(RESOURCE_DIR, "guardian_election_results_2010.csv")

# Wikipedia's historical poll data API URL
WIKI_POLLS_URL = ("http://en.wikipedia.org/w/api.php?action=parse&prop=text&"
                  "page=Opinion_polling_for_the_next_United_Kingdom_"
                  "general_election&format=json")

# Constituency numbers (only including those contested in 2010)
NUM_OF_CONSTITUENCIES = 649
NEEDED_FOR_MAJORITY = int(math.ceil(NUM_OF_CONSTITUENCIES / 2)) 

# Tuning parameters for the model
RESULT_TOLERANCE = 0.03 # In percentage points divided by 100
SUPPORT_VARIATION = 0.005 # Also in percentage points
SWING_SCALE_FACTOR = 70.0 # Scale the amount of variance in vote numbers by this

# User agent to use when fetching historical poll data
USER_AGENT_STR = "Electobot PollScrape http://github.com/ZsigE/electobot"

# Results timeout.  Set this to None on very slow machines.
RESULTS_TIMEOUT = 10

# Logging
LOGS_DIR = "logs"
LOG_FILE = os.path.join(LOGS_DIR, "electobot.log")
LOG_LEVEL = logging.INFO