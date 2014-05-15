#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Constituency data structure
"""
    
class Constituency(object):
    """Represents an entire constituency."""
    
    def __init__(self, name):
        """Constructor."""
        
        self.name = name
        self.candidates = {}
        self.change = None
        self.region = None
        
        return