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
### Last update: 22.09.2017
'''

import sys
import datetime

from prettytable import PrettyTable

from db import db_get_dividends, db_number_of_stocks, db_id_stocks


def calculate_profit(ticker, dividend, start, end):
    profit = (end + dividend) / (start)
    return [ticker, profit, start, end, dividend]


def sort_on_date(data):
    date_list = []

    # Loop through database data and append date to list
    for x in range(len(data)):
        date_list.append(data[x]['date'])

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
                        current_date = dividend_data[x]['date']

                        if from_date_dividend <= current_date <= to_date_dividend:
                            total_dividend = total_dividend + float(dividend_data[x]['dividend'])

            # Find start and end stock value
            filename = 'data/stocks/' + ticker + '.csv'
            with open(filename, 'r') as f:
                next(f)
                second_line = f.readline()
                second_line_split = second_line.split(',')
                end_stock_value = float(second_line_split[6])
                last_line = list(f)[-1]
                last_line_split = last_line.split(',')
                start_stock_value = float(last_line_split[6])

            profit = calculate_profit(ticker, total_dividend, start_stock_value, end_stock_value)
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
            end_stock_value = 0

            # Find ticker
            stock_id = (x + 1)
            ticker = db_id_stocks(stock_id)

            # Find total dividend data
            dividend_data = db_get_dividends(ticker)
            dividend_date_list = sort_on_date(dividend_data)

            for x in range(len(dividend_date_list)):
                if dividend_date_list[x].startswith(arg[1]):
                    total_dividend = total_dividend + float(dividend_data[x]['dividend'])

            # Find start and end stock value
            filename = 'data/stocks/' + ticker + '.csv'
            found_date = False
            with open(filename, 'r') as f:
                previous_line = []
                for line in f:
                    split_line = line.split(',')
                    if not found_date and split_line[0].startswith(arg[1]):
                        end_stock_value = float(split_line[6])
                        found_date = True

                    if split_line[0].startswith(str(int_arg)):
                        break
                    previous_line = line

                previous_line_split = previous_line.split(',')
                start_stock_value = float(previous_line_split[6])

            profit = calculate_profit(ticker, total_dividend, start_stock_value, end_stock_value)
            profit_list.append(profit)

    # If rate selected is from/to specific years
    elif number_of_arguments == 2:
        print("Rating stocks from " + arg[1] + " to " + arg[2] + '...')

        # Add relevanted years to a list
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
            end_stock_value = 0

            # Find ticker
            stock_id = (x + 1)
            ticker = db_id_stocks(stock_id)

            # Find total dividend data
            dividend_data = db_get_dividends(ticker)

            for x in range(len(years)):
                for y in range(len(dividend_data)):
                    if dividend_data[y]['date'].startswith(str(years[x])):
                        total_dividend = total_dividend + float(dividend_data[y]['dividend'])

            # Find start and end stock value
            filename = 'data/stocks/' + ticker + '.csv'
            found_date = False
            before_start_year = year_from - 1
            with open(filename, 'r') as f:
                previous_line = []
                for line in f:
                    split_line = line.split(',')
                    if not found_date and split_line[0].startswith(str(year_to)):
                        end_stock_value = float(split_line[6])
                        found_date = True

                    if split_line[0].startswith(str(before_start_year)):
                        break
                    previous_line = line

                previous_line_split = previous_line.split(',')
                start_stock_value = float(previous_line_split[6])

            profit = calculate_profit(ticker, total_dividend, start_stock_value, end_stock_value)
            profit_list.append(profit)

    # Else: Invalid arguments
    else:
        print("That is an invalid argument, please use one of the following arguments:\n"
              "'all', 'year', 'from_year to_year'")

    sorted_list = sorted(profit_list, key=lambda x: x[1])

    t = PrettyTable(['Loss / Profit', 'Ticker', 'Total (%)', 'From stock value', 'To stock value', 'Total dividend'])

    for x in range(len(sorted_list)):
        if sorted_list[x][1] > 1:
            loss_profit = 'PROFIT'
        elif sorted_list[x][1] < 1:
            loss_profit = 'LOSS'
        else:
            loss_profit = 'NO CHANGE'

        if sorted_list[x][4] == 0:
            dividend = '-'
        else:
            dividend = '{0:.2f}'.format(sorted_list[x][4]) + ' kr'

        if not (sorted_list[x][1] == 0 and sorted_list[x][2] == 0 and sorted_list[x][3] == 0):
            t.add_row([loss_profit, sorted_list[x][0], '{:.3%}'.format(sorted_list[x][1]),
                       '{0:.2f}'.format(sorted_list[x][2]), '{0:.2f}'.format(sorted_list[x][3]), dividend])

    print(t)
    print('\nSoftware has been developed by Fredrik Bakken.\n'
          '\nEmail:   fredrik.bakken(at)gmail.com'
          '\nWebsite: https://www.fredrikbakken.no/'
          '\nGithub:  https://www.github.com/FredrikBakken\n'
          "\nThank you for trying out this free software I've made.")

if __name__ == "__main__":
    rating(sys.argv)
