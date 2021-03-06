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
    save it in the requested location.  Note that 'filepath' should not include 
    the filetype suffix."""
    
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

def create_line_range_chart(savedpolls, 
                            filepath, 
                            pollsters=None, 
                            sponsors=None,
                            min_sample_size=None, 
                            start_date=None, 
                            end_date=None):
    """Generate a line chart from a series of pollscrape Polls, with dates along
    the x-axis, and one line per party.  Also error bars for each result's 95%
    confidence intervals."""
    
    # Order the results by date.
    polls = sorted(savedpolls, key=attrgetter("date"))
    logger.info("Found {0} results, first from {1}, last from {2}".
                format(len(polls), polls[0].date, polls[-1].date))
    
    # Select the polls we want based on the various filter critera specified.
    # Assume that the poll is going to be included unless filtered out.
    polls_to_chart = []
    for poll in polls:
        if pollsters is not None and poll.pollster not in pollsters:
            logger.debug("Poll filtered out on pollster ({0})".
                         format(poll.pollster))
            continue
        elif sponsors is not None and poll.sponsor not in sponsors:
            logger.debug("Poll filtered out on sponsor ({0})".
                         format(poll.sponsor))
            continue
        elif min_sample_size is not None and poll.sample_size < min_sample_size:
            logger.debug("Poll filtered out on sample size ({0})".
                         format(poll.sample_size))
            continue
        elif start_date is not None and poll.date < start_date:
            logger.debug("Poll filtered out by start date ({0})".
                         format(poll.date))
            continue
        elif end_date is not None and poll.date > end_date:
            logger.debug("Poll filtered out by end date ({0})".
                         format(poll.date))
            continue
        else:
            polls_to_chart.append(poll)
    
    # Generate the various arrays that we'll need to plot these results.
    dates = [poll.date for poll in polls_to_chart]
    party_mean_seats = {}
    party_seat_error = {}
    for party in PARTY_NAMES:
        party_mean_seats[party] = []
        party_seat_error[party] = []
    for poll in polls_to_chart:
        for party in PARTY_NAMES:
            party_mean_seats[party].append(poll.result.mean_seats[party])
            
            # Error bars will be at +-2*standard deviation, as this gives us 95%
            # confidence intervals.
            party_seat_error[party].append(2 * poll.result.stddev_seats[party])
            
    # Create axes on which to put this information.
    axes = plt.subplot(1, 1, 1)
    
    # Generate points with error bars for all parties.  Suppress the line, as
    # this is misleading or multiple polls from the same day, but add markers 
    # instead.
    for party in PARTY_NAMES:
        logger.debug("Adding line for {0}".format(party))
        logger.debug("  Line colour: {0}".format(PARTY_COLOURS[party]))
        axes.errorbar(dates, 
                      party_mean_seats[party],
                      yerr=party_seat_error[party],
                      color=PARTY_COLOURS[party],
                      linestyle="None",
                      marker=".",
                      label=party)
     
    # Tweak the axis limits to ensure the y-axis starts at 0 and there's a gap
    # after the last results (scaled down for fewer results).
    limits = list(plt.axis())
    limits[1] += min(10, len(polls)/300.0)
    limits[2] = 0
    plt.axis(limits)
    
    # Rotate the x-axis labels to stop them clashing.
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45) 
    
    # Add a horizontal line at the winning mark.
    plt.axhline(NEEDED_FOR_MAJORITY, color="black", linewidth=1)
    
    # Add a legend.
    plt.legend(loc="upper center", 
               ncol=3,
               numpoints=1, 
               bbox_to_anchor=(0.5, 1.16))
    
    # Increase the size of the figure to accommodate these elements.
    fig = plt.gcf()
    fig.set_size_inches(10, 8)
    fig.subplots_adjust(bottom=0.15, top=0.85)
    
    # Add a credit line (remove this if you're forking the code, obviously)
    fig.text(0.99, 0.01, 
             "Generated by Electobot (http://github.com/ZsigE/electobot)",
             size="small", color="Black", ha="right")
            
    # Save off the chart.
    filename = "{0}.png".format(filepath)
    plt.savefig(filename)
    
    return 
    
def create_poll_summary_barchart(mc_results, filepath):
    """Generate a bar chart with error bars to summarise the results of a
    Monte Carlo simulation.  Note that 'filepath' should not include the
    filetype suffix."""    
    
    # Convert the MonteCarlo results into Matplotlib arrays.
    x_indices = range(len(mc_results.mean_seats))
    parties_seats = sorted(mc_results.mean_seats.items(), 
                           key=itemgetter(1), 
                           reverse=True)
    parties = [item[0] for item in parties_seats]
    seat_nums = [item[1] for item in parties_seats]
    errors = [2 * mc_results.stddev_seats[party] for party in parties]
    colours = [PARTY_COLOURS[party] for party in parties]
    
    # Create some axes and plot the data.
    axes = plt.subplot(1, 1, 1)
    axes.bar(x_indices, seat_nums, color=colours, yerr=errors, width=1, 
             ecolor="Black")
    
    # Add a horizontal line at the winning mark.
    plt.axhline(NEEDED_FOR_MAJORITY, color="black", linewidth=1)
    
    # Tweak the axes - the y-axis starts at 0, and the x-axis labels are the
    # party names.
    plt.ylim(ymin=0)
    plt.xticks([num + 0.5 for num in x_indices], parties, size="x-small")
    plt.tick_params(bottom="off")
    
    # Add a credit line (remove this if you're forking the code, obviously)
    fig = plt.gcf()
    fig.text(0.99, 0.01, 
             "Generated by Electobot (http://github.com/ZsigE/electobot)",
             size="small", color="Black", ha="right")
    
    # Save off the chart.
    filename = "{0}.png".format(filepath)
    plt.savefig(filename)

    return
    