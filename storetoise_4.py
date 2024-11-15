"""The Storetoise CLI."""

from argparse import ArgumentParser
import requests

BASE_URL = "http://storetoise-lb-992940215.eu-west-2.elb.amazonaws.com"


class APIError(Exception):
    """An error for issues with contacting an API."""


def get_storage_ids(namespace: str):
    """Returns the all the ids for a given username"""
    response = requests.get(f'{BASE_URL}//storage/{namespace}')
    return sorted(response.json()["ids"])


def display_storage_ids(namespace: str, number: str = None) -> None:
    """Prints a list of storage IDs in ascending order based on a namespace given."""
    ids = get_storage_ids(namespace)
    if number is None or number > len(ids):
        for num in ids:
            print(num)
    else:
        for num in ids[:number]:
            print(num)


def display_messages(username: str, id: int) -> None:
    """Displays all messages for a given ID"""
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


def send_message(username:str, id: int, message: str) -> None:
    """Sends a message to a given ID"""
    if message is not None:
        response = requests.post(f'{BASE_URL}/storage/{username}/{id}', json={"message": message})
        print(response.status_code)
        if response.status_code == 200:
            print(f"Message added to Storage ID {id} successfully.")
        else:
            print("Cannot add more than 10 messages to a storage ID.")


def delete_messages(username:str, id: int, delete: bool) -> None:
    """Deletes all messages from a a given ID"""
    if delete:
        response = requests.delete(f'{BASE_URL}/storage/{username}/{id}')
        print(response.status_code)
        if response.status_code == 200:
            print(f'Storage ID {id} deleted successfully.')
        else:
            print("Cannot delete a non-existent storage ID.")


def get_arg_parser() -> ArgumentParser:
    """Returns an argument parser object."""

    parser = ArgumentParser(prog="Storetoise CLI",
                            description="A command-line interface to the Storetoise API.")
    parser.add_argument("-u", "--username",
                        help="The username for the namespace to use", required=True)
    parser.add_argument("-n", "--number",
                        help="The number of results to return")
    parser.add_argument("-s", "--storage",
                        help="Displays messages from a given id")
    parser.add_argument("-m", "--message",
                        help="sends messages from a given id")
    parser.add_argument("-d", "--delete",
                        help="deletes all messages from a given id", action="store_true")
    return parser


def verify_number(number: str):
    """Verifies if number is a valid integer"""
    if number is not None:
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
    """Verifies storage ID"""
    if number is not None:
        if not number.isnumeric():
            print("Storage ID must be a three-digit integer.")
            number = None
        elif len(number) != 3:
            print("Storage ID must be a three-digit integer.")
            number = None
        else:
            number = int(number)
    return number


def verify_message(message: str):
    """Verifies message is valid"""
    if message is not None:
        if len(message) > 140:
            print("Message must be 140 characters or fewer.")
            return None
        if not message.replace(" ", "").isalpha():
            print("Message must consist only of lowercase letters and spaces.")
            return None
        if not message.islower():
            print("Message must consist only of lowercase letters and spaces.")
            return None
    return message


if __name__ == "__main__":
    args = get_arg_parser().parse_args()
    try:
        delete_messages(args.username, verify_storage(args.storage), args.delete)
        send_message(args.username, verify_storage(args.storage), verify_message(args.message))
        display_storage_ids(args.username, verify_number(args.number))
        display_messages(args.username, verify_storage(args.storage))
    except (ValueError, APIError) as e:
        print(str(e))
