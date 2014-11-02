#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

Main module
"""

# Python imports
import argparse
import cPickle as pickle
import logging
import sys
import datetime

# Electobot imports
import electobot.election as election
from electobot.constants import *
import electobot.montecarlo as montecarlo
import electobot.pollscrape as pollscrape

# Set up logging
logger = logging.getLogger("electobot")
    
# Functions
def run_electobot():
    """Main function."""

    # Set up logging.
    if not os.path.exists(LOGS_DIR):
        os.mkdir(LOGS_DIR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                  '%(levelname)s - %(message)s')
    handler = logging.FileHandler(LOG_FILE, mode="w")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
     
    # Parse the input arguments.
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--debug",
                        help="Switch on debug logging",
                        action="store_true",
                        default=False,
                        dest="debug")
    
    fileopts = parser.add_argument_group("File options")
    fileopts.add_argument("--loadfile", "-p",
                          help="File containing saved-off results data",
                          action="store",
                          dest="pickle")
    fileopts.add_argument("--savefile", "-s", 
                          help="Filename for saving results data",
                          action="store",
                          dest="savefile")
    
    simopts = parser.add_argument_group("Simulation options")
    simopts.add_argument("--single-election", "-1",
                         help="Simulate a single election",
                         action="store_true",
                         dest="single_election")
    simopts.add_argument("--montecarlo", "-m",
                         help="Run a Monte Carlo simulation",
                         action="store",
                         type=int,
                         default=0,
                         dest="iterations")
    simopts.add_argument("--new-polls", "-e",
                         help="Simulate based on any new polling data",
                         action="store_true",
                         dest="newpolls")
    
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
    partyopts.add_argument("--scot-con",
                           help="Predicted percentage of Conservative support "
                                                                  "in Scotland",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="scot_con")
    partyopts.add_argument("--scot-lab",
                           help="Predicted percentage of Labour support in "
                                                                     "Scotland",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="scot_lab")
    partyopts.add_argument("--scot-libdem",
                           help="Predicted percentage of Lib-Dem support in "
                                                                     "scotland",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="scot_ld")
    partyopts.add_argument("--scot-green",
                           help="Predicted percentage of Green support in "
                                                                     "Scotland",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="scot_grn")
    partyopts.add_argument("--scot-ukip",
                           help="Predicted percentage of UKIP support in "
                                                                     "Scotland",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="scot_ukp")
    partyopts.add_argument("--scot-snp",
                           help="Predicted percentage of SNP support in "
                                                                    "Scotland",
                           action="store",
                           type=float,
                           default=0.0,
                           dest="scot_snp")
    
    chartopts = parser.add_argument_group("Data visualisation options")
    chartopts.add_argument("--chart-type",
                           help="Type of chart to create (options: pie, line)",
                           action="store",
                           type=str,
                           default="",
                           dest="charttype")
    chartopts.add_argument("--chart-location",
                           help="Filename of this chart, minus filetype suffix",
                           action="store",
                           type=str,
                           default="",
                           dest="chartloc")
    chartopts.add_argument("--start-date",
                           help="Chart results from this date onwards "
                                                                 "(YYYY-MM-DD)",
                           action="store",
                           default=None,
                           dest="startdate")
    chartopts.add_argument("--end-date",
                           help="Chart results up to and including this date "
                                                                 "(YYYY-MM-DD)",
                           action="store",
                           default=None,
                           dest="enddate")
    chartopts.add_argument("--pollsters",
                           help="Comma-separated list of pollsters to include",
                           action="store",
                           default=None,
                           dest="pollsters")
    chartopts.add_argument("--sponsors",
                           help="Comma-separated list of sponsors to include",
                           action="store",
                           default=None,
                           dest="sponsors")
    chartopts.add_argument("--min-sample-size",
                           help="Minimum sample size of poll to include",
                           action="store",
                           type=int,
                           default=0,
                           dest="minsamplesize")
    

    opts = parser.parse_args()
        
    if opts.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(LOG_LEVEL)
    
    if opts.charttype == "line":
        # Generating a line chart from saved data.
        assert opts.pickle is not None, "No saved results file specified"
        assert opts.chartloc != "", "No chart filename specified"
        with open(opts.pickle, "r") as loadfile:
            savedpolls = pickle.load(loadfile)
        
        # Do the plotting import here to avoid making matplotlib a dependency
        # unless absolutely necessary.
        import electobot.electoplot as plot
        
        # If dates have been provided, convert them to datetimes.
        if opts.startdate is not None:
            startdate = datetime.datetime.strptime(opts.startdate, "%Y-%m-%d")
        else:
            startdate = None
            
        if opts.enddate is not None:
            enddate = datetime.datetime.strptime(opts.enddate, "%Y-%m-%d")
        else:
            enddate = None

        # If pollsters or sponsors have been provided, convert them to lists.
        if opts.pollsters is not None:
            pollsters = opts.pollsters.split(",")
        else:
            pollsters = None
            
        if opts.sponsors is not None:
            sponsors = opts.sponsors.split(",")
        else:
            sponsors = None
                
        plot.create_line_range_chart(savedpolls, 
                                     opts.chartloc,
                                     start_date=startdate,
                                     end_date=enddate,
                                     min_sample_size=opts.minsamplesize,
                                     pollsters=pollsters,
                                     sponsors=sponsors)
    else:
        # Populate the election from the CSV data file.
        elect = election.Election()
        elect.populate_from_csv()
        
        # For no apparent reason, the Harvard data does not include the total
        # votes cast in each constituency in 2010.  Fill this in from the 
        # Guardian data instead.
        elect.add_total_2010_votes()
        
        if opts.newpolls:
            # Fetch new polling data from the internet and simulate any that 
            # isn't already in our saved data.
            assert opts.savefile is not None,  \
                "No filename specified for saving results"
            if opts.iterations == 0:
                logger.info("No number of iterations specified, using 1000")
                iter = 1000
            else:
                iter = opts.iterations
            
            if opts.pickle is not None:
                with open(opts.pickle, "r") as pickle_file:
                    saved_polls = pickle.load(pickle_file)
                    logger.info("Loaded {0} saved polls from file".
                                format(len(saved_polls)))
            else:
                saved_polls = []
                
            scraper = pollscrape.PollScrape()
            scraper.create_polls_from_table()
            
            # Calculate only those polls that aren't already in our dataset.
            polls_to_calculate = set(scraper.polls) - set(saved_polls)
            for index, poll in enumerate(polls_to_calculate, start=1):
                logger.info("Running poll {0} of {1}".
                                                format(index, 
                                                       len(polls_to_calculate)))
                logger.debug("Running poll with following support:")
                logger.debug(str(poll.support))
                elect.predicted_support = poll.support
                poll.result = montecarlo.run_multithreaded_montecarlo(elect, 
                                                                      iter)
                saved_polls.append(poll)
                
                # Update the saved polls list after every run in case it gets
                # interrupted.
                with open(opts.savefile, "w") as pickle_file:
                    pickle.dump(saved_polls, pickle_file)
            
            logger.info("Completed generating from new polls")
        else:    
            # Fill in the support for each party from the command-line 
            # arguments.
            overall_support = {
                               CON: opts.conservative,
                               LAB: opts.labour,
                               LD: opts.libdem,
                               SNP: opts.snp,
                               PC: opts.plaid,
                               GRN: opts.green,
                               BNP: opts.bnp,
                               UKP: opts.ukip,
                              }
            
            elect.predicted_support = elect.prepare_predicted_support(
                                                                overall_support)
            
            if opts.scot_snp > 0:
                # We have a set of Scotland-only support.  Prepare this as well.
                scot_support = {
                                CON: opts.scot_con,
                                LAB: opts.scot_lab,
                                LD: opts.scot_ld,
                                SNP: opts.scot_snp,
                                GRN: opts.scot_grn,
                                UKP: opts.scot_ukp
                               }
                elect.regional_support = {"Scotland": 
                                  elect.prepare_predicted_support(scot_support)} 
                    
            if opts.single_election:
                assert elect is not None, "No election data to work with"
                elect.run()
                print elect.result.summary
                if len(elect.result.ukip_stealth_targets) > 0:
                    # Some UKIP stealth targets have been found - print them
                    # here.
                    print ("{0} UKIP stealth targets identified:".
                                 format(len(elect.result.ukip_stealth_targets)))
                    for tgt in elect.result.ukip_stealth_targets:
                        print "  {0}: CON majority {1}".format(tgt,
                                         elect.result.ukip_stealth_targets[tgt])
                if opts.charttype == "pie":
                    # Do the plotting import here to avoid making matplotlib a
                    # dependency unless absolutely necessary
                    import electobot.electoplot as plot
                    plot.create_pie_chart(elect.result.seats, opts.chartloc)
                    
            elif opts.iterations > 0:
                assert elect is not None, "No election data to work with"
                mc_result = montecarlo.run_multithreaded_montecarlo(elect,
                                                                opts.iterations)
                mc_result.report()
                
                if opts.charttype == "bar":
                    import electobot.electoplot as plot
                    plot.create_poll_summary_barchart(mc_result, opts.chartloc)
                
        return
    
if __name__ == "__main__":
    run_electobot()    
    