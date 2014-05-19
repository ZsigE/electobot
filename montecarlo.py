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
    
# Set up logging
logger = logging.getLogger("electobot.montecarlo")

# Classes
class MonteCarlo(object):
    """Monte Carlo simulation of multiple elections."""
    
    def __init__(self, election):
        """Constructor, also prepares election structure for simulation."""
        
        # Create a copy of the election so that we don't modify the original.
        self.reference_election = copy.deepcopy(election)
        
        # Results for later analysis.
        self.results = []
        
        # Things we want to know about the final dataset.
        self.win_counts = {}
        self.largest_party_counts = {}
        self.runnerup_counts = {}
        self.third_place_counts = {}
        self.mean_margin_of_victory = 0
        self.most_seats_won = 0
        self.most_seats_won_party = None
        self.ukip_get_seats_count = 0
        self.libdem_wipeout_count = 0
        self.greens_hold_brighton_count = 0
        self.seat_winner_is_pop_winner_count = 0
        
        return
    
    def get_modified_support(self):
        """Return a tweaked copy of the support dictionary."""
        
        predicted_support = copy.deepcopy(self.reference_election.
                                                              predicted_support)
        
        # Poll results are always given to the nearest percentage point.  That
        # means we can push each value up to half a percentage point in either
        # direction and still be faithful to the provided poll numbers.
        for party in predicted_support.keys():
            modifier = random.uniform(-0.5, 0.5)
            predicted_support[party] += modifier
            
        return predicted_support
    
    def get_result_percentage(self, result):
        """Return the result as a percentage of all results."""
        
        return (float(result) / len(self.results)) * 100
    
    def analyze(self):
        """Analyze the overall results."""
        
        margins_of_victory = []
        for result in self.results:
            if result.winner in self.win_counts:
                self.win_counts[result.winner] += 1
            else:
                self.win_counts[result.winner] = 1
                
            if result.largest_party in self.largest_party_counts:
                self.largest_party_counts[result.largest_party] += 1
            else:
                self.largest_party_counts[result.largest_party] = 1
                
            if result.runner_up in self.runnerup_counts:
                self.runnerup_counts[result.runner_up] += 1
            else:
                self.runnerup_counts[result.runner_up] = 1
                
            if result.third_place in self.third_place_counts:
                self.third_place_counts[result.third_place] += 1
            else:
                self.third_place_counts[result.third_place] = 1
                
            margins_of_victory.append(result.margin_of_victory)
            
            if result.most_seats_won > self.most_seats_won:
                self.most_seats_won = result.most_seats_won
                self.most_seats_won_party = result.largest_party
                
            if result.ukip_seats > 0:
                self.ukip_get_seats_count += 1
                
            if result.libdem_seats == 0:
                self.libdem_wipeout_count += 1
                
            if result.greens_hold_brighton:
                self.greens_hold_brighton_count += 1
                
            if result.seat_winner_is_pop_winner:
                self.seat_winner_is_pop_winner_count += 1
                
        self.mean_margin_of_victory = (sum(margins_of_victory) /
                                       len(self.results))
        
        return
    
    def run(self, iterations):
        """Run a full Monte Carlo simulation for the given number of iterations.
        """
        
        for ii in range(iterations):
            logger.info("Monte Carlo iteration {0}".format(ii))
            
            # Create a copy of the reference election to work with.
            this_election = copy.deepcopy(self.reference_election)
            
            # Tweak the poll numbers a bit to give us some variety.
            this_election.predicted_support = self.get_modified_support()
            
            # Now run this election and store its Result.  We copy it so that
            # the election itself can be immediately GCed.
            this_election.run()
            self.results.append(copy.deepcopy(this_election.result))
            
        # Now analyze the Monte Carlo results.
        self.analyze()
        
        return
        
        