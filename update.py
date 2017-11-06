#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
### UPDATE SCRIPT
###
### PURPOSE
### The purpose of this file is to check for updated dividend data and manually extracting the updates from the
### www.newsweb.no website in an efficient manner. This way of manually working with the data is a prototype solution
### until an efficient and fail-proof automated solution has been designed.
###
### WHAT DATA TO STORE
### | Ticker            | Last run date (dd.mm.yyyy)    | Number of entries     |
### | Date (dd.mm.yyy)  | Type (Dividend / Info)        | Amount (float / X)    |
###
### @Author: Fredrik Bakken
### Email:   fredrik.bakken(at)gmail.com
### Website: https://www.fredrikbakken.no/
### Github:  https://github.com/FredrikBakken
###
### Last update: 22.09.2017
'''

import os
import sys
import math
import time
import datetime
import contextlib

from bs4 import BeautifulSoup
from urllib.request import urlopen

from dividend import store_dividends
from db import db_id_stocks, db_number_of_stocks


def file_exist(filename):
    try:
        open(filename, 'r')
        return True
    except IOError:
        return False


def get_url(page, ticker, from_date, today):
    eks_dato = '1101'

    url = 'http://www.newsweb.no/newsweb/search.do?headerSearch=' \
          '&searchCriteria.categoryIds=' \
          '&selectedPagenumber=' + str(page) + \
          '&searchSubmitType=searchtype' \
          '&searchtype=full' \
          '&searchCriteria.issuerSign=' + ticker + \
          '&searchCriteria.instrumentShortName=' \
          '&searchCriteria.categoryId=' + eks_dato + \
          '&searchCriteria.fromDate=' + from_date + \
          '&searchCriteria.toDate=' + today + \
          '&searchCriteria.exchangeCode=' \
          '&_searchCriteria.activeIssuersOnly=' \
          '&searchCriteria.activeIssuersOnly=true'
    print(url)
    return url


def update():
    updates_filename = 'data/updates.txt'
    number_of_stocks = db_number_of_stocks()

    # Start by deleting the updates.txt file
    with contextlib.suppress(FileNotFoundError):
        os.remove(updates_filename)

    # Execute one ticker at the time
    for x in range(number_of_stocks):

        # Get today's date
        today = datetime.datetime.today().strftime('%d.%m.%Y')

        # Get ticker from db_stocks.json
        stock_id = (x + 1)
        ticker = db_id_stocks(stock_id)
        filename = 'data/div-split/' + ticker + '.json'

        # Check if file exist
        exist = file_exist(filename)
        first_line_split = ''

        # Find which date last updates are from
        if not exist:
            from_date = '01.01.1900'
            previous_entries = 0

            # Write first line to files
            with open(filename, 'a') as f:
                f.write(ticker + ',' + today + ',' + str(previous_entries) + '\n')
        else:
            with open(filename, 'r') as f:
                first_line = f.readline()
                lines = f.readlines()

            first_line_split = first_line.split(",")
            from_date = first_line_split[1]
            previous_entries = first_line_split[2]


        # Get number of pages to check and number of new entries
        url = get_url(1, ticker, from_date, today)
        web_content = urlopen(url).read()
        soup = BeautifulSoup(web_content, "html.parser")
        hits = str(soup.find_all('div', attrs={'class': 'hits'}))
        entries = int(''.join(x for x in hits if x.isdigit()))
        pages = int(math.ceil(entries / 25))
        print("Number of updates: " + str(entries))

        # Update entries
        total_entries = (int(previous_entries) + int(entries))
        new_line = (ticker + ',' + today + ',' + str(total_entries) + '\n')

        check_date = ''
        # Get latest dividend entry date
        if (len(lines) > 0):
            date_line = lines[0]
            date_line_split = date_line.split(",")
            check_date = date_line_split[0]

        date_list = []

        # Go through all pages and extract rows
        for page in range(pages):
            time.sleep(1)  # Avoid DDoS
            page_number = (page + 1)
            dividend_url = get_url(page_number, ticker, from_date, today)

            dividend_page = urlopen(dividend_url).read()
            soup_table = BeautifulSoup(dividend_page, "html.parser")
            table = soup_table.find('table', attrs={'class': 'messageTable'})
            rows = table.find_all('tr')

            # Get update dates
            for row in rows[1:]:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]

                date = cols[0].split(' ')[0]
                if not date == check_date:
                    element = date + ',type,amount\n'
                    if not element in date_list:
                        date_list.append(element)

        # Overwrite file with new data
        with open(filename, 'w') as f:
            f.write(first_line.replace(first_line, new_line))
            for element in date_list:
                f.write(element)
            for line in lines:
                f.write(line)

        # Check every file for updates
        missing_updates = 0
        with open(filename, 'r') as f:
            for line in f:
                if ("type" in line) or ("amount" in line):
                    missing_updates = missing_updates + 1

        # Append all missing data to updates file ('ticker' : number of missing updates)
        with open(updates_filename, 'a') as upd:
            if missing_updates > 0:
                upd.write(ticker + ': ' + str(missing_updates) + '\n')

    updates_size = os.stat(updates_filename).st_size

    # If the updates.txt is empty
    if updates_size == 0:
        store_dividends()

    # There are new dividend updates which has not been fixed
    else:
        sys.exit("\nOBS!\nThere are new dividend updates which has to be manually updated.\n"
                 "Please check in the '/data/updates.txt' for more information.")

    return True


# Setting starting method
if __name__ == "__main__":
    update()
