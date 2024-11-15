"""The Storetoise CLI."""

from argparse import ArgumentParser
import requests

BASE_URL = "http://storetoise-lb-992940215.eu-west-2.elb.amazonaws.com"


class APIError(Exception):
    """An error for issues with contacting an API."""



def display_storage_ids(namespace: str, number: str = None) -> None:
    """Prints a list of storage IDs in ascending order based on a namespace given."""
    ids = sorted(get_API_json(namespace)["ids"])
    message = ""
    if number == None:
        for id in ids:
            message += f"{id}\n"
    elif number > len(ids):
         for id in ids:
            message += f"{id}\n"
    else:
        for i in range(number):
            message += f"{ids[i]}\n"
       
    print(message[:-1])


def display_messages(username: str, id: int) -> None:
    response = requests.get(f'{BASE_URL}/storage/{username}/{id}')
    print(f'{BASE_URL}/storage/:{username}/:{id}')
    try:
        messages = response.json()["messages"]
        if len(messages) == 0:
            print(f'No messages found for storage ID {id}.')
        else:
            for i in range(len(messages)):
                print(f"{i}) {messages[i]}")
    except:
        print("Cannot get messages for a non-existent storage ID.")


def get_arg_parser() -> ArgumentParser:
    """Returns an argument parser object."""

    parser = ArgumentParser(prog="Storetoise CLI", description="A command-line interface to the Storetoise API.")

    parser.add_argument("-u", "--username", help="The username for the namespace to use", required=True)
    parser.add_argument("-n", "--number", help="The number of results to return")
    parser.add_argument("-s", "--storage", help="Displays messages from a given id")

    return parser


def get_API_json(username: str) -> dict:
    response = requests.get(f'{BASE_URL}//storage/:{username}')
    return response.json()


def verify_number(number: str):
    if number != None:
        if not number.isnumeric():
            print("Number must be an integer between 0 and 1000.")
            number = None
        elif float(number) < 0 or float(number) > 1000:
            print("Number must be an integer between 0 and 1000.")
            number = None
        else:
            number = int(number)
    return number


def verify_storage(number: str):
    if number != None:
        if not number.isnumeric():
            print("Storage ID must be a three-digit integer.")
            number = None
        elif len(number) != 3:
            print("Storage ID must be a three-digit integer.")
            number = None
        else:
            number = int(number)
    return number

if __name__ == "__main__":
    args = get_arg_parser().parse_args()
    print(args)
    username = args.username
    number = verify_number(args.number)
    id = verify_storage(args.storage)
    try:
        display_storage_ids(namespace=username, number=number)
        display_messages(username, id)
    except (ValueError, APIError) as e:
        print(str(e))