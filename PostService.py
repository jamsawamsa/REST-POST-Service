__author__ = 'James Lee'
__since__ = '15 Sept 2017'
import requests as req
import collections


def is_empty(payload):
    """
    Checks if the payload dictionary is empty
    :return: True is length of dictionary is 0, False otherwise
    """
    return len(payload) == 0


def view_payload(url, payload):
    """
    Prints the current payload to the terminal
    :return: None
    """
    HOR_SPLIT = "===================="
    print(HOR_SPLIT)
    print("URL:", url)
    print('Current payload:')
    for key, value in payload.items():
        print("\t%s: %s" % (key, value))
    print(HOR_SPLIT)


def get_current_payload(payload):
    """
    Gets the current payload to be posted
    :return: dictionary with the payload to post
    """
    r = {}
    for key, val in payload.items():
        # check for whitespace at both ends
        if isinstance(payload[key], str):
            if payload[key].strip() != "":
                r[key] = payload[key].strip()
        elif isinstance(payload[key], bool):
            r[key] = payload[key]
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

    # Default payload fields
    fullName = ""
    email = ""
    message = ""
    website = ""
    github = ""
    twitter = ""
    linkedIn = "https://www.linkedin.com/in/jamsawamsa/"
    testMode = True

    payload = {'fullName': fullName, 'email': email, 'message': message, 'website': website,
    'github': github, 'twitter':twitter, 'linkedin': linkedIn,'testMode': testMode }

    menu = {} # main menu
    menu['1']="Reset and fill in fields"
    menu['2']="Add field"
    menu['3']="Del field"
    menu['4']='Edit item'
    menu['5']="Clear all data"
    menu['6']='Post'
    menu['7']='Change URL'
    menu['8']='View payload'
    menu['9']='Exit'

    # main loop
    while True:
        print("====================")

        # print main menu
        options=collections.OrderedDict(sorted(menu.items()))
        for key, value in options.items():
            print("%s: %s" % (key, value))
        selection=input("Please select menu option:")

        # Reset fields and fill them in again
        if selection == '1':
            fields =collections.OrderedDict(sorted(payload.items()))
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
                payload[key] = entry

            input("Payload updated. Press enter to continue.")

        # Add a new field, only string fields can be added
        if selection == '2':
            newKey = input("Please enter the key of the new field: ")

            if newKey in payload:
                print("Field already exists. Returning to main menu.")
                continue

            newValue = input("Please enter the value of the new field: ")
            payload[newKey] = newValue

            input("New field added. Press enter to continue.")

        # Delete a field
        if selection == '3':
            # Check if payload has no fields
            if is_empty(payload):
                print("Nothing to delete.")
                continue

            # get field to delete
            delKey= input("Enter the field to delete: ")

            # delete field
            if delKey in payload:
                payload.pop(delKey)
                input("Payload updated. Press enter to continue.")
            else:
                input("Field not found. Press enter to continue")

        # Edit an item
        if selection == '4':
            # Check if payload has no fields
            if is_empty(payload):
                print("Nothing to edit.")
                continue

            # get user input
            editKey = input("Select field to edit: ")

            # edit field
            if editKey in payload:
                # editing testMode booleans
                if editKey == 'testMode':
                    entry = ""
                    while not (entry == 'true' or entry == 'false'):
                        entry = input("Set new value (true/false): ").lower()
                    if entry == 'true':
                        payload[editKey] = True
                    else:
                        payload[editKey] = False
                # everything else
                else:
                    payload[editKey] = input("Set new value: ")
                    input("Field updated. Press enter to continue.")
            else:
                input("Field not found. Press enter to continue")

        # Clear data
        if selection == '5':
            for key in payload:
                payload[key] = ""

                if key == 'testMode':
                    payload[key] = True

            input("Data cleared. Press enter to continue")

        # Post
        if selection == '6':
            # Check if payload has no fields
            if is_empty(payload):
                print("Nothing to post.")
                continue

            view_payload(url, payload) # print current payload
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
                    curr_payload = get_current_payload(payload)
                    r = req.post(url, data=curr_payload)

                    # print response
                    print("Payload header:\n ", r.headers)
                    print("Payload status:\n ",r.status_code)
                    r.raise_for_status()
                    input("Posted to:" + url + ". Press enter to continue.")
                # catch HTTPError
                except req.HTTPError as e:
                    print("HTTPError:", e)
                    input('Press enter to continue.')

        #  Change URL
        if selection == '7':
            entry = ""
            while entry == "":
                entry = input('Please enter the new URL: ')

            url = entry
            input('URL updated. Press enter to continue.')

        # view payload
        if selection == '8':
            if is_empty(payload):
                print("Nothing to view.")
                continue
            view_payload(url, payload)
            input("Press enter to continue.")

        # Exit program
        if selection == '9':
            print("Goodbye!")
            exit()

if __name__ == '__main__':
    driver_m()
