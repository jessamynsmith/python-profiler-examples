#!/usr/bin/env python

"""Naive approach to postal code checking for a CSV"""

import os

from pypostalcode import PostalCodeDatabase
import unicodecsv as csv


def count_data(infile):
    pcdb = PostalCodeDatabase()

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

    write_file(os.path.join('output', 'lookup_errors_1.csv'), ['Row', 'Postal Code'], lookup_errors)


# If the script is being invoked as main, run the main method
if __name__ == "__main__":
    main()


# 4806
# Snapshot saved to /Users/jessamyn/Library/Caches/PyCharm2016.2/snapshots/pyladies-profiler19.pstat

# $ time python csv_checker_1.py
# Lookup Errors: 60
#
# real    0m4.547s
# user    0m3.453s
# sys     0m0.954s
