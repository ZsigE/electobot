#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

CSV parser
"""

# Python imports
import csv

# Electobot imports
from constants import *

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
        
        val = dict.__getitem__(self, key)
        return val if val != "" else None
        
    def get_candidate(self, party):
        """Fetch the name of the candidate for the given party."""
        
        return self[self.cand_cells[party]]
    
    def candidates(self):
        """List all the candidates who stood in this constituency."""
        
        candidates = {}
        for party in self.cand_cells.keys():
            cand = self.get_candidate(party)
            if cand is not None:
                candidates[party] = cand
                
        return candidates
    

def csv_to_dicts(filename):
    """Function to convert a CSV file into a list of DataRows, each holding
    one row of the CSV table.
    """
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        # The first row is the headers - save off their names.
        headers = csvfile.next()
        
        # All subsequent rows are the entries in this table - save them off
        # under their appropriate headers.
        rows = []
        for row in reader:
            row_dict = DataRow()
            for ii in range(len(row)):
                row_dict[headers[ii]] = row[ii]
            rows.append(row_dict)
            
    return rows
    