#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
### DATABASE SCRIPT
###
### PURPOSE
### The purpose of the db script is to handle every inserts and every searches of the NoSQL tinyDB database.
###
### DATABASES
### Database | STOCKS |
### Ticker , Name , Source
###
### Database | ANNUAL STOCK VALUE |
### Ticker , Date , Value
###
### Database | DIVIDEND HISTORY |
### Ticker , Date , Dividend , Currency
###
### @Author: Fredrik Bakken
### Email:   fredrik.bakken(at)gmail.com
### Website: https://www.fredrikbakken.no/
### Github:  https://github.com/FredrikBakken
###
### Last update: 22.09.2017
'''

from tinydb import TinyDB, where

# Database links
db_stocks = TinyDB('data/db/db_stocks.json')
db_dividend_history = TinyDB('data/db/db_dividend_history.json')
db_annual_stock_value = TinyDB('data/db/db_annual_stock_value.json')


# INSERT DATABASE: Stocks
def db_insert_stocks(ticker, name, source):
    exist = db_search_stocks(ticker)
    if not exist:
        before = len(db_stocks)
        db_stocks.insert({'ticker': ticker, 'name': name, 'source': source})
        after = len(db_stocks)

        if after > before:
            return True
        else:
            return False
    else:
        return False


# INSERT DATABASE: Dividend History
def db_insert_dividend_history(ticker, date, dividend, currency):
    date_split = date.split('.')
    year = date_split[2]
    month = date_split[1]
    day = date_split[0]

    formatted_date = year + month + day

    exist = db_search_dividend_history(ticker, formatted_date, dividend)
    if not exist:
        before = len(db_dividend_history)
        db_dividend_history.insert({'ticker': ticker, 'date': formatted_date,
                                    'dividend': dividend, 'currency': currency})
        after = len(db_dividend_history)

        if after > before:
            return True
        else:
            return False
    else:
        return False


# INSERT DATABASE: Annual Stock Value
def db_insert_annual_stock_value(ticker, date, value):
    exist = db_search_annual_stock_value(ticker, date)
    if not exist:
        before = len(db_annual_stock_value)
        db_annual_stock_value.insert({'ticker': ticker, 'date': date, 'value': value})
        after = len(db_annual_stock_value)

        if after > before:
            return True
        else:
            return False
    else:
        return False


#  SEARCH DATABASE (DUPLICATE HANDLER): Stocks
def db_search_stocks(ticker):
    result = db_stocks.search(where('ticker') == ticker)
    return result


# SEARCH DATABASE (DUPLICATE HANDLER): Dividend History
def db_search_dividend_history(ticker, date, dividend):
    result = db_dividend_history.search((where('ticker') == ticker) &
                                        (where('date') == date) &
                                        (where('dividend') == dividend))

    print(result)
    return result


# SEARCH DATABASE (DUPLICATE HANDLER): Annual Stock Value
def db_search_annual_stock_value(ticker, date):
    result = db_annual_stock_value.search((where('ticker') == ticker) &
                                          (where('date') == date))

    return result


# GET LENGTH: Stocks
def db_number_of_stocks():
    number_of_stocks = len(db_stocks)
    return number_of_stocks


# GET STOCK: Based on ID
def db_id_stocks(s_id):
    element = db_stocks.get(eid=s_id)
    ticker = element.get('ticker')
    return ticker


# GET STOCK AND SOURCE: Based on ID
def db_id_stock_source(s_id):
    element = db_stocks.get(eid=s_id)
    ticker = element.get('ticker')
    source = element.get('source')
    return ticker, source


# SEARCH DATABASE: Get dividends
def db_get_dividends(ticker):
    result = db_dividend_history.search(where('ticker') == ticker)

    return result


# SEARCH DATABASE: Get annual stock value
def db_get_annual_stock_value(ticker):
    result = db_annual_stock_value.search(where('ticker') == ticker)
    return result
