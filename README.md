# Norwegian Stocks Rating

[![Python Powered](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

Norwegian Stocks Rating is a program for collecting all stocks on the norwegian stock market and then rating the stocks based upon historical values and dividends.

**Latest 'data' content updated:** 07.11.2017.

**Latest results can be found [here](https://github.com/FredrikBakken/Norwegian-Stocks-Rating/blob/master/results/profit_results.txt).**

## Installation

Install [Python 3.5.4](https://www.python.org/downloads/release/python-354/) and confirm the successful installation by running (in cmd):
```
py -3.5 --version
>>> Python 3.5.4
```

Open cmd, go to the project folder, and install the libraries by running:
```
py -3.5 -m pip install -r requirements.txt
```

## How to Run the Program

All commands described below can be ran from cmd.

### Running main.py
```
py -3.5 main.py
```

main.py runs all parts of the program and is therefore **not recommended** to run as it may cause issues for data providers (Netfonds/Newsweb). For the moment, the software needs to be manually updated by the user when it comes to dividend information. Running the main.py file may therefore result in the software stopping and an 'error' message showing, if there are new dividends which has not been handled. The developer will try to keep the files in the 'data' folder updated, so that you as a user won't have to do this manual task.

### Examples of Running rating.py
```
py -3.5 rating.py all           |    (Prints sorted rating based on all historical data and dividends)
py -3.5 rating.py 2015          |    (Prints sorted rating from 2015)
py -3.5 rating.py 2010 2014     |    (Prints sorted rating from 2010 to 2014)
```

![All rating example (16.10.2017)](https://github.com/FredrikBakken/Norwegian-Stocks-Rating/blob/master/images/run_results_example.png)

## Missing Features

 - Handle the stock value data in a more efficient way with tinyDB
 - Optimize the software for efficiency
 - Automate the collection of dividend data
 
## Contact Me
If you're having issues, please contact me on email: fredrik.bakken(at)gmail.com

Website: https://www.fredrikbakken.no/

### DISCLAIMER

DO NOT USE THIS SOFTWARE AS A RELIABLE SOURCE OF INFORMATION WHEN IT COMES TO INVESTING IN NORWEGIAN STOCKS. IT HAS NOT BEEN FULLY TESTED AND THERE ARE KNOWN ISSUES THAT HAS TO BE SOLVED. THE DEVELOPER WILL NOT TAKE ANY RESPONSIBILITY FOR ANY LOSSES THE INVESTOR MAY EXPERIENCE.

THIS SOFTWARE IS ONLY TO BE USED AS A TOOL FOR GETTING MORE INFORMATION ABOUT THE STOCKS ON THE NORWEGIAN MARKET. MAKE SURE TO DO YOUR OWN RESEARCH BEFORE TRUSTING ANY OF THE INFORMATION PROVIDED BY THIS SOFTWARE.

License
----

MIT


**Free Software, Hell Yeah!**
