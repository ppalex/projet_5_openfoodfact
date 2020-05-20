import argparse

from Controller.controller import Controller
from jobs import drop_tables_job, initialize_job


def main():
    controller = Controller()
    controller.init()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='OpenFoodFact')
    parser.add_argument('--job', type=str, nargs=1,
                        help='Launch the script to create tables in DB, \
                                get data from API and fill DB with data.')
    args = parser.parse_args()

    if args.job:
        if args.job[0] == 'initialize':

            initialize_job()

        elif args.job[0] == 'drop_tables':
            drop_tables_job()
    else:
        main()
