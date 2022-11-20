import argparse
from search import search


def main():
    command = ""
    string = None
    keywords = None
    parser = argparse.ArgumentParser(description="collection of parameters")
    while command != "4":
        print_menu()
        command = input("Your command: ")
        if command == "1":
            string = input_text()
        elif command == "2":
            keywords = input_keywords()
            print(keywords)
        elif command == "3":
            string = get_string(string)
            is_correct = False
            if string:
                keywords = get_keys(keywords)
                if keywords:
                    answer = search(string, keywords)
                    print(answer)
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
    print("1 - input text")
    print("2 - add keywords")
    print("3 - search keywords in text")
    print("4 - exit")
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


main()
