#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Candidate data structure
"""

class Candidate(object):
    """Candidate for a seat."""
    
    def __init__(self, name, party, votes):
        """Constructor.  Store relevant information."""
        
        self.name = name
        self.party = party
        self.votes_2010 = votes
        self.incumbent = None
        
        return