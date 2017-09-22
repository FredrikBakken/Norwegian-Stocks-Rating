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
### Last update: 22.09.2017
'''

import csv
import requests

from db import db_insert_stocks, db_search_stocks


json_storage = 'data/json/stocks.json'


def download_stocks():
    # Oslo Bors, Oslo Axess, and Merkur stock urls
    url_bors = 'http://www.netfonds.no/quotes/kurs.php?exchange=OSE' \
               '&sec_types=&sectors=&ticks=&table=tab&sort=alphabetic'
    url_axess = 'http://www.netfonds.no/quotes/kurs.php?exchange=OAX' \
                '&sec_types=&sectors=&ticks=&table=tab&sort=alphabetic'
    url_merkur = 'http://www.netfonds.no/quotes/kurs.php?exchange=MERK' \
                 '&sec_types=&sectors=&ticks=&table=tab&sort=alphabetic'

    # Open urls
    with requests.Session() as s:
        # Access data from Oslo Bors
        download_bors = s.get(url_bors)
        decode_bors = download_bors.content.decode('iso-8859-1')
        csr_bors = csv.reader(decode_bors.splitlines(), delimiter='\t')
        list_bors = list(csr_bors)
        list_bors.pop(0)

        # Access data from Oslo Axess
        download_axess = s.get(url_axess)
        decode_axess = download_axess.content.decode('iso-8859-1')
        csr_axess = csv.reader(decode_axess.splitlines(), delimiter='\t')
        list_axess = list(csr_axess)
        list_axess.pop(0)

        # Access data from Merkur
        download_merkur = s.get(url_merkur)
        decode_merkur = download_merkur.content.decode('iso-8859-1')
        csr_merkur = csv.reader(decode_merkur.splitlines(), delimiter='\t')
        list_merkur = list(csr_merkur)
        list_merkur.pop(0)

        # Open write access to temporary stocks file
        with open(json_storage, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')

            # Write data from Oslo Bors
            for row in list_bors:
                print(row)
                row.append('Oslo Børs')
                writer.writerow(row)

            # Write data from Oslo Axess
            for row in list_axess:
                print(row)
                row.append('Oslo Axess')
                writer.writerow(row)

            # Write data from Merkur
            for row in list_merkur:
                print(row)
                row.append('Merkur')
                writer.writerow(row)

    print("Updated stocks data has been downloaded to 'data/json/stocks.json'.")

    # Store stocks into the database
    store_stocks()

    return True


def store_stocks():
    # Open temporary stocks file
    with open(json_storage, 'rU') as file:

        # Read line for line the temporary stocks file
        for line in file:
            cells = line.split(",")
            name = str(cells[0])
            ticker = str(cells[1])
            source = str(cells[13].strip())

            # Run through tests before inserting data to the database
            if "OBTEST" not in ticker:
                exist_ticker = db_search_stocks(ticker)

                if not exist_ticker:
                    db_insert_stocks(ticker, name, source)

    print("New stocks has been stored in the database: 'data/db/db_stocks.json'.")

    return True


# Setting starting method
if __name__ == "__main__":
    download_stocks()
