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
from candidate import Candidate
from constituency import Constituency

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
            if const not in self.constituencies:
                c = Constituency(const)
                self.constituencies[const] = c
            else:
                c = self.constituencies[const]
            c.region = row["Region"]
            candidates_2010 = row.candidates()
            c.votes_2005 = row.votes(2005)
            c.votes_2010 = row.votes(2010)
            c.turnout_2005 = float(row["Turn05"])
            c.turnout_2010 = float(row["Turn10"])

            # Copy the votes into the Candidate structures.
            c.candidates = []
            for party in c.votes_2010.keys():
                if party in candidates_2010.keys():
                    name = candidates_2010[party]
                else:
                    name = "Unknown"
                candidate = Candidate(name, party, c.votes_2010[party])
                c.candidates.append(candidate)
            

                
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
    