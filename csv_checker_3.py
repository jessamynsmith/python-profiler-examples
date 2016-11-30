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

    write_file(os.path.join('output', 'lookup_errors_3.csv'), ['Row', 'Postal Code'], lookup_errors)


# If the script is being invoked as main, run the main method
if __name__ == "__main__":
    main()


# $ time python csv_checker_3.py
# Lookup Errors: 60
#
# real    0m1.220s
# user    0m0.964s
# sys     0m0.209s


# $ python -m cProfile -s cumtime csv_checker_3.py | head -n 30
# Lookup Errors: 60
#          243673 function calls (243603 primitive calls) in 1.313 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#       9/1    0.000    0.000    1.313    1.313 {built-in method builtins.exec}
#         1    0.000    0.000    1.313    1.313 csv_checker_3.py:3(<module>)
#         1    0.001    0.001    1.301    1.301 csv_checker_3.py:61(main)
#         1    0.093    0.093    1.300    1.300 csv_checker_3.py:27(count_data)
#     17010    0.025    0.000    0.938    0.000 __init__.py:117(__getitem__)
#     17010    0.044    0.000    0.913    0.000 __init__.py:114(get)
#     17010    0.031    0.000    0.777    0.000 csv_checker_3.py:18(query)
#     17010    0.649    0.000    0.649    0.000 {method 'execute' of 'sqlite3.Cursor' objects}
#     17012    0.182    0.000    0.260    0.000 py3.py:54(__next__)
#     17010    0.097    0.000    0.097    0.000 {method 'fetchall' of 'sqlite3.Cursor' objects}
#     17010    0.030    0.000    0.093    0.000 __init__.py:55(format_result)
#     17283    0.046    0.000    0.078    0.000 py3.py:51(<genexpr>)
#     16950    0.029    0.000    0.059    0.000 __init__.py:57(<listcomp>)
#     17282    0.032    0.000    0.032    0.000 {method 'decode' of 'bytes' objects}
#     16950    0.029    0.000    0.029    0.000 __init__.py:46(__init__)
#      12/3    0.000    0.000    0.012    0.004 <frozen importlib._bootstrap>:966(_find_and_load)
#      12/3    0.000    0.000    0.012    0.004 <frozen importlib._bootstrap>:939(_find_and_load_unlocked)
#      12/3    0.000    0.000    0.010    0.003 <frozen importlib._bootstrap>:659(_load_unlocked)
#       8/3    0.000    0.000    0.010    0.003 <frozen importlib._bootstrap_external>:659(exec_module)
#      16/3    0.000    0.000    0.009    0.003 <frozen importlib._bootstrap>:214(_call_with_frames_removed)
#         1    0.000    0.000    0.006    0.006 __init__.py:23(<module>)
#         1    0.000    0.000    0.006    0.006 dbapi2.py:23(<module>)
#     17010    0.005    0.000    0.005    0.000 {method 'strip' of 'str' objects}
#     17044    0.004    0.000    0.004    0.000 {built-in method builtins.len}
