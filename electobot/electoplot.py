#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Data visualisation tools
"""

# Python imports
from operator import itemgetter, attrgetter
import os
import logging

# Third-party imports
import matplotlib.pyplot as plt
import numpy as np

# Electobot imports
import electobot.pollscrape as pollscrape
from electobot.constants import *

# Set up logging
logger = logging.getLogger("electobot.electoplot")

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
    ptch, txts = plt.pie(numofseats, 
                         labels=partynames, 
                         colors=colours)
    for txt in txts:
        txt.set_size("small")
    
    # Save it off!
    filename = "{0}.png".format(filepath)
    plt.savefig(filename)
    
    return

def create_line_range_chart(savedpolls, filepath):
    """Generate a line chart from a series of pollscrape Polls, with dates along
    the x-axis, and one line per party.  Also error bars for each result's 95%
    confidence intervals."""
    
    # Order the results by date.
    polls = sorted(savedpolls, key=attrgetter("date"))
    logger.info("Found {0} results, first from {1}, last from {2}".
                format(len(polls), polls[0].date, polls[-1].date))
    
    # Generate the various arrays that we'll need to plot these results.
    dates = [poll.date for poll in polls]
    party_mean_seats = {}
    party_seat_error = {}
    for party in PARTY_NAMES:
        party_mean_seats[party] = []
        party_seat_error[party] = []
    for poll in polls:
        for party in PARTY_NAMES:
            party_mean_seats[party].append(poll.result.mean_seats[party])
            
            # Error bars will be at +-2*standard deviation, as this gives us 95%
            # confidence intervals.
            party_seat_error[party].append(2 * poll.result.stddev_seats[party])
            
    # Create axes on which to put this information.
    axes = plt.subplot(1, 1, 1)
    
    # Generate lines with error bars for all parties.
    for party in PARTY_NAMES:
        axes.errorbar(dates, 
                      party_mean_seats[party],
                      yerr=party_seat_error[party],
                      mfc=PARTY_COLOURS[party],
                      mec=PARTY_COLOURS[party])
    
    # Save off the chart.
    filename = "{0}.png".format(filepath)
    plt.savefig(filename)
    
    return 
    
    
    
    
    