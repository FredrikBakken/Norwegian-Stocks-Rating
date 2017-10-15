#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
### DOWNLOAD SCRIPT
###
### PURPOSE
### The purpose of the download script is to download all current stock data from the different norwegian markets,
### then storing the relevant data into the stocks database.
###
### @Author: Fredrik Bakken
### Email:   fredrik.bakken(at)gmail.com
### Website: https://www.fredrikbakken.no/
### Github:  https://github.com/FredrikBakken
###
### Last update: 15.10.2017
'''

import os
import csv
import shutil
import requests
import contextlib

from db import db_insert_stocks, db_search_stocks


filename = 'data/tmp-stocks/stocks.json'


def download_stocks():
    # Oslo Bors, Oslo Axess, and Merkur stock urls
    markets = [['OSE', 'Oslo Børs'], ['OAX', 'Oslo Axess'], ['MERK', 'Merkur']]

    directory = 'data/tmp-stocks/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Delete old stocks overview file
    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)

    # Open session
    with requests.Session() as s:

        # Loop through defined markets
        for x in range(len(markets)):
            market_tag = markets[x][0]
            market_name = markets[x][1]

            # Download stocks on the market
            download = s.get('http://www.netfonds.no/quotes/kurs.php?exchange=' + market_tag + '&sec_types=&sectors=&ticks=&table=tab&sort=alphabetic')
            decode = download.content.decode('iso-8859-1')
            csr = csv.reader(decode.splitlines(), delimiter='\t')
            stocklist = list(csr)
            stocklist.pop(0)

            # Write stocks to file
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file, delimiter=',')

                for row in stocklist:
                    print("Download ticker: " + row[1])
                    row.append(market_name)
                    writer.writerow(row)

    print('Updated stocks data has been downloaded to: ' + filename)

    # Store stocks into the database
    store_stocks()

    # Remove temporary stock data storage
    if os.path.exists(directory):
        shutil.rmtree(directory)

    return True


def store_stocks():
    # Open temporary stocks file
    with open(filename, 'rU') as file:

        # Read line for line the temporary stocks file
        for line in file:
            cells = line.split(",")
            name = str(cells[0])
            ticker = str(cells[1])
            source = str(cells[13].strip())

            # Run through tests before inserting data to the database
            if 'OBTEST' not in ticker:
                exist_ticker = db_search_stocks(ticker)

                if not exist_ticker:
                    db_insert_stocks(ticker, name, source)

    print('New stocks has been stored in the database.')

    return True


# Setting starting method
if __name__ == "__main__":
    download_stocks()
