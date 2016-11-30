#!/usr/bin/env python

"""First cut at optimizing postal code checking for a CSV: only connect to DB once"""

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
        reader = csv.DictReader(csv_in, encoding='utf-8')

        i = 1
        for row in reader:
            i += 1
            postal_code = row['Postal Code'].strip().upper()
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

    write_file(os.path.join('output', 'lookup_errors_2.csv'), ['Row', 'Postal Code'], lookup_errors)


# If the script is being invoked as main, run the main method
if __name__ == "__main__":
    main()


# 1570
# Snapshot saved to /Users/jessamyn/Library/Caches/PyCharm2016.2/snapshots/pyladies-profiler21.pstat

# $ time python csv_checker_2.py
# Lookup Errors: 60
#
# real    0m1.384s
# user    0m1.133s
# sys     0m0.209s