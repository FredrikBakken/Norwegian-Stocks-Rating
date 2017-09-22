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
### Last update: 22.09.2017
'''

from db import db_number_of_stocks, db_id_stocks, db_insert_dividend_history


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
            # Split line and organize content into: date, type, amount, currency
            line_split = line.split(',')
            date = line_split[0]
            data_type = line_split[1]
            amount_holder = line_split[2]
            amount_holder_split = amount_holder.split(' ')
            dividend = amount_holder_split[0]
            currency = amount_holder_split[-1].rstrip()

            # If line is dividend, store into dividend database
            if data_type == 'Dividend':
                db_insert_dividend_history(ticker, date, dividend, currency)
                print(ticker + " has dividend on " + date + " at " + dividend + ' ' + currency)

    return True


if __name__ == "__main__":
    store_dividends()
