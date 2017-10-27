#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
### THE MAIN SCRIPT
###
### PURPOSE
### The purpose of this script is to gather data about all the stocks noted on Oslo Bors and Oslo Axess and then
### presenting a rating list of which stocks has had the best result over time. Data includes stock dividends and
### stock values.
###
### CORE FILES
### 1) main.py      - Keeps the program structure and every sub-process.
### 2) db.py        - Includes every method used for sending/receiving data from the database.
### 3) download.py  - Accessing Oslo Bors and Oslo Axess (Netfonds) to scrape all current stock data.
### 4) dividend.py  - Parsing all dividend data and stores it into the database.
### 5) update.py    - Checks for dividend updates on Newsweb.
### 6) value.py     - Gets the value of each stock in the database at January 1st every year.
### 7) rating.py    - Gives a complete rating list of all the stocks and their performance based on input.
###
### @Author: Fredrik Bakken
### Email:   fredrik.bakken(at)gmail.com
### Website: https://www.fredrikbakken.no/
### Github:  https://github.com/FredrikBakken
###
### Last update: 22.09.2017
'''

import sys
import time
import schedule

from update import update
from rating import rating
from value import stocks_value
from download import download_stocks


def controller(argv):
    if len(argv) > 1:
        argument = argv[1]

        schedule.every().day.at(argument).do(run)

        while True:
            schedule.run_pending()
            time.sleep(3600)

    else:
        run()

def run():
    # Download and store all stocks into the database db_stocks.json
    download_stocks()

    # Check the latest stock value updates
    stocks_value()

    # Check the latest dividend updates
    update()

    # Give a rating of the stock's performance
    rating("all")

    return True


if __name__ == "__main__":
    controller(sys.argv)
