electobot
=========

## What is Electobot?
Electobot provides election results analysis for UK General Elections. Its aim is to make it possible to predict the outcome of the 2015 General Election based on polling data, with greater accuracy than can be provided by a [Uniform National Swing](http://en.wikipedia.org/wiki/Uniform_national_swing) projection.

## I don't care how it works, what are the results?
I have now started [a blog](http://electobot.wordpress.com) to answer that very question.

## What do I need to run it?
### If you want to simulate elections...
The only dependency right now is Python 2.7. Electobot should run on any platform for which Python 2.7 has been released, although it's only been tested on Windows so far.
### If you want to visualize the results...
You'll also need [matplotlib](http://matplotlib.org/) and [numpy](http://www.numpy.org/).

Once you have the code and any dependencies, run `python run_electobot.py -h` to see the available options for running simulations.

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

## Are you using any third-party code?
Funny you should mention that. Electobot uses [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) v4.3.2, which can be included in code like this under the MIT License (see the LICENSE file for the full text).

## Where did the election data come from?
Electobot uses two data sources: [the Guardian's datablog](http://www.theguardian.com/news/datablog/2010/may/07/uk-election-results-data-candidates-seats) and [Pippa Norris's dataset](http://www.hks.harvard.edu/fs/pnorris/Data/Data.htm#) from the John F Kennedy School of Government at Harvard University. Both have been converted to CSV files and checked into the repo.

Historical polling data comes from [Wikipedia](http://en.wikipedia.org/wiki/Opinion_polling_for_the_next_United_Kingdom_general_election), so take it with a pinch of salt and check the latest revisions before running based on that!