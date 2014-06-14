#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

CSV parser
"""

# Python imports
import csv
import logging

# Electobot imports
from electobot.constants import *

# Set up logging
logger = logging.getLogger("electobot.csvparser")

# Classes
class DataRow(dict):
    """Single row of data from the election results."""
    
    cand_cells = {CON: "ConPPC",
                  LAB: "LabPPC", 
                  LD:  "LDPPC", 
                  SNP: "SNPPPC10", 
                  PC:  "PCPPC10", 
                  GRN: "GreenPPC10",
                  BNP: "BNPPPC10",
                  UKP: "UKIPPPC10"}
    
    votes_2010_cells = {CON: "Convt10",
                        LAB: "Labvt10",
                        LD:  "LDvt10",
                        SNP: "SNPvt10",
                        PC:  "PCvt10",
                        GRN: "Greenvt10",
                        BNP: "BNPvt10",
                        UKP: "UKIPvt10"}
    
    votes_2005_cells = {CON: "Convt05",
                        LAB: "Labvt05",
                        LD:  "LDvt05",
                        SNP: "SNPvt05",
                        PC:  "PCvt05",
                        GRN: "Grnvt05",
                        BNP: "BNPvt05",
                        UKP: "UKIPvt05"}
    
    def __getitem__(self, key):
        """Override to return None rather than an empty string."""
        
        if not dict.__contains__(self, key):
            return None
        val = dict.__getitem__(self, key)
        return val if val != "" else None
        
    def get_candidate(self, party):
        """Fetch the name of the candidate for the given party."""
        
        return self[self.cand_cells[party]]
    
    def candidates(self):
        """List all the candidates who stood in 2010 in this constituency."""
        
        candidates = {}
        for party in self.cand_cells.keys():
            cand = self.get_candidate(party)
            if cand is not None:
                candidates[party] = cand
                
        return candidates
    
    def votes(self, year):
        """Return the number of votes gained by each party in the given year."""
        
        votes = {}
        if year == 2005:
            cell_key = self.votes_2005_cells
            total_votes = int(self["Totvt05"].replace(",",""))
        elif year == 2010:
            # Unaccountably, there is no total vote count for 2010, so we need
            # to work it out from the turnout and electorate fields.
            cell_key = self.votes_2010_cells
            electorate = int(self["Elec10"].replace(",",""))
            turnout = float(self["Turn10"])
            total_votes = int(turnout * electorate / 100)
        else:
            assert False, "Invalid year requested for votes: {0}".format(year)
            
        for party in cell_key.keys():
            numvotes = self[cell_key[party]]
            if numvotes is not None:
                numvotes = int(numvotes.replace(",",""))
            else:
                numvotes = 0
            
            logging.debug("{0}: {1} got {2} votes".format(self["Seat"],
                                                          party,
                                                          numvotes))
            votes[party] = numvotes
        
        # Calculate the number of votes for unlisted parties.
        logger.debug("Total votes: {0}".format(total_votes))  
        votes[OTH] = total_votes - sum(votes.values())
            
        return votes
    
# Utility functions
def csv_to_dicts(filename, harvard=True):
    """Function to convert a CSV file into a list of DataRows, each holding
    one row of the CSV table.
    """
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        
        # The first row is the headers - save off their names, minus
        # surrounding whitespace.
        headers = [hdr.strip() for hdr in reader.next()]
        logger.debug("Found {0} headers".format(len(headers)))
        
        # All subsequent rows are the entries in this table - save them off
        # under their appropriate headers.
        rows = []
        for row in reader:
            row_dict = DataRow()
            for ii in range(len(row)):
                row_dict[headers[ii]] = row[ii]
            
            # If we're assuming that this is the Harvard election data file,
            # include only constituencies that were contested in 2010.
            if (row_dict["Win10"] is not None) or (not harvard):
                rows.append(row_dict)   
            
    return rows

def get_total_votes_from_guardian():
    """Open the Guardian CSV file and get the total votes for each constituency.
    """
    
    rows = csv_to_dicts(GUARDIAN_CSV, harvard=False)
    
    constituencies = {}
    for row in rows:
        if row["Seat"] in constituencies:
            constituencies[row["Seat"]] += int(row["Vote"].replace(",",""))
        else:
            constituencies[row["Seat"]] = int(row["Vote"].replace(",",""))
            
    return constituencies
        
        
    
    
    
    
    