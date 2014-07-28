#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Data visualisation tools
"""

# Python imports
from operator import itemgetter
import os

# Third-party imports
import matplotlib.pyplot as plt
import numpy as np

# Electobot imports
import electobot.pollscrape as pollscrape
from electobot.constants import *

def create_pie_chart(results, filepath):
    """Generate a pie chart based on the results for a single election, and
    save it in the requested location.  Note that 'name' should not include the
    filetype suffix."""
    
    # Convert the results dictionary into arrays for matplotlib.
    items = sorted(results.iteritems(), key=itemgetter(1), reverse=True)
    partynames = [item[0] for item in items]
    numofseats = [item[1] for item in items]
    colours = [PARTY_COLOURS[party] for party in partynames]
    
    # Generate the chart.
    plt.figure(figsize=(8, 8))
    ptch, txts =  plt.pie(numofseats, 
                          labels=partynames, 
                          colors=colours)
    for txt in txts:
        txt.set_size("small")
    
    # Save it off!
    filename = "{0}.png".format(filepath)
    plt.savefig(filename)
    
    return
    