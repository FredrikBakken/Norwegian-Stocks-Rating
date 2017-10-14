#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
### VALUE SCRIPT
###
### PURPOSE
### The purpose of this part of the script is to find all the historical value data (since 1950) for every stock on
### the norwegian stock market and download them into the folder 'data/stocks'.
###
### @Author: Fredrik Bakken
### Email:   fredrik.bakken(at)gmail.com
### Website: https://www.fredrikbakken.no/
### Github:  https://github.com/FredrikBakken
###
### Last update: 22.09.2017
'''

import datetime

from urllib.request import urlopen

from db import db_id_stock_source, db_number_of_stocks, db_insert_annual_stock_value, db_insert_stock_value


def stocks_value():
    # Get the number of stocks in the database
    number_of_stocks = db_number_of_stocks()

    # Loop through the database and get the tickers
    for x in range(number_of_stocks):
        stock_id = (x + 1)
        element = db_id_stock_source(stock_id)
        ticker = element[0]
        source = element[1]

        # Handle dividends for each ticker
        get_stock_values(ticker, source)

    return True


def get_stock_values(ticker, source):
    # Get the correct urls based on the stored source data
    url = ''
    if source == 'Oslo Børs':
        url = 'http://www.netfonds.no/quotes/paperhistory.php?paper=' + ticker + '.OSE&csv_format=csv'
    elif source == 'Oslo Axess':
        url = 'http://www.netfonds.no/quotes/paperhistory.php?paper=' + ticker + '.OAX&csv_format=csv'
    elif source == 'Merkur':
        url = 'http://www.netfonds.no/quotes/paperhistory.php?paper=' + ticker + '.MERK&csv_format=csv'
    else:
        print("Incorrect")

    # Download the latest historical ticker data
    filename = 'data/stocks/' + ticker + '.csv'
    response = urlopen(url)
    html = response.read()
    with open(filename, 'wb') as f:
        f.write(html)

    print("Stocks data from " + ticker + " has been downloaded to: " + filename)

    # Store annual stock values into database
    store_annual_stock_values(ticker, filename)

    # Store all stock values into databases
    store_stock_values(ticker, filename)

    return True


def store_annual_stock_values(ticker, filename):
    # Set start date (year)
    start_year = 1950
    this_year = datetime.datetime.now().year
    current_line = ''

    # For loop (this year - start date):
    for x in range(this_year - start_year):
        checking_year = start_year + x

        # Search file for data on this date
        with open(filename, 'r') as f:
            previous_date = ''

            # Read each line in the file
            for line in f:
                current_line = line.split(",")
                date = current_line[0]
                checking_new_year = str(checking_year) + '01'
                checking_previous_year = date[:4] + '12'

                # If line is last day in a year
                if (checking_previous_year in date) and (checking_new_year in previous_date):
                    value = current_line[6]

                    # Insert into the database
                    db_insert_annual_stock_value(ticker, date, value)

                # Update the previous date
                previous_date = date

    # Insert the last date (first day on the market) into the database
    last_line = current_line
    last_date = last_line[0]
    last_value = last_line[6]

    # Insert into the database
    db_insert_annual_stock_value(ticker, last_date, last_value)

    return True


def store_stock_values(ticker, filename):
    response = True

    with open(filename, 'r') as f:
        first_line = f.readline()

        # Read each line in the file
        for line in f:
            if response:
                current_line = line.split(",")
                date = current_line[0]
                vopen = current_line[3]
                vhigh = current_line[4]
                vlow = current_line[5]
                vclose = current_line[6]
                volume = current_line[7]
                value = current_line[8].rstrip()

                response = db_insert_stock_value(ticker, date, vopen, vhigh, vlow, vclose, volume, value)
            else:
                return True

    return True


if __name__ == "__main__":
    stocks_value()
