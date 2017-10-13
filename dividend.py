#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
### DIVIDEND SCRIPT
###
### PURPOSE
### The purpose of the dividend script is to store all dividend data into the database. This is done only after the
### complete check in update.py is done.
###
### @Author: Fredrik Bakken
### Email:   fredrik.bakken(at)gmail.com
### Website: https://www.fredrikbakken.no/
### Github:  https://github.com/FredrikBakken
###
### Last update: 12.10.2017
'''

import sys

from db import db_number_of_stocks, db_id_stocks, db_insert_dividend_history, db_insert_split_history


def store_dividends():
    # Get the number of stocks in the database
    number_of_stocks = db_number_of_stocks()

    # Loop through the database and get the tickers
    for x in range(number_of_stocks):
        stock_id = (x + 1)
        ticker = db_id_stocks(stock_id)

        # Handle dividends for each ticker
        handle_dividend(ticker)

    return True


def handle_dividend(ticker):
    # File name for each tickers
    ticker_filename = 'data/div/' + ticker + '.json'

    # Open file
    with open(ticker_filename, 'r') as f:
        # Skip first line
        next(f)

        # For each line in file
        for line in f:
            # Split line and organize content into: date and type
            line_split = line.split(',')
            date = line_split[0]
            data_type = line_split[1]
            data_value = line_split[2]

            # Perform a control check of the contents
            if not ((data_type == 'Dividend') or (data_type == 'Ex.Split') or (data_type == 'Info')):
                sys.exit('\nOBS!\nThere are dividend/split updates which has not been fixed.\n'
                         'Please update data for file: ' + ticker_filename)

            # If line is dividend, store into dividend database
            if data_type == 'Dividend':
                amount_holder = data_value
                amount_holder_split = amount_holder.split(' ')
                dividend = amount_holder_split[0]
                currency = amount_holder_split[-1].rstrip()
                db_insert_dividend_history(ticker, date, dividend, currency)
                print(ticker + " has dividend on " + date + " at " + dividend + ' ' + currency)

            # If line is ex.split, store into split database
            if data_type == 'Ex.Split':
                split_data = data_value
                split_data_split = split_data.split(':')
                split_from = split_data_split[0]
                split_to = split_data_split[-1].rstrip()
                db_insert_split_history(ticker, date, split_from, split_to)
                print(ticker + " has ex.split on " + date + " at rate: " + split_data)

    return True


if __name__ == "__main__":
    store_dividends()
