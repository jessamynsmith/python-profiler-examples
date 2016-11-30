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

    write_file(os.path.join('output', 'lookup_errors_1.csv'), ['Row', 'Postal Code'], lookup_errors)


# If the script is being invoked as main, run the main method
if __name__ == "__main__":
    main()


# $ time python csv_checker_1.py
# Lookup Errors: 60
#
# real	0m1.586s
# user	0m1.226s
# sys	0m0.235s


# python -m cProfile -s cumtime csv_checker_1.py | head -n 30
# Lookup Errors: 60
#          396767 function calls (396697 primitive calls) in 1.804 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#       9/1    0.000    0.000    1.804    1.804 {built-in method builtins.exec}
#         1    0.000    0.000    1.804    1.804 csv_checker_1.py:3(<module>)
#         1    0.001    0.001    1.784    1.784 csv_checker_1.py:58(main)
#         1    0.096    0.096    1.782    1.782 csv_checker_1.py:27(count_data)
#     17010    0.024    0.000    1.194    0.000 __init__.py:117(__getitem__)
#     17010    0.042    0.000    1.170    0.000 __init__.py:114(get)
#     17010    0.029    0.000    1.035    0.000 csv_checker_1.py:18(query)
#     17010    0.914    0.000    0.914    0.000 {method 'execute' of 'sqlite3.Cursor' objects}
#     17011    0.162    0.000    0.475    0.000 csv.py:106(__next__)
#     17012    0.016    0.000    0.265    0.000 {built-in method builtins.next}
#     17012    0.174    0.000    0.249    0.000 py3.py:54(__next__)
#     17010    0.031    0.000    0.093    0.000 __init__.py:55(format_result)
#     17010    0.092    0.000    0.092    0.000 {method 'fetchall' of 'sqlite3.Cursor' objects}
#     17283    0.046    0.000    0.075    0.000 py3.py:51(<genexpr>)
#     16950    0.029    0.000    0.058    0.000 __init__.py:57(<listcomp>)
#     34021    0.028    0.000    0.037    0.000 csv.py:92(fieldnames)
#     16950    0.029    0.000    0.029    0.000 __init__.py:46(__init__)
#     17282    0.029    0.000    0.029    0.000 {method 'decode' of 'bytes' objects}
#      12/3    0.000    0.000    0.020    0.007 <frozen importlib._bootstrap>:966(_find_and_load)
#      12/3    0.000    0.000    0.020    0.007 <frozen importlib._bootstrap>:939(_find_and_load_unlocked)
#      12/3    0.000    0.000    0.019    0.006 <frozen importlib._bootstrap>:659(_load_unlocked)
#       8/3    0.000    0.000    0.018    0.006 <frozen importlib._bootstrap_external>:659(exec_module)
#      16/3    0.000    0.000    0.017    0.006 <frozen importlib._bootstrap>:214(_call_with_frames_removed)
#     51031    0.016    0.000    0.016    0.000 py3.py:64(line_num)
