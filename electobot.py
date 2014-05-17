#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Main module and data structures
"""

# Python imports
import argparse
import os
import cPickle as pickle
import logging

# Electobot imports
import csvparser
import utils
from constants import *
from candidate import Candidate
from constituency import Constituency

# Set up logging
logger = logging.getLogger("electobot")

# Classes
class Election(object):
    """Master class containing all information about the election."""
    
    def __init__(self):
        """Constructor."""
        
        # Data used to run the election
        self.constituencies = {}
        self.predicted_support = {}
        
        # Data generated by running the election
        self.parties = {}
        
        # Data generated by analyzing the results
        self.result = ""
        self.largest_party = None
        self.most_seats = 0
        
        return
    
    def populate_from_csv(self, csv_filename):
        """Create an Election from saved election data in CSV format."""
        
        # Extract all the information from the CSV file.
        rows = csvparser.csv_to_dicts(csv_filename)
        logger.debug("Found {0} rows".format(len(rows)))
           
        for row in rows:
            const = row["Seat"]
            logger.debug("Found seat {0}".format(const))
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
            c.candidates_2010 = []
            for party in c.votes_2010.keys():
                if party in candidates_2010.keys():
                    name = candidates_2010[party]
                else:
                    name = "Unknown"
                candidate = Candidate(name, party, c.votes_2010[party])
                c.candidates_2010.append(candidate)
                            
        return
    
    def predict_votes(self):
        """Predict the numbers of votes in each constituency."""
        
        for const_name in self.constituencies:
            const = self.constituencies[const_name]
            const.predict_votes(self.predicted_support)
            
        return
    
    def simulate(self):
        """Simulate the outcome of this election."""
        
        for const_name in self.constituencies:
            const = self.constituencies[const_name]
            const.simulate()
            if const.winning_party in self.parties.keys():          
                self.parties[const.winning_party].seats += 1
            else:
                party = Party(const.winning_party)
                party.seats = 1
                self.parties[const.winning_party] = party
        
        return
    
    def analyze(self):
        """Analyze the results of the election."""
        
        # First determine the largest party.
        self.most_seats = 0
        self.largest_party = None
        for party in self.parties:
            if self.parties[party].seats > self.most_seats:
                self.most_seats = self.parties[party].seats
                self.largest_party = party
                
        # Now determine whether they're past or behind the winning line (and
        # by how much).
        margin_of_victory = self.most_seats - NEEDED_FOR_MAJORITY
        if margin_of_victory >= 0:
            self.result = "{0} victory (majority {1})".format(
                                                             self.largest_party,
                                                             margin_of_victory)
        else:
            self.result = "Hung Parliament ({0} needs {1})".format(
                                                          self.largest_party,
                                                          (0-margin_of_victory))
        
        return

class Party(object):
    """Political party.  Used to classify Candidates."""
    
    def __init__(self, name):
        """Constructor.  Store just the name."""
        
        self.name = name
        self.seats = 0
        
        return
    
    
# Functions
def electobot():
    """Main function."""

    # Set up logging.
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')
    handler = logging.FileHandler(LOG_FILE, mode="w")
    handler.setFormatter(formatter)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(handler)
     
    # Parse the input arguments.
    parser = argparse.ArgumentParser()
    fileopts = parser.add_argument_group("File options")
    fileopts.add_argument("--csv", "-c",
                         help="CSV file containing election data",
                         action="store", dest="csv")
    fileopts.add_argument("--pickle", "-p",
                          help="File containing pickled election data",
                          action="store",
                          dest="pickle")
    fileopts.add_argument("--savefile", "-s", 
                          help="Filename for saving pickled election data",
                          action="store",
                          dest="savefile")
    
    simopts = parser.add_argument_group("Simulation options")
    simopts.add_argument("--single-election", "-1",
                         help="Simulate a single election",
                         action="store_true",
                         dest="single_election")
    
    partyopts = parser.add_argument_group("Party support options")
    partyopts.add_argument("--conservative", "-t",
                           help="Predicted percentage of Conservative support",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="conservative")
    partyopts.add_argument("--labour", "-l",
                           help="Predicted percentage of Labour support",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="labour")
    partyopts.add_argument("--libdem", "-d",
                           help="Predicted percentage of Lib-Dem support",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="libdem")
    partyopts.add_argument("--green", "-g",
                           help="Predicted percentage of Green support",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="green")
    partyopts.add_argument("--ukip", "-u",
                           help="Predicted percentage of UKIP support",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="ukip")
    partyopts.add_argument("--snp", "-n",
                           help="Predicted percentage of SNP support",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="snp")
    partyopts.add_argument("--plaid-cymru", "-w",
                           help="Predicted percentage of Plaid Cymru support",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="plaid")
    partyopts.add_argument("--bnp", "-z",
                           help="Predicted percentage of BNP support",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="bnp")

    opts = parser.parse_args()
    
    election = None
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
    
    # Fill in the support for each party from the command-line arguments.
    election.predicted_support = {
                                  CON: opts.conservative,
                                  LAB: opts.labour,
                                  LD: opts.libdem,
                                  SNP: opts.snp,
                                  PC: opts.plaid,
                                  GRN: opts.green,
                                  BNP: opts.bnp,
                                  UKP: opts.ukip,
                                 }
    
    # If a party has no support recorded, remove them entirely - we'll treat
    # them as part of the "Other" pot.
    for party in election.predicted_support.keys():
        if election.predicted_support[party] == 0:
            del election.predicted_support[party]
        else:
            # Express the support as a ratio, not a percentage - this makes the
            # maths much easier.
            election.predicted_support[party] = \
                                       (election.predicted_support[party] / 100)
    
    # Fill in "Other" support automatically, to guarantee the support adds up
    # to 100.
    election.predicted_support[OTH] = (1 - 
                                       sum(election.predicted_support.values())) 
            
    if opts.single_election:
        assert election is not None, "No election data to work with"
        election.predict_votes()
        election.simulate()
        election.analyze()
        print election.result
            
    return
    
if __name__ == "__main__":
    electobot()    
    