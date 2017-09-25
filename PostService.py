__author__ = 'James Lee'
__since__ = '15 Sept 2017'
import requests as req
import collections

# Global variables
# Default payload fields
fullName = "James Lee Zhong Kein"
email = "jamsawamsa@gmail.com"
message = ""
website = ""
github = ""
twitter = ""
linkedIn = ""
testMode = True

PAYLOAD = {'fullName': fullName, 'email': email, 'message': message, 'website': website,
'github': github, 'twitter':twitter, 'linkedin': linkedIn,'testMode': testMode }
HOR_SPLIT = "===================="


def is_empty():
    """
    Checks if the payload dictionary is empty
    :return: True is length of dictionary is 0, False otherwise
    """
    return len(PAYLOAD) == 0


def view_payload():
    """
    Prints the current payload to the terminal
    :return: None
    """
    print(HOR_SPLIT)
    print('Current payload:')
    for key, value in PAYLOAD.items():
        print("\t%s: %s" % (key, value))
    print(HOR_SPLIT)


def get_current_payload():
    """
    Gets the current payload to be posted
    :return: dictionary with the payload to post
    """
    r = {}
    for key, val in PAYLOAD.items():
        # check for whitespace at both ends
        if isinstance(PAYLOAD[key], str):
            if PAYLOAD[key].strip() != "":
                r[key] = PAYLOAD[key].strip()
        elif isinstance(PAYLOAD[key], bool):
            r[key] = PAYLOAD[key]
        # only submit fields with content
        else:
            continue

    return r


def driver_m():
    """
    Main, runs the menu
    :return: None
    """
    #  define vars and main menu
    url = 'https://www.pixl8.co.uk/api/jobs/v1/application/'
    dataFilled = False # denotes whether the payload has been filled/edited at least once

    menu = {} # main menu
    menu['1']="Reset and fill in fields"
    menu['2']="Add field"
    menu['3']="Del field"
    menu['4']='Edit item'
    menu['5']="Clear all data"
    menu['6']='Post'
    menu['7']='Change URL'
    menu['8']='Exit'

    # main loop
    while True:
        # checks for an empty payload
        if is_empty():
            dataFilled = False

        # print data if data has been filled at least once
        if dataFilled:
            print(HOR_SPLIT)
            print("URL:", url)
            print('Current payload:')
            for key, value in PAYLOAD.items():
                print("\t%s: %s" % (key, value))
            print(HOR_SPLIT)

        # print main menu
        options=collections.OrderedDict(sorted(menu.items()))
        for key, value in options.items():
            print("%s: %s" % (key, value))
        selection=input("Please select menu option:")

        # Reset fields and fill them in again
        if selection == '1':
            fields =collections.OrderedDict(sorted(PAYLOAD.items()))
            for key, value in fields.items():

                # Ensures only true or false is entered for testMode
                if key == 'testMode':
                    while not (entry.lower() == 'true' or entry.lower() == 'false'):
                        entry = input("Please enter 'true' or 'false' for testMode: ")
                    if entry == 'true'.lower():
                        entry = True
                    else:
                        entry = False
                # every other field
                else:
                    entry = input("What is your " + key + "?")

                # assign value to dictionary
                PAYLOAD[key] = entry
            dataFilled = True

        # Add a new field, only string fields can be added
        if selection == '2':
            newKey = input("Please enter the key of the new field: ")

            if newKey in PAYLOAD:
                print("Field already exists. Returning to main menu.")
                continue

            newValue = input("Please enter the value of the new field: ")
            PAYLOAD[newKey] = newValue

        # Delete a field
        if selection == '3':
            # Check if payload has no fields
            if is_empty():
                print("Nothing to delete.")
                continue

            # get field to delete
            delKey= input("Enter the field to delete: ")

            # delete field
            if delKey in PAYLOAD:
                PAYLOAD.pop(delKey)
            else:
                print("Field not found.")

        # Edit an item
        if selection == '4':
            # Check if payload has no fields
            if is_empty():
                print("Nothing to edit.")
                continue

            # get user input
            editKey = input("Select field to edit: ")

            # edit field
            if editKey in PAYLOAD:
                PAYLOAD[editKey] = input("Set new value: ")
            else:
                print('Field not found.')

        # Clear data
        if selection == '5':
            for key in PAYLOAD:
                PAYLOAD[key] = ""

                if key == 'testMode':
                    PAYLOAD[key] = False

            dataFilled = False

        # Post
        if selection == '6':
            # Check if payload has no fields
            if is_empty():
                print("Nothing to post.")
                continue

            # get user input
            decision = input('Are you sure you want to post? y/n ').lower()

            # user input validation
            while not (decision == 'y' or decision == 'n'):
                decision = input("Please enter 'y' or 'n': ")
            post = False

            # user confirmation
            if decision == 'y':
                post = True
            if post:
                # post the data
                try:
                    while url == "":
                        url = input('Please enter the destination URL: ')
                    curr_payload = get_current_payload()
                    r = req.post(url, data=curr_payload)

                    # print response
                    print("Payload header:\n ", r.headers)
                    print("Payload status:\n ",r.status_code)
                    r.raise_for_status()

                # catch HTTPError
                except req.HTTPError as e:
                    print("HTTPError:", e)

            print("Posted to:", url)

        #  Change URL
        if selection == '7':
            entry = ""
            while entry == "":
                entry = input('Please enter the new URL: ')

            url = entry

        # Exit program
        if selection == '8':
            print("Goodbye!")
            exit()

if __name__ == '__main__':
    driver_m()
