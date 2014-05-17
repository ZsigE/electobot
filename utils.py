#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Utility functions
"""

# Python imports
import logging
    
# Set up logging
logger = logging.getLogger("electobot.utils")    

def calculate_support(votes):
    """Given a number of votes for each party, calculate the percentage support
    enjoyed by each party.
    """
    
    support = {}
    for party in votes.keys():
        support[party] = float(votes[party]) / sum(votes.values())
        
    return support

def calculate_swing(support_before, support_after):
    """Given levels of support for each party in before and after states, 
    generate a swing matrix.
    """
    
    # First work out the absolute swing - that is, whether support for each 
    # party has gone up or down.
    abs_swing = {}
    for party in support_before.keys():
        if party in support_after.keys():
            abs_swing[party] = support_after[party] - support_before[party]
        else:
            # No support level provided for this party - treat this as a zero
            # swing.
            abs_swing[party] = 0
            
    # Now fill in any new parties as if all their support swung into place.
    for party in (set(support_after.keys()) - set(support_before.keys())):
        abs_swing[party] = support_after[party]
        
    # Sort parties into those with positive and negative swings.  Zero swings
    # count as neither.
    positive_swings = {party:abs_swing[party] for party in abs_swing.keys() if 
                                                           abs_swing[party] > 0}
    negative_swings = {party:abs_swing[party] for party in abs_swing.keys() if 
                                                           abs_swing[party] < 0}
    zero_swings = {party:0 for party in abs_swing.keys() if 
                                                          abs_swing[party] == 0}
    
    # Calculate the relative support for each of the parties in the positive and
    # negative groups.
    positive_support = {}
    for party in positive_swings.keys():
        positive_support[party] = (positive_swings[party] /
                                   sum(positive_swings.values()))
    negative_support = {}
    for party in negative_swings.keys():
        negative_support[party] = (negative_swings[party] /
                                   sum(negative_swings.values()))
    
    # Create the swing matrix.  Basic rule is that parties with positive swing
    # must have taken that swing from parties with negative swing.  We don't
    # know how much came from each party, so take it proportional to each
    # party's support.
    #
    # (Technically, this is not true in the real world.  Any number of Labour
    # voters might switch to Conservative, and Labour's support could still rise
    # if they get their votes from other parties.  But it all looks the same to
    # the statistics, so screw it.)
    swing_matrix = {}
    for to_party in positive_swings.keys():
        swing = abs_swing[to_party]
        swing_matrix[to_party] = {}
        for from_party in negative_swings.keys():
            swing_matrix[to_party][from_party] = (swing * 
                                                  negative_support[from_party])
        for from_party in zero_swings.keys():
            swing_matrix[to_party][from_party] = 0
    
    # Parcel out negative swing as being "from" the positive-swing parties in 
    # the same way.
    for to_party in negative_swings.keys():
        swing = abs_swing[to_party]
        swing_matrix[to_party] = {}
        for from_party in positive_swings.keys():
            swing_matrix[to_party][from_party] = (swing * 
                                                  positive_support[from_party])
        for from_party in zero_swings.keys():
            swing_matrix[to_party][from_party] = 0            
    
    # Record that zero-swing parties haven't swung to or from anyone.
    for to_party in zero_swings.keys():
        swing_matrix[to_party] = {}
        for from_party in (abs_swing.keys()):
            swing_matrix[to_party][from_party] = 0
            
    return swing_matrix
        
        
            
            
            
        
    
    