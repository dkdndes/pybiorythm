#!/usr/bin/env python3
import argparse
import sys
from biorythm import main as biorythm_main


def create_parser():
    parser = argparse.ArgumentParser(
        description="Generate biorhythm charts (pseudoscience demonstration)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -y 1990 -m 5 -d 15
  python main.py --year 1990 --month 5 --day 15 --orientation horizontal
  python main.py -y 1990 -m 5 -d 15 --days 30 --orientation json-vertical
        """,
    )

    parser.add_argument("-y", "--year", type=int, help="Birth year (1-9999)")
    parser.add_argument("-m", "--month", type=int, help="Birth month (1-12)")
    parser.add_argument("-d", "--day", type=int, help="Birth day (1-31)")
    parser.add_argument(
        "--orientation",
        choices=["vertical", "horizontal", "json-vertical", "json-horizontal"],
        default="vertical",
        help="Chart orientation (default: vertical)",
    )
    parser.add_argument(
        "--days", type=int, default=29, help="Number of days to plot (default: 29)"
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # If no arguments provided, run interactive mode
    if not any([args.year, args.month, args.day]):
        biorythm_main()
    else:
        # Validate that all date components are provided
        if not all([args.year, args.month, args.day]):
            print(
                "Error: When using command line arguments, all date components (--year, --month, --day) must be provided"
            )
            sys.exit(1)

        # Call biorythm main with provided arguments
        biorythm_main(
            year=args.year,
            month=args.month,
            day=args.day,
            orientation=args.orientation,
            days=args.days,
        )


if __name__ == "__main__":
    main()
