#!/usr/bin/env python

"""A further attempt at optimizing postal code checking for a CSV: look up each postal code once"""

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

    lookup_errors = {}

    with open(infile, "rb") as csv_in:
        reader = csv.DictReader(csv_in, encoding='utf-8')

        i = 1
        for row in reader:
            i += 1
            postal_code = row['Postal Code'].strip().upper()
            if postal_code in lookup_errors:
                lookup_errors[postal_code].append(i)
            else:
                forward_sortation_area = postal_code[:3]
                try:
                    pcdb[forward_sortation_area]
                except IndexError:
                    lookup_errors[postal_code] = [i]

    return lookup_errors


def write_file(filename, fields, data):

    with open(filename, "wb") as csv_out:
        writer = csv.writer(csv_out, encoding='utf-8')

        writer.writerow(fields)
        for key in data:
            for item in data[key]:
                writer.writerow([item, key])


def main():
    # Input CSV file
    infile = 'data/bps_raw_data_2013_revised_en.csv'
    lookup_errors = count_data(infile)

    print('Lookup Errors: {}'.format(len(lookup_errors)))

    write_file(os.path.join('output', 'lookup_errors_2.csv'), ['Row', 'Postal Code'], lookup_errors)


# If the script is being invoked as main, run the main method
if __name__ == "__main__":
    main()


# $ time python csv_checker_2.py
# Lookup Errors: 60
#
# real	0m1.526s
# user	0m1.206s
# sys	0m0.230s


# $ python -m cProfile -s cumtime csv_checker_2.py | head -n 30
# Lookup Errors: 36
#          396563 function calls (396493 primitive calls) in 1.563 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#       9/1    0.000    0.000    1.563    1.563 {built-in method builtins.exec}
#         1    0.000    0.000    1.563    1.563 csv_checker_2.py:3(<module>)
#         1    0.001    0.001    1.555    1.555 csv_checker_2.py:62(main)
#         1    0.106    0.106    1.554    1.554 csv_checker_2.py:27(count_data)
#     16986    0.025    0.000    0.933    0.000 __init__.py:117(__getitem__)
#     16986    0.042    0.000    0.908    0.000 __init__.py:114(get)
#     16986    0.030    0.000    0.770    0.000 csv_checker_2.py:18(query)
#     16986    0.641    0.000    0.641    0.000 {method 'execute' of 'sqlite3.Cursor' objects}
#     17011    0.169    0.000    0.506    0.000 csv.py:106(__next__)
#     17012    0.016    0.000    0.286    0.000 {built-in method builtins.next}
#     17012    0.192    0.000    0.270    0.000 py3.py:54(__next__)
#     16986    0.098    0.000    0.098    0.000 {method 'fetchall' of 'sqlite3.Cursor' objects}
#     16986    0.031    0.000    0.097    0.000 __init__.py:55(format_result)
#     17283    0.048    0.000    0.078    0.000 py3.py:51(<genexpr>)
#     16950    0.030    0.000    0.061    0.000 __init__.py:57(<listcomp>)
#     34021    0.029    0.000    0.039    0.000 csv.py:92(fieldnames)
#     16950    0.031    0.000    0.031    0.000 __init__.py:46(__init__)
#     17282    0.030    0.000    0.030    0.000 {method 'decode' of 'bytes' objects}
#     51031    0.017    0.000    0.017    0.000 py3.py:64(line_num)
#      12/3    0.000    0.000    0.009    0.003 <frozen importlib._bootstrap>:966(_find_and_load)
#      12/3    0.000    0.000    0.008    0.003 <frozen importlib._bootstrap>:939(_find_and_load_unlocked)
#     51040    0.008    0.000    0.008    0.000 {built-in method builtins.len}
#      12/3    0.000    0.000    0.007    0.002 <frozen importlib._bootstrap>:659(_load_unlocked)
#       8/3    0.000    0.000    0.007    0.002 <frozen importlib._bootstrap_external>:659(exec_module)
