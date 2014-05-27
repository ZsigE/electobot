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
import time

# Electobot imports
from constants import *
    
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
        """Run a full Monte Carlo simulation for the given number of iterations.
        """
        
        # Create a copy of the reference election to work with.
        this_election = copy.deepcopy(self.reference_election)
        
        # Tweak the poll numbers a bit to give us some variety.
        this_election.predicted_support = self.get_modified_support()
        
        # Now run this election and store its Result.  We copy it so that
        # the election itself can be immediately GCed.
        this_election.run()
        self.results.put(copy.deepcopy(this_election.result))
            
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

def get_result_percentage(self, result, total_results):
    """Return the result as a percentage of all results."""
    
    return (float(result) / len(self.results)) * 100
        
def analyze_montecarlo_results(results_queue):
    """Analyze the overall results."""
    
    # Things we want to know about the final dataset.
    num_of_results = 0
    win_counts = {}
    largest_party_counts = {}
    runnerup_counts = {}
    third_place_counts = {}
    mean_margin_of_victory = 0
    most_seats_won = 0
    most_seats_won_party = None
    ukip_get_seats_count = 0
    libdem_wipeout_count = 0
    greens_hold_brighton_count = 0
    seat_winner_is_pop_winner_count = 0
    
    margins_of_victory = []
    while not results_queue.empty():
        result = results_queue.get()
        num_of_results += 1
        if result.winner in win_counts:
            win_counts[result.winner] += 1
        else:
            win_counts[result.winner] = 1
            
        if result.largest_party in largest_party_counts:
            largest_party_counts[result.largest_party] += 1
        else:
            largest_party_counts[result.largest_party] = 1
            
        if result.runner_up in runnerup_counts:
            runnerup_counts[result.runner_up] += 1
        else:
            runnerup_counts[result.runner_up] = 1
            
        if result.third_place in third_place_counts:
            third_place_counts[result.third_place] += 1
        else:
            third_place_counts[result.third_place] = 1
            
        margins_of_victory.append(result.margin_of_victory)
        
        if result.most_seats_won > most_seats_won:
            most_seats_won = result.most_seats_won
            most_seats_won_party = result.largest_party
            
        if result.ukip_seats > 0:
            ukip_get_seats_count += 1
            
        if result.libdem_seats == 0:
            libdem_wipeout_count += 1
            
        if result.greens_hold_brighton:
            greens_hold_brighton_count += 1
            
        if result.seat_winner_is_pop_winner:
            seat_winner_is_pop_winner_count += 1
            
    mean_margin_of_victory = (sum(margins_of_victory) /
                              num_of_results)
    
    # Report the results from this analysis.
    print "Largest-party percentages:"
    for party in sorted(largest_party_counts.keys()):
        print "  {0}: {1}".format(party,
                                  get_result_percentage(
                                                    largest_party_counts[party],
                                                    num_of_results))
        
    print "Runner-up percentages:"
    for party in sorted(runnerup_counts.keys()):
        print "  {0}: {1}".format(party,
                                  get_result_percentage(runnerup_counts[party],
                                                        num_of_results))
    
    return

def run_multithreaded_montecarlo(election, iterations):
    """Run a Monte Carlo simulation using multiple threads to save time."""
    
    # Create some processes ready to run the simulation.
    pool_manager = multiprocessing.Manager()
    proc_pool = pool_manager.Pool()
    
    # Create a queue to hold the results.
    results_queue = pool_manager.Queue()
    
    # Kick off the required number of iterations.
    for ii in range(iterations):
        proc_pool.apply_async(make_and_run_montecarlo,
                              (election, results_queue))
        
    proc_pool.close()
    
    # Monitor the results queue so we can see them coming in.
    while results_queue.qsize() < iterations:
        logger.info("Results so far: {0} of {1}".format(results_queue.qsize(),
                                                        iterations))
        time.sleep(0.5)
        
    proc_pool.join()
    
    # All results are in, so now we can analyze them.
    analyze_montecarlo_results(results_queue)
    
    return