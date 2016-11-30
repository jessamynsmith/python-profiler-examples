python-profiler-example
=======================

Examples of profiling Python code, used in this [Profiling Talk]()
    

Files
-----

Postal code checkers for a CSV:

    csv_checker_1.py - Naive approach
    csv_checker_2.py - Only connect to DB once
    csv_checker_3.py - Only lookup each postal code once
    csv_checker_4.py - Switch from DictReader to reader
    
Other examples:

    time_example.py          - Simple example of using time.time
    timeit_example.py        - Example of using timeit
    timeit_example_import.py - Example of using timeit with an import
    run_pstats.py            - Example of running pstats on profile data


Development
-----------

Fork the project on github and git clone your fork, e.g.:

    git clone https://github.com/<username>/python-profiler-example.git

Create a virtualenv using Python 3 and install dependencies. I recommend getting python3 via homebrew as well, then installing [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation) to that python. NOTE! You must change 'path/to/python3'
to be the actual path to python3 on your system.

    mkvirtualenv python-profiler-example --python=/path/to/python3
    pip install -r requirements.txt

Run any of the python scripts, e.g.:

    python csv_checker_1.py
    
Time any of the python scripts, e.g.:

    time python csv_checker_1.py
    
Profile any of the python scripts and show data, e.g.:

    python -m cProfile -s cumtime csv_checker_1.py
    
Profile any of the python scripts and save data for later analysis, e.g.:

    python -m cProfile -o output/csv_checker_1.cprof csv_checker_1.py
    
Analyze data with pstats (in python), e.g.:

    import pstats
    
    p = pstats.Stats('output/csv_checker_1.cprof')
    p.sort_stats('cumtime')
    p.print_stats()
    
