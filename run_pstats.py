import pstats


def main():
    p = pstats.Stats('output/csv_checker_1.cprof')
    p.sort_stats('cumtime')
    p.print_stats(20)


# If the script is being invoked as main, run the main method
if __name__ == "__main__":
    main()
