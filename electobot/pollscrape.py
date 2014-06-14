#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Poll data scraper
"""

# Python imports
import logging
import urllib2
import datetime
import json

# External imports
from bs4 import BeautifulSoup

# Electobot imports
import electobot.utils as utils
from electobot.constants import *
    
# Set up logging
logger = logging.getLogger("electobot.pollscrape")

# Classes
class PollScrape(object):
    """Web scraper to generate historical poll support data"""
    
    class Poll(object):
        """Historical poll data."""
        
        def __init__(self, 
                     datestr, 
                     pollster, 
                     sponsor, 
                     sample_size, 
                     con, lab, lib, ukip):
            """Constructor.  Store off data."""
            
            # Store off the easy stuff.
            self.pollster = pollster
            self.sponsor = sponsor
            self.sample_size = sample_size
            
            # Parse the date string into a date object for easy sorting.
            self.date = datetime.datetime.strptime(datestr, '%d %b %Y')
            
            # Store all the vote percentages as if they were votes from a total
            # turnout of 100.
            votes = {CON: con,
                     LAB: lab,
                     LD: lib,
                     UKP: ukip}
            votes[OTH] = 100 - sum(votes.values())
            
            # Now convert those into a support dictionary.
            self.support = utils.calculate_support(votes)
            
            # Initialize somewhere to store the MonteCarlo results of this poll.
            self.mc_results = None
            
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
        
        request = urllib2.Request(WIKI_POLLS_URL)
        request.add_header("user-Agent", USER_AGENT_STR)
        pollpage = urllib2.urlopen(request).read()
        json_page = json.loads(pollpage)
        tree = BeautifulSoup(json_page["parse"]["text"]["*"])
        
        tables = tree.find_all("table")
        
        # There's one table for every year in the polling records.  We only care
        # about the first two (2014 and 2013), but we want to join those values
        # together.  Take all the rows after the first (as that's the header).
        rows_2014 = tables[0].find_all("tr")[1:]
        rows_2013 = tables[1].find_all("tr")[1:]
        
        rows = {2014: rows_2014, 2013: rows_2013}
        
        return rows
        
    def create_polls_from_table(self):
        """Convert XML table into a series of Poll objects."""
        
        rows_dict = self.fetch_poll_xml()
        
        # Go through the rows, extracting the data from the cells and storing 
        # it in Poll structures.
        for year, rows in rows_dict.iteritems():
            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 8:
                    # Not all cells are present - skip this row.
                    continue
 
                # We only care about the last date when fieldwork was conducted.
                dates = cells[0].string
                if "-" in dates:
                    dates = dates.partition("-")[2]
                elif u"\u2013" in dates:
                    dates = dates.partition(u"\u2013")[2]
                
                datestr = "{0} {1}".format(dates, year).strip()
                label = cells[1].a.string
                pollster, slash, sponsor = label.partition("/")
                sample_size = int(cells[2].string.replace(",",""))
                con = int(cells[3].string.replace("%", ""))
                lab = int(cells[4].string.replace("%", ""))
                lib = int(cells[5].string.replace("%", ""))
                ukip = int(cells[6].string.replace("%", ""))
                
                poll = self.Poll(datestr,
                                 pollster, 
                                 sponsor,
                                 sample_size, 
                                 con, lab, lib, ukip)
                self.polls.append(poll)
            
        return
    
            
            
            
            
            
            
            
            
    