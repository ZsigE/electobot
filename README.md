electobot
=========

## What is Electobot?
Electobot provides election results analysis for UK General Elections. Its aim is to make it possible to predict the outcome of the 2015 General Election based on polling data, with greater accuracy than can be provided by a [Uniform National Swing](http://en.wikipedia.org/wiki/Uniform_national_swing) projection.

## What do I need to run it?
The only dependency right now is Python 2.7. Electobot should run on any platform for which Python 2.7 has been released, although it's only been tested on Windows so far.

Once you have the code, run `python electobot.py -h` to see the available options for running simulations. (You'll want to specify `harvard_election_results_2010.csv` as the CSV file.)

## What still needs doing?
Plenty! Right now Electobot can simulate the outcome of an election based on polling data, and can also run a [Monte Carlo simulation](http://en.wikipedia.org/wiki/Monte_Carlo_method) to apply some random variation. Still to do:
  * ~~Tweaking the model - right now it appears to be biased too heavily towards the results of the 2010 election~~ **Done!**
  * ~~Tuning the randomization to give interesting but still plausible outcomes~~ **Done**, but tweaking still encouraged
  * Adding a web server interface to allow kicking off simulations online
  * ~~Multithreading the Monte Carlo simulation to take advantage of multiple-core systems~~ **Done!**
  * Using more of the data (turnout/socioeconomic indicators/etc) to improve the model
  * Anything else!

## Where's the documentation?
The code is pretty well commented, so that's a good place to start. I'll also be trying to document the code in a more user-friendly way on the Wiki. Watch [this space](http://github.com/ZsigE/electobot/wiki/Electobot).

## Where did the election data come from?
Electobot uses two data sources: [the Guardian's datablog](http://www.theguardian.com/news/datablog/2010/may/07/uk-election-results-data-candidates-seats) and [Pippa Norris's dataset](http://www.hks.harvard.edu/fs/pnorris/Data/Data.htm#) from the John F Kennedy School of Government at Harvard University. Both have been converted to CSV files and checked into the repo.
