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

    write_file(os.path.join('output', 'lookup_errors_0.csv'), ['Row', 'Postal Code'], lookup_errors)


# If the script is being invoked as main, run the main method
if __name__ == "__main__":
    main()


# $ time python csv_checker_0.py
# Lookup Errors: 60
#
# real    0m4.547s
# user    0m3.453s
# sys     0m0.954s


# $ python -m cProfile -s cumtime csv_checker_0.py | head -n 30
# Lookup Errors: 60
#          447793 function calls (447718 primitive calls) in 4.549 seconds
#
#    Ordered by: cumulative time
#
#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#       9/1    0.000    0.000    4.549    4.549 {built-in method builtins.exec}
#         1    0.000    0.000    4.549    4.549 csv_checker_0.py:3(<module>)
#         1    0.000    0.000    4.529    4.529 csv_checker_0.py:42(main)
#         1    0.117    0.117    4.527    4.527 csv_checker_0.py:11(count_data)
#     17010    0.030    0.000    3.847    0.000 __init__.py:117(__getitem__)
#     17010    0.093    0.000    3.817    0.000 __init__.py:114(get)
#     17010    0.077    0.000    3.607    0.000 __init__.py:20(query)
#     17010    2.093    0.000    2.093    0.000 {method 'execute' of 'sqlite3.Cursor' objects}
#     17011    0.848    0.000    0.848    0.000 {built-in method _sqlite3.connect}
#     17011    0.199    0.000    0.545    0.000 csv.py:106(__next__)
#     17011    0.473    0.000    0.473    0.000 {method 'close' of 'sqlite3.Connection' objects}
#     17012    0.018    0.000    0.297    0.000 {built-in method builtins.next}
#     17012    0.187    0.000    0.279    0.000 py3.py:54(__next__)
#     17010    0.037    0.000    0.117    0.000 __init__.py:55(format_result)
#     17010    0.098    0.000    0.098    0.000 {method 'fetchall' of 'sqlite3.Cursor' objects}
#     17283    0.053    0.000    0.092    0.000 py3.py:51(<genexpr>)
#     16950    0.036    0.000    0.075    0.000 __init__.py:57(<listcomp>)
#     16950    0.040    0.000    0.040    0.000 __init__.py:46(__init__)
#     34021    0.029    0.000    0.038    0.000 csv.py:92(fieldnames)
#     17282    0.038    0.000    0.038    0.000 {method 'decode' of 'bytes' objects}
#     17010    0.025    0.000    0.025    0.000 {method 'cursor' of 'sqlite3.Connection' objects}
#      12/2    0.000    0.000    0.019    0.010 <frozen importlib._bootstrap>:966(_find_and_load)
#      12/2    0.000    0.000    0.019    0.009 <frozen importlib._bootstrap>:939(_find_and_load_unlocked)
#      12/2    0.000    0.000    0.018    0.009 <frozen importlib._bootstrap>:659(_load_unlocked)
