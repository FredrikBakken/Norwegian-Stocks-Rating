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
### (t) Ticker , (n) Name , (s) Source
###
### Database | ANNUAL STOCK VALUE |
### (t) Ticker , (d) Date , (v) Value
###
### Database | DIVIDEND HISTORY |
### (t) Ticker , (d) Date , (di) Dividend , (c) Currency
###
### Database | SPLIT HISTORY |
### (t) Ticker, (d) Date, (sf) From, (st) To
###
### Database | STOCK VALUES |
### (d) Date, (o) Open, (h) High, (l) Low, (c) Close, (vo) Volume, (va) Value
###
### @Author: Fredrik Bakken
### Email:   fredrik.bakken(at)gmail.com
### Website: https://www.fredrikbakken.no/
### Github:  https://github.com/FredrikBakken
###
### Last update: 12.10.2017
'''

import os

from tinydb import TinyDB, where

# Database links
db_stocks = TinyDB('data/db/db_stocks.json')
db_dividend_history = TinyDB('data/db/db_dividend_history.json')
db_split_history = TinyDB('data/db/db_split_history.json')
db_annual_stock_value = TinyDB('data/db/db_annual_stock_value.json')


# Generic method for insert response
def insert_success(before, after):
    if after > before:
        return True
    else:
        return False


# INSERT DATABASE: Stocks
def db_insert_stocks(ticker, name, source):
    exist = db_search_stocks(ticker)
    if not exist:
        before = len(db_stocks)
        db_stocks.insert({'t': ticker, 'n': name, 's': source})
        after = len(db_stocks)

        response = insert_success(before, after)
        return response
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
        db_dividend_history.insert({'t': ticker, 'd': formatted_date,
                                    'di': dividend, 'c': currency})
        after = len(db_dividend_history)

        response = insert_success(before, after)
        return response
    else:
        return False


# INSERT DATABASE: Ex.split History
def db_insert_split_history(ticker, date, split_from, split_to):
    date_split = date.split('.')
    year = date_split[2]
    month = date_split[1]
    day = date_split[0]
    formatted_date = year + month + day

    exist = db_search_split_history(ticker, formatted_date)
    if not exist:
        before = len(db_split_history)
        db_split_history.insert({'t': ticker, 'd': formatted_date,
                                 'sf': split_from, 'st': split_to})
        after = len(db_split_history)

        response = insert_success(before, after)
        return response
    else:
        return False


# INSERT DATABASE: Annual Stock Value
def db_insert_annual_stock_value(ticker, date, value):
    exist = db_search_annual_stock_value(ticker, date)
    if not exist:
        before = len(db_annual_stock_value)
        db_annual_stock_value.insert({'t': ticker, 'd': date, 'v': value})
        after = len(db_annual_stock_value)

        response = insert_success(before, after)
        return response
    else:
        return False


# INSERT DATABASE: Stock Value
def db_insert_stock_value(ticker, date, open, high, low, close, volume, value):
    filename = ticker + '.json'
    directory = 'data/db/value/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    db_stock_value = TinyDB(directory + filename)

    exist = db_search_stock_value(db_stock_value, date)
    if not exist:
        before = len(db_stock_value)
        db_stock_value.insert({'d': date, 'o': open, 'h': high, 'l': low,
                               'c': close, 'vo': volume, 'va': value})
        after = len(db_stock_value)

        response = insert_success(before, after)
        return response
    else:
        return False


#  SEARCH DATABASE (DUPLICATE HANDLER): Stocks
def db_search_stocks(ticker):
    result = db_stocks.search(where('t') == ticker)
    return result


# SEARCH DATABASE (DUPLICATE HANDLER): Dividend History
def db_search_dividend_history(ticker, date, dividend):
    result = db_dividend_history.search((where('t') == ticker) &
                                        (where('d') == date) &
                                        (where('di') == dividend))

    print(result)
    return result


def db_search_split_history(ticker, date):
    result = db_split_history.search((where('t') == ticker) &
                                     (where('d') == date))

    print(result)
    return result


# SEARCH DATABASE (DUPLICATE HANDLER): Annual Stock Value
def db_search_annual_stock_value(ticker, date):
    result = db_annual_stock_value.search((where('t') == ticker) &
                                          (where('d') == date))

    return result


# SEARCH DATABASE (DUPLICATE HANDLER): Stock Value
def db_search_stock_value(db, date):
    result = db.search(where('d') == date)

    return result


# GET LENGTH: Stocks
def db_number_of_stocks():
    number_of_stocks = len(db_stocks)
    return number_of_stocks


# GET STOCK: Based on ID
def db_id_stocks(s_id):
    element = db_stocks.get(eid=s_id)
    ticker = element.get('t')
    return ticker


# GET STOCK AND SOURCE: Based on ID
def db_id_stock_source(s_id):
    element = db_stocks.get(eid=s_id)
    ticker = element.get('t')
    source = element.get('s')
    return ticker, source


# SEARCH DATABASE: Get dividends
def db_get_dividends(ticker):
    result = db_dividend_history.search(where('t') == ticker)
    return result


# SEARCH DATABASE: Get splits
def db_get_splits(ticker):
    result = db_split_history.search(where('t') == ticker)
    return result


# SEARCH DATABASE: Get annual stock value
def db_get_annual_stock_value(ticker):
    result = db_annual_stock_value.search(where('t') == ticker)
    return result
