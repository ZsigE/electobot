#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Constituency data structure
"""

import logging
import random
    
# Set up logging
logger = logging.getLogger("electobot.constituency")    
    
class Constituency(object):
    """Represents an entire constituency."""
    
    def __init__(self, name):
        """Constructor."""
        
        # Constant data
        self.name = name
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
    
    def predict_votes(self):
        """Make a prediction of the vote distribution in this constituency."""
        
        # For now, copy the votes from 2010.
        self.sim_votes = self.votes_2010
        
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
    
    