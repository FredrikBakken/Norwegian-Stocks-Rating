#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
### RATING SCRIPT
###
### PURPOSE
### The purpose of the rating script is to rate the different stocks found on the norwegian market based upon their
### historical value and dividends.
###
### PS! DO NOT use the results from the rating script as the decider for whether or not to buy a specific stock. Make
### sure to do enough research about the companies you are thinking of buying stocks for. This program is just a
### tool to give rating evaluation of their historical performance and does not predict the future.
###
### @Author: Fredrik Bakken
### Email:   fredrik.bakken(at)gmail.com
### Website: https://www.fredrikbakken.no/
### Github:  https://github.com/FredrikBakken
###
### Last update: 12.10.2017
'''

import sys
import datetime

from prettytable import PrettyTable

from db import db_get_dividends, db_get_splits, db_get_stock_value, db_get_stock_value_year, db_number_of_stocks, db_id_stocks


def calculate_profit(ticker, dividend, start, end, split_variation):
    start_split = (start / split_variation)
    if not start == 0:
        profit = (end + dividend) / start_split
    else:
        profit = 0
    return [ticker, profit, start, start_split, end, dividend]


def sort_on_date(data):
    date_list = []

    # Loop through database data and append date to list
    for x in range(len(data)):
        date_list.append(data[x]['d'])

    # Sort the date_list from first date to last date
    sorted_list = sorted(date_list, key=lambda x: datetime.datetime.strptime(x, '%Y%m%d'))

    return sorted_list


def rating(arg):
    number_of_arguments = 0
    int_arg = 0
    if not arg == 'all':
        number_of_arguments = (len(arg) - 1)
    profit_list = []

    try:
        int_arg = int(arg[1]) - 1
        bool_year = True
    except:
        bool_year = False

    # If rate select is 'all' historical stocks
    if ((number_of_arguments == 1 and arg[1] == 'all') or (arg == 'all')):
        print("Rate stocks for all historical values...")

        # Get the number of stocks in the database
        number_of_stocks = db_number_of_stocks()

        # Loop through the database and get the tickers
        for x in range(number_of_stocks):
            # Variables
            total_dividend = 0

            # Find ticker
            stock_id = (x + 1)
            ticker = db_id_stocks(stock_id)

            # Find total dividend data
            dividend_data = db_get_dividends(ticker)
            dividend_date_list = sort_on_date(dividend_data)

            if len(dividend_date_list) > 0:
                from_date_dividend = dividend_date_list[0]
                to_date_dividend = dividend_date_list[(len(dividend_date_list) - 1)]

                if ((float(from_date_dividend) > 0) and (float(to_date_dividend) > 0)):
                    for x in range(len(dividend_data)):
                        current_date = dividend_data[x]['d']

                        if from_date_dividend <= current_date <= to_date_dividend:
                            total_dividend = total_dividend + float(dividend_data[x]['di'])

            # Check for split data
            split_data = db_get_splits(ticker)
            split_variation = 1
            for x in range(len(split_data)):
                split_from = split_data[x]['sf']
                split_to = split_data[x]['st']

                split_variation = ((split_variation * float(split_from)) / float(split_to))

            # Find start and end stock value
            stock_data = db_get_stock_value(ticker)
            stock_date_list = sort_on_date(stock_data)

            if len(stock_date_list) > 0:
                from_date_stock = stock_date_list[0]
                to_date_stock = stock_date_list[-1]

                if ((float(from_date_stock) > 0) and (float(to_date_stock) > 0)):
                    val_f = False
                    val_t = False

                    for x in range(len(stock_data)):
                        if stock_data[x]['d'] == from_date_stock:
                            start_stock_value = float(stock_data[x]['c'])
                            val_f = True
                        elif stock_data[x]['d'] == to_date_stock:
                            end_stock_value = float(stock_data[x]['c'])
                            val_t = True

                        if val_f and val_t:
                            break

            profit = calculate_profit(ticker, total_dividend, start_stock_value, end_stock_value, split_variation)
            profit_list.append(profit)

    # If rate select is specific year
    elif number_of_arguments == 1 and bool_year:
        print("Rate stocks for year " + arg[1] + '...')

        # Get the number of stocks in the database
        number_of_stocks = db_number_of_stocks()

        # Loop through the database and get the tickers
        for x in range(number_of_stocks):
            # Variables
            total_dividend = 0

            # Find ticker
            stock_id = (x + 1)
            ticker = db_id_stocks(stock_id)

            # Find total dividend data
            dividend_data = db_get_dividends(ticker)
            dividend_date_list = sort_on_date(dividend_data)

            for x in range(len(dividend_date_list)):
                if dividend_data[x]['d'].startswith(arg[1]):
                    total_dividend = total_dividend + float(dividend_data[x]['di'])

            # Check for split data
            split_data = db_get_splits(ticker)
            split_date_list = sort_on_date(split_data)
            split_variation = 1
            for x in range(len(split_date_list)):
                if split_data[x]['d'].startswith(arg[1]):
                    split_from = split_data[x]['sf']
                    split_to = split_data[x]['st']

                    split_variation = ((split_variation * float(split_from)) / float(split_to))

            # Find start and end stock value
            stock_data = db_get_stock_value_year(ticker, arg[1])
            stock_date_list = sort_on_date(stock_data)

            if len(stock_date_list) > 0:
                from_date_stock = stock_date_list[0]
                to_date_stock = stock_date_list[-1]

                if ((float(from_date_stock) > 0) and (float(to_date_stock) > 0)):
                    val_f = False
                    val_t = False

                    for x in range(len(stock_data)):
                        if stock_data[x]['d'] == from_date_stock:
                            start_stock_value = float(stock_data[x]['c'])
                            val_f = True
                        elif stock_data[x]['d'] == to_date_stock:
                            end_stock_value = float(stock_data[x]['c'])
                            val_t = True

                        if val_f and val_t:
                            break

            profit = calculate_profit(ticker, total_dividend, start_stock_value, end_stock_value, split_variation)
            profit_list.append(profit)

    # If rate selected is from/to specific years
    elif number_of_arguments == 2:
        print("Rating stocks from " + arg[1] + " to " + arg[2] + '...')

        # Add relevant years to a list
        year_from = int(arg[1])
        year_to = int(arg[2])
        difference = (year_to - year_from)
        years = []

        for x in range(difference + 1):
            years.append(year_from + x)

        # Get the number of stocks in the database
        number_of_stocks = db_number_of_stocks()

        # Loop through the database and get the tickers
        for x in range(number_of_stocks):
            # Variables
            total_dividend = 0
            #end_stock_value = 0

            # Find ticker
            stock_id = (x + 1)
            ticker = db_id_stocks(stock_id)

            # Find total dividend data
            dividend_data = db_get_dividends(ticker)

            for x in range(len(years)):
                for y in range(len(dividend_data)):
                    if dividend_data[y]['d'].startswith(str(years[x])):
                        total_dividend = total_dividend + float(dividend_data[y]['di'])

            # Check for split data
            split_data = db_get_splits(ticker)

            split_variation = 1
            for x in range(len(years)):
                for y in range(len(split_data)):
                    if split_data[y]['d'].startswith(str(years[x])):
                        split_from = split_data[y]['sf']
                        split_to = split_data[y]['st']

                        split_variation = ((split_variation * float(split_from)) / float(split_to))

            # Find start and end stock value
            start_stock_data = db_get_stock_value_year(ticker, arg[1])
            start_stock_date_list = sort_on_date(start_stock_data)

            end_stock_data = db_get_stock_value_year(ticker, arg[2])
            end_stock_date_list = sort_on_date(end_stock_data)


            if len(start_stock_data) > 0 and len(end_stock_data) > 0:
                from_date_stock = start_stock_date_list[0]
                to_date_stock = end_stock_date_list[-1]

                if ((float(from_date_stock) > 0) and (float(to_date_stock) > 0)):
                    val_f = False
                    val_t = False

                    for x in range(len(start_stock_data)):
                        if start_stock_data[x]['d'] == from_date_stock:
                            start_stock_value = float(start_stock_data[x]['c'])
                            break

                    for x in range(len(end_stock_data)):
                        if end_stock_data[x]['d'] == to_date_stock:
                            end_stock_value = float(end_stock_data[x]['c'])
                            break

            profit = calculate_profit(ticker, total_dividend, start_stock_value, end_stock_value, split_variation)
            profit_list.append(profit)

    # Else: Invalid arguments
    else:
        print("That is an invalid argument, please use one of the following arguments:\n"
              "'all', 'year', 'from_year to_year'")

    sorted_list = sorted(profit_list, key=lambda x: x[1])

    t = PrettyTable(['Loss / Profit', 'Ticker', 'Total (%)', 'From stock value (orginal)', 'From stock value (split)', 'To stock value', 'Total dividend'])

    for x in range(len(sorted_list)):
        if sorted_list[x][1] > 1:
            loss_profit = 'PROFIT'
        elif sorted_list[x][1] < 1:
            loss_profit = 'LOSS'
        else:
            loss_profit = 'NO CHANGE'

        if sorted_list[x][5] == 0:
            dividend = '-'
        else:
            dividend = '{0:.2f}'.format(sorted_list[x][5]) + ' kr'

        if not (sorted_list[x][1] == 0 and sorted_list[x][2] == 0 and sorted_list[x][4] == 0):
            t.add_row([loss_profit, sorted_list[x][0], '{:.3%}'.format(sorted_list[x][1]),
                       '{0:.2f}'.format(sorted_list[x][2]), '{0:.2f}'.format(sorted_list[x][3]),
                       '{0:.2f}'.format(sorted_list[x][4]), dividend])

    # return [ticker, profit, start, start_split, end, dividend]

    print(t)

    print('\nWARNING! DO NOT TRUST THE CURRENT RESULTS!!!\n')

    print('\nSoftware has been developed by Fredrik Bakken.\n'
          '\nEmail:   fredrik.bakken(at)gmail.com'
          '\nWebsite: https://www.fredrikbakken.no/'
          '\nGithub:  https://www.github.com/FredrikBakken\n'
          "\nThank you for trying out this free stock rating software.")

if __name__ == "__main__":
    rating(sys.argv)
