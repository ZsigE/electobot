#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Monte Carlo simulation tools
"""

# Python imports
import logging
import copy
import random
import multiprocessing
from operator import itemgetter

# Electobot imports
from electobot.constants import *
import utils
    
# Set up logging
logger = logging.getLogger("electobot.montecarlo")

# Classes
class MonteCarlo(object):
    """Monte Carlo simulation of multiple elections."""
    
    def __init__(self, election, results_queue):
        """Constructor, also prepares election structure for simulation."""
        
        # Save off the results queue.
        self.results = results_queue
        
        # Create a copy of the election so that we don't modify the original.
        self.reference_election = copy.deepcopy(election)
        
        return
    
    def __call__(self):
        """Call straight through to the run method."""
        self.run()
    
    def get_modified_support(self):
        """Return a tweaked copy of the support dictionary."""
        
        predicted_support = copy.deepcopy(self.reference_election.
                                                              predicted_support)
        
        # Poll results are always given to within a margin of error.  That
        # means we can push each value up to SUPPORT_VARIATION percentage
        # points in either direction and still be faithful to the provided poll
        # numbers.
        for party in predicted_support.keys():
            modifier = random.uniform(-SUPPORT_VARIATION, SUPPORT_VARIATION)
            predicted_support[party] += modifier
            
        return predicted_support
    
    def run(self):
        """Run full Monte Carlo simulations until stopped."""
        
        while True:
            # Create a copy of the reference election to work with.
            this_election = copy.deepcopy(self.reference_election)
        
            # Tweak the poll numbers a bit to give us some variety.
            this_election.predicted_support = self.get_modified_support()
        
            # Now run this election and store its Result.  We copy it so that
            # the election itself can be immediately GCed.
            this_election.run()
            self.results.put(copy.deepcopy(this_election.result))
            
        return

class MonteCarloResult(object):
    """Object to hold results from a set of elections run as a Monte Carlo
    simulation.
    """
    
    def __init__(self):
        """Initialize variables."""
        
        # Things we want to know about the final dataset.
        self.num_of_results = 0
        self.win_counts = {}
        self.seats = {}
        self.mean_seats = {}
        self.stddev_seats = {}
        self.largest_party_counts = {}
        self.mean_margin_of_victory = 0
        self.most_seats_won = 0
        self.most_seats_won_party = None
        self.greens_hold_brighton_count = 0
        self.seat_winner_is_pop_winner_count = 0
        self.margins_of_victory = []
        
        return
    
    def analyze(self, results):
        """Analyze the results."""
        
        for result in results:
            self.num_of_results += 1
            if result.winner in self.win_counts:
                self.win_counts[result.winner] += 1
            else:
                self.win_counts[result.winner] = 1
            
            for party in result.seats.keys():
                if party in self.seats.keys():
                    self.seats[party].append(result.seats[party])
                else:
                    self.seats[party] = [result.seats[party]]
                
            if result.largest_party in self.largest_party_counts:
                self.largest_party_counts[result.largest_party] += 1
            else:
                self.largest_party_counts[result.largest_party] = 1
                
            self.margins_of_victory.append(result.margin_of_victory)
            
            if result.most_seats_won > self.most_seats_won:
                self.most_seats_won = result.most_seats_won
                self.most_seats_won_party = result.largest_party
                
            if result.greens_hold_brighton:
                self.greens_hold_brighton_count += 1
                
            if result.seat_winner_is_pop_winner:
                self.seat_winner_is_pop_winner_count += 1
                
        # Calculate the mean and standard deviation of the number of seats for
        # each party.
        for party in self.seats.keys():
            self.mean_seats[party] = (sum(self.seats[party]) / 
                                      len(self.seats[party]))
            self.stddev_seats[party] = utils.std_dev(self.seats[party])
            
        return
    
    def report(self):
        """Report overall results."""
        
        # Get the mean and standard deviation of the margin of victory.
        mean_margin_of_victory = (sum(self.margins_of_victory) /
                                  float(self.num_of_results))
        margin_stddev = utils.std_dev(self.margins_of_victory)
        
        # Report the results from this analysis.
        print "Winning percentages:"
        for party in sorted(self.win_counts.iteritems(),
                            key=itemgetter(1), 
                            reverse=True):
            if party[0] is None:
                party_name = "[Hung Parliament]"
            else:
                party_name = party[0]
            print "  {0}: {1}%".format(party_name,
                                get_result_percentage(self.win_counts[party[0]],
                                                      self.num_of_results))
        
        print "Largest-party percentages:"
        for party in sorted(self.largest_party_counts.keys()):
            print "  {0}: {1}%".format(party,
                                       get_result_percentage(
                                               self.largest_party_counts[party],
                                               self.num_of_results))
            
        print "Mean number of seats per-party (95% confidence intervals):"
        for party in sorted(self.mean_seats.keys(), 
                            key=self.mean_seats.get,
                            reverse=True):
            print "  {0}: {1} ({2:.2f}-{3:.2f})".format(
                                               party,
                                               self.mean_seats[party],
                                               (self.mean_seats[party] -
                                                (2 * self.stddev_seats[party])),
                                               (self.mean_seats[party] + 
                                                (2 * self.stddev_seats[party])))
            
        print ("Mean margin of victory: {0} (95% between {1:.2f} and"
               " {2:.2f})".format(
                                mean_margin_of_victory,
                                (mean_margin_of_victory - (2 * margin_stddev)),
                                (mean_margin_of_victory + (2 * margin_stddev))))

        print ("Greens hold Brighton Pavilion in "
               "{0}% of runs".format(get_result_percentage(
                                                self.greens_hold_brighton_count,
                                                self.num_of_results)))
        
        return

def make_and_run_montecarlo(election, results_queue):
    """Run a single election for the Monte Carlo simulation."""
    
    # This function is at the top level of the module rather than part of the
    # MonteCarlo class because Python's multiprocessing module, in its ineffable
    # wisdom, won't let you use a class method as the function you pass to the
    # threads.  I don't get it either.
    mc = MonteCarlo(election, results_queue)
    mc.run()
    
    return

def get_result_percentage(result, total_results):
    """Return the result as a percentage of all results."""
    
    return (float(result) / total_results) * 100

def run_multithreaded_montecarlo(election, iterations):
    """Run a Monte Carlo simulation using multiple threads to save time."""
    
    # Create a queue to hold the results.
    results_queue = multiprocessing.Queue()
    
    # Create and start some processes ready to run the simulation.
    processes = []
    try:
        for ii in range(multiprocessing.cpu_count()):
            mc = MonteCarlo(election, results_queue)
            proc = multiprocessing.Process(target=mc)
            processes.append(proc)
            proc.start()
        
        # Monitor the results queue so we can see them coming in.
        results = []
        too_divergent = 0
        while len(results) < iterations:
            logger.info("Results so far: {0} of {1}".format(len(results),
                                                            iterations))
            res = results_queue.get(block=True, timeout=RESULTS_TIMEOUT)
            if not res.result_too_divergent:
                results.append(res)
            else:
                logger.debug("Too divergent.")
                logger.debug(str(res.support))
                too_divergent += 1
        logger.info("{0} results discarded for unacceptable "
                    "divergence".format(too_divergent))
    finally: 
        # Make sure we kill all the processes if we're interrupted.   
        for proc in processes:
            proc.terminate()
    
    # All results are in, so now we can analyze them.
    mcresult = MonteCarloResult()
    mcresult.analyze(results)
    
    return mcresult