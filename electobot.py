#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Main module and data structures
"""

# Python imports
import optparse
import os
import cPickle as pickle

# Electobot imports
import csvparser
from constants import *
import candidate

# Constants


# Classes
class Election(object):
    """Master class containing all information about the election."""
    
    def __init__(self):
        """Constructor."""
        
        self.constituencies = {}
        self.parties = {}
        
        return
    
    def populate_from_csv(self, csv_filename):
        """Create an Election from saved election data in CSV format."""
        
        # Extract all the information from the CSV file.
        rows = csvparser.csv_to_dicts(csv_filename)
           
        for row in rows:
            const = row["Seat"]
            candidates = row.candidates()
            votes = row[5]
            # row[6] is vote %, so skip it
            incumbent = row[7]
            # Nothing interesting in the next few fields
            turnout = row[11]
            change = row[12]
            swing_lab_con = row[13]
            swing_con_ld = row[14]
            swing_lab_ld = row[15]
            swing_holder_winner = row[16]
            
            # All the data is now split out, so pack it into structures.
            if const not in self.constituencies:
                constituency = Constituency(const)
                self.constituencies[const] = constituency
            else:
                constituency = self.constituencies[const]
                
            is_incumbent = True if incumbent == "*" else False
            votes_num = int(votes.replace(",", ""))
            if party not in self.parties:
                party_obj = Party(party)
                self.parties[party] = party_obj
            else:
                party_obj = self.parties[party]
            cand_obj = Candidate(candidate,
                                 party_obj, 
                                 votes_num, 
                                 is_incumbent)
            constituency.race.candidates[candidate] = cand_obj
            
            constituency.race.turnout = float(turnout)
            constituency.race.change = change
            constituency.race.swing_lab_con = swing_lab_con
            constituency.race.swing_con_ld = swing_con_ld
            constituency.race.swing_lab_ld = swing_lab_ld
            constituency.race.swing_holder_winner = swing_holder_winner
                
        return    
                    
        
    
class Constituency(object):
    """Represents an entire constituency."""
    
    def __init__(self, name):
        """Constructor."""
        
        self.name = name
        self.race = Race()
        
        return

        
class Race(object):
    """Election within a single constituency."""

    def __init__(self):
        """Constructor."""
        
        self.candidates = {}
        self.turnout = 0
        self.change = None
        self.swing_lab_con = 0
        self.swing_con_ld = 0
        self.swing_lab_ld = 0
        self.swing_holder_winner = 0
        
        return


class Party(object):
    """Political party.  Used to classify Candidates."""
    
    def __init__(self, name):
        """Constructor.  Store just the name."""
        
        self.name = name
        
        return
    
    
# Functions
def electobot():
    """Main function."""

    # Parse the input arguments.
    parser = optparse.OptionParser()
    parser.add_option("--csv", "-c", help="CSV file containing election data",
                      action="store", dest="csv")
    parser.add_option("--pickle", "-p",
                      help="File containing pickled election data",
                      action="store",
                      dest="pickle")
    parser.add_option("--savefile", "-s", 
                      help="Filename for saving pickled election data",
                      action="store",
                      dest="savefile")
    opts, args = parser.parse_args()
    assert len(args) == 0, "ELECTOBOT ACCEPTS NO ARGUMENT"
    
    if opts.csv:
        # Populate the election from a CSV file.
        assert os.path.exists(opts.csv), "{0} does not exist".format(opts.csv)
        election = Election()
        election.populate_from_csv(opts.csv)
    elif opts.pickle:
        # Restore a saved election file from the pickled representation.
        assert os.path.exists(opts.pickle),                                    \
            "{0} does not exist".format(opts.pickle)
        with open(opts.pickle, "rb") as pickle_file:
            election = pickle.load(pickle_file)
        
    if opts.savefile:
        assert os.path.exists(opts.savefile),                                  \
            "{0} does not exist".format(opts.savefile)
        with open(opts.savefile, "wb") as save_file:
            pickle.dump(election, save_file, protocol=0)
            
    return
    
if __name__ == "__main__":
    electobot()    
    