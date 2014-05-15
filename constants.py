#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Constants for use by all modules
"""

import math
import logging

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

# Constituency numbers (only including those contested in 2010)
NUM_OF_CONSTITUENCIES = 649
NEEDED_FOR_MAJORITY = int(math.ceil(NUM_OF_CONSTITUENCIES / 2)) 

# Logging
LOG_FILE = "electobot.log"
LOG_LEVEL = logging.DEBUG