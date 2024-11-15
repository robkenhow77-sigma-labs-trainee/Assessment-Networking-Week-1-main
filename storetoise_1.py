"""The Storetoise CLI."""

from argparse import ArgumentParser
import requests

BASE_URL = "http://storetoise-lb-992940215.eu-west-2.elb.amazonaws.com"


class APIError(Exception):
    """An error for issues with contacting an API."""



def display_storage_ids(namespace: str, number: str = None) -> None:
    """Prints a list of storage IDs in ascending order based on a namespace given."""
    ...



def get_arg_parser() -> ArgumentParser:
    """Returns an argument parser object."""

    parser = ArgumentParser(prog="Storetoise CLI",
                            description="A command-line interface to the Storetoise API.")

    parser.add_argument("-u", "--username", help="The username for the namespace to use",
                        required=True)

    parser.add_argument(
        "-n", "--number", help="The number of results to return")

    # More command line arguments can be added here as required


    return parser

# TODO Write functions for your solution out here


if __name__ == "__main__":

    args = get_arg_parser().parse_args()
    # print("Arguments: ", args)

    try:

        # TODO Call functions for your solution inside here

        # display_storage_ids(namespace=args.username)


    except (ValueError, APIError) as e:

        print(str(e))
