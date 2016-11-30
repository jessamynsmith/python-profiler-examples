#!/usr/bin/env python

"""A final attempt at optimizing postal code checking for a CSV: replace DictReader with reader"""

import os
import sqlite3

from pypostalcode import PostalCodeDatabase
from pypostalcode.settings import db_location
import unicodecsv as csv


class ConnectionManager(object):
    def __init__(self):
        self.conn = sqlite3.connect(db_location)
        self.cursor = self.conn.cursor()

    def query(self, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def close(self):
        self.conn.close()


def count_data(infile):
    pcdb = PostalCodeDatabase(ConnectionManager())

    lookup_errors = []

    with open(infile, "rb") as csv_in:
        reader = csv.reader(csv_in, encoding='utf-8')

        # Skip header row
        next(reader)

        i = 1
        for row in reader:
            i += 1
            postal_code = row[6].strip().upper()
            forward_sortation_area = postal_code[:3]
            try:
                pcdb[forward_sortation_area]
            except IndexError:
                lookup_errors.append([i, postal_code])

    return lookup_errors


def write_file(filename, fields, data):

    with open(filename, "wb") as csv_out:
        writer = csv.writer(csv_out, encoding='utf-8')

        writer.writerow(fields)
        for row in data:
            writer.writerow(row)


def main():
    # Input CSV file
    infile = 'data/bps_raw_data_2013_revised_en.csv'
    lookup_errors = count_data(infile)

    print('Lookup Errors: {}'.format(len(lookup_errors)))

    write_file(os.path.join('output', 'lookup_errors_4.csv'), ['Row', 'Postal Code'], lookup_errors)


# If the script is being invoked as main, run the main method
if __name__ == "__main__":
    main()


# 1337
# Snapshot saved to /Users/jessamyn/Library/Caches/PyCharm2016.2/snapshots/pyladies-profiler27.pstat

# $ time python csv_checker_4.py
# Lookup Errors: 60
#
# real    0m1.220s
# user    0m0.964s
# sys     0m0.209s
