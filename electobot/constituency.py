#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Constituency data structure
"""

# Python imports
import logging
import random

# Electobot imports
import utils
from constants import *
    
# Set up logging
logger = logging.getLogger("electobot.constituency")    
    
class Constituency(object):
    """Represents an entire constituency."""
    
    def __init__(self, name, parent_election):
        """Constructor."""
        
        # Constant data
        self.name = name
        self.election = parent_election
        self.candidates_2010 = {}
        self.votes_2010 = {}
        self.votes_2005 = {}
        self.turnout_2005 = 0.0
        self.turnout_2010 = 0.0
        self.region = None
        
        # Data that we'll use in the simulation
        self.sim_votes = {}
        
        # Data that we'll get out of the simulation
        self.winning_party = None
        self.change = False
        
        return
    
    def predict_votes(self, predicted_support, use_regional=False):
        """Make a prediction of the vote distribution in this constituency."""
        
        logger.debug("Predicting votes in {0}".format(self.name))
        # First, calculate the support each party had in the 2005 and 2010
        # elections.
        support_2005 = utils.calculate_support(self.votes_2005)
        support_2010 = utils.calculate_support(self.votes_2010)
        
        # Calculate the swing matrix between those two elections.
        swing_05_10 = utils.calculate_swing(support_2005, support_2010)
        
        # Now compare the 2010 support to the new national support dictionary  
        # and calculate a swing matrix for that too.
        swing_matrix = utils.calculate_swing(support_2010, predicted_support)
          
        if use_regional:
            # Extract the swing between the 2010 results for this region and the
            # predicted results for this region.
            general_swing = self.election.regional_swing[self.region]
        else:
            # Extract the swing between the national 2010 results and the 
            # national prediction from the parent election.
            general_swing = self.election.swing_matrix
        
        # Calculate the total number of votes in this constituency in 2010.
        total_votes_2010 = sum(self.votes_2010.values())
        
        # Now we have to parcel those votes out.  Give each party the amount
        # they got last time, modified by the total national swing towards that
        # party.
        for party in swing_matrix.keys():
            vote_diff = int(sum(general_swing[party].values()) *
                            total_votes_2010)
            logger.debug("{0} vote changes by {1}".format(party, vote_diff))
            self.sim_votes[party] = self.votes_2010[party] + vote_diff
            if self.sim_votes[party] < 0:
                # Support dropped the number of votes below zero.  Fix that.
                logger.debug("{0} went below zero ({1})".
                                           format(party, self.sim_votes[party]))
                self.sim_votes[party] = 0
            
        # We now have the mean number of votes we expect each party to receive.
        # Use a normal distribution to select an actual number of votes, with
        # the variance of the distribution scaled to the amount of swing each
        # party generally experiences (as a swingier party is less predictable.)
        for party in swing_matrix.keys():
            mean_absolute_swing = ((sum([abs(swing) for swing in
                                        swing_matrix[party].values()]) +
                                    sum([abs(swing) for swing in
                                        swing_05_10[party].values()])) /
                                   (len(swing_05_10[party]) +
                                    len(swing_matrix[party])))
            
            # Normal distributions have about 95% of their values within 2
            # standard deviations from the mean.  Therefore, set the standard
            # deviation to be half the mean change in votes we expect from
            # the swing.
            stdev = 0.5 * self.sim_votes[party] * mean_absolute_swing
            
            # Apply a scaling factor for tuning.
            stdev = stdev * SWING_SCALE_FACTOR
            
            # Calculate the tweaked number of votes.
            self.sim_votes[party] = int(random.normalvariate(
                                                          self.sim_votes[party],
                                                          stdev))
            logger.debug("{0} votes in 2010: {1}. Predicted: {2}.".format(party,
                                                         self.votes_2010[party],
                                                         self.sim_votes[party]))

        return
    
    def simulate(self):
        """Simulate the result of the election in this constituency."""
        
        logger.debug("Simulate election in {0}".format(self.name))
        max_votes = 0
        
        for party in self.sim_votes:
            if self.sim_votes == max_votes:
                # Two parties have exactly the same vote.  This is highly
                # unusual, but is legally handled by drawing lots.  Simulate
                # that here.
                if random.randrange(2) == 0:
                    max_votes = self.sim_votes[party]
                    self.winning_party = party
            elif self.sim_votes[party] > max_votes:
                max_votes = self.sim_votes[party]
                self.winning_party = party
                
        logger.debug("Winner of {0} is {1} with {2} votes".
                                                      format(self.name,
                                                             self.winning_party,
                                                             max_votes))
                
        return
    
    