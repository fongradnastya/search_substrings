import argparse
from colorama import init, Back, Style
from search import search


def main():
    command = ""
    string = None
    keywords = None
    parser = argparse.ArgumentParser(description="collection of parameters")
    while command != "5":
        print_menu()
        command = input("Your command: ")
        if command == "1":
            string = input_text()
        elif command == "2":
            keywords = input_keywords()
            print(keywords)
        elif command == "3" or command == "4":
            string = get_string(string)
            is_correct = False
            if string:
                keywords = get_keys(keywords)
                if keywords:
                    if command == "3":
                        answer = search(string, keywords)
                    else:
                        answer = advanced_search(string, keywords)
                    print_text(string, answer, keywords)
                    is_correct = True
            if not is_correct:
                print("Impossible to search data")
        else:
            print("Wrong command")


def check_status(string, keywords):
    string = get_string(string)
    if not string:
        return False
    keywords = get_keys(keywords)
    if not keywords:
        return False
    return True


def get_string(string):
    if not string:
        print("Search string has not been added yet")
        answer = input("Do you want to add it now, (yes/no): ")
        if answer == "yes":
            string = input_text()
        else:
            if answer != "no":
                print("Incorrect answer")
            return None
    return string


def get_keys(keys):
    if not keys:
        print("Key words have not been added yet")
        answer = input("Do you want to add it now, (yes/no): ")
        if answer == "yes":
            keys = input_keywords()
        else:
            if answer != "no":
                print("Incorrect answer")
            return None
    return keys


def print_menu():
    print("------------------------MENU------------------------")
    print("1 - input a text")
    print("2 - add keywords")
    print("3 - default search keywords in the text")
    print("4 - advanced search keywords in the text")
    print("5 - exit")
    print("----------------------------------------------------")


def input_text():
    print("-----------------------INPUT-----------------------")
    print("1 - input from file")
    print("2 - input from console")
    print("3 - exit")
    print("---------------------------------------------------")
    command = input("Your command: ")
    strings = ""
    if command == "2":
        for i in range(10):
            string = input("Enter string or 'quit': ")
            if string == "quit":
                break
            else:
                strings += string
        return strings
    elif command != "3":
        print("Wrong command")


def input_keywords():
    keywords = []
    keyword = ""
    while keyword != "quit":
        keyword = input("Print keyword or 'quit': ")
        if keyword == "quit":
            break
        elif keyword in keywords:
            print("This keyword is already added")
        else:
            keywords.append(keyword)
    if not keywords:
        return None
    elif len(keywords) == 1:
        return keywords[0]
    return tuple(keywords)


def advanced_search(string, keywords):
    case_sensitivity = input("Case sensitivity (True/False): ")
    while case_sensitivity not in ("True", "False"):
        print("Wrong value, please, try again")
        case_sensitivity = input("Case sensitivity (True/False): ")
    if case_sensitivity == "True":
        case_sensitivity = True
    else:
        case_sensitivity = False
    method = input("Search method (first/last): ")
    while method not in ("first", "last"):
        print("Wrong value, please, try again")
        method = input("Search method (first/last): ")
    is_correct = False
    count = 0
    while not is_correct:
        count = input("Number of searched substrings: ")
        if not count.isnumeric():
            print("Value should be numeric")
        elif int(count) < 1:
            print("Value should be positive")
        else:
            is_correct = True
            count = int(count)
    return search(string, keywords, case_sensitivity, method, count)


def print_text(string, found, key):
    init()
    colors = (
        Back.BLACK,
        Back.RED,
        Back.BLUE,
        Back.CYAN,
        Back.GREEN,
        Back.MAGENTA,
        Back.YELLOW,
    )
    counter = 0
    for i, char in enumerate(string):
        if i in found:
            print(colors[counter] + char, end="")
        else:
            for f in found:
                if (i > f) and (i < f + len(key)):
                    print(colors[counter] + char, end="")
                    break
                elif i == f + len(key):
                    counter += 1
                    print(Back.RESET + char, end="")
                    break
                else:
                    print(Back.RESET + char, end="")
        if counter >= len(colors):
            counter = 0
    print(Back.RESET)


def print_one_key():
    pass


def print_many_keys():
    pass


main()
