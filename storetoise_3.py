"""The Storetoise CLI."""

from argparse import ArgumentParser
import requests

BASE_URL = "http://storetoise-lb-992940215.eu-west-2.elb.amazonaws.com"


class APIError(Exception):
    """An error for issues with contacting an API."""



def display_storage_ids(namespace: str, number: str = None) -> None:
    """Prints a list of storage IDs in ascending order based on a namespace given."""
    ids = sorted(get_API_json(namespace)["ids"])
    print(ids)
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


def send_message(username:str, id: int, message: str) -> None:
    if message != None:
        response = requests.post(f'{BASE_URL}/storage/{username}/{id}', json={"message": message})
        print(response.status_code)
        if response.status_code == 200:
            print(f"Message added to Storage ID {id} successfully.")
        else:
            print("Cannot add more than 10 messages to a storage ID.")


def get_arg_parser() -> ArgumentParser:
    """Returns an argument parser object."""

    parser = ArgumentParser(prog="Storetoise CLI", description="A command-line interface to the Storetoise API.")

    parser.add_argument("-u", "--username", help="The username for the namespace to use", required=True)
    parser.add_argument("-n", "--number", help="The number of results to return")
    parser.add_argument("-s", "--storage", help="Displays messages from a given id")
    parser.add_argument("-m", "--message", help="sends messages from a given id")

    return parser


def get_API_json(username: str) -> dict:
    response = requests.get(f'{BASE_URL}//storage/{username}')
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


def verify_message(message: str):
    if message != None:
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
    username = args.username
    number = verify_number(args.number)
    id = verify_storage(args.storage)
    message = verify_message(args.message)
    try:
        send_message(username, id, message)
        display_storage_ids(namespace=username, number=number)
        display_messages(username, id)
    except (ValueError, APIError) as e:
        print(str(e))


# "YYYYY", ",-", "./1'23", "aBcDeF", "readad."