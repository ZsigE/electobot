#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Poll data scraper
"""

# Python imports
import logging
import urllib
from xml.etree import ElementTree
import datetime

# Electobot imports
import utils
from constants import *
    
# Set up logging
logger = logging.getLogger("electobot.pollscrape")

# Classes
class PollScrape(object):
    """Web scraper to generate historical poll support data"""
    
    class Poll(object):
        """Historical poll data."""
        
        def __init__(self, datestr, pollster, sponsor, con, lab, lib, ukip):
            """Constructor.  Store off data."""
            
            # Store off the easy stuff.
            self.pollster = pollster
            self.sponsor = sponsor
            
            # Parse the date string into a date object for easy sorting.
            self.date = datetime.datetime.strptime(datestr, '%Y-%m-%d')
            
            # Store all the vote percentages as if they were votes from a total
            # turnout of 100.
            votes = {CON: con,
                     LAB: lab,
                     LD: lib,
                     UKP: ukip}
            votes[OTH] = 100 - sum(votes.values())
            
            # Now convert those into a support dictionary.
            self.support = utils.calculate_support(votes)
            
            return
        
        def __eq__(self, other):
            """Equality operator."""
            
            return (self.pollster == other.pollster and
                    self.sponsor == other.sponsor and
                    self.date == other.date and
                    self.support == other.support)
        
    def __init__(self):
        """Constructor.  Initialise data structure."""
        
        self.polls = []
        
        return
    
    def fetch_poll_xml(self):
        """Get the UK Polling Report historical poll page and parse it to
        extract the historical polling data table in XML."""
        
        with urllib.urlopen(UKPR_POLL_URL) as pollpage:
        
            tree = ElementTree.parse(pollpage)
            
            table_div = tree.find(".//div[class='polltable']")
            table = table_div.find("table")
        
        return table
        
    def create_polls_from_table(self):
        """Convert XML table into a series of Poll objects."""
        
        table = self.fetch_poll_xml()
        rows_iter = table.iterfind(".//tr")
        
        # Discard the first two rows from the iterator, as these are just the
        # header row.
        rows_iter.next()
        rows_iter.next()
        
        # Now go through the remaining rows, extracting the data and storing it
        # in Poll structures.
        for row in rows_iter:
            cells = list(row.iter("td"))
            label = cells[0].findtext(".")
            pollster, slash, sponsor = label.partition("/")
            datestr = cells[1].findtext(".")
            con = int(cells[2].findtext("."))
            lab = int(cells[3].findtext("."))
            lib = int(cells[4].findtext("."))
            ukip = int(cells[5].findtext("."))
            
            poll = self.Poll(datestr, pollster, sponsor, con, lab, lib, ukip)
            self.polls.append(poll)
            
        return
    
            
            
            
            
            
            
            
            
    