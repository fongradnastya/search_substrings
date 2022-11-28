import argparse
import os
from colorama import init, Back, Fore, Style
from search import search
from typing import Union


def main() -> None:
    """
    Точка входа в приложение
    :return: None
    """
    value = started_parser()
    if not value:
        command = ""
        string = None
        keywords = None
        while command != "5":
            print_menu()
            command = input("Your command: ")
            if command == "1":
                string = input_text()
                print(string)
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


def started_parser() -> int:
    """
    Инициализация парсинга аргументов командной строки
    :return: 0 - если нет аргументов, 1 - если ошибка, 2 - если корректно
    """
    parser = argparse.ArgumentParser(description="collection of parameters")
    parser.add_argument("--str", type=str, help="searching string")
    parser.add_argument("--file", type=str, help="file")
    parser.add_argument("--substr", nargs='+', type=str, help="substrings for searching")
    parser.add_argument("--cases", type=bool, help="case sensitive",
                        default=True)
    parser.add_argument("--method", type=str, help="searching method",
                        default="first")
    parser.add_argument("--cnt", type=int, help="number of occurrences",
                        default=None)
    args = parser.parse_args()
    parse = parse_arguments(args)
    return parse


def parse_arguments(args) -> int:
    """
    Получение и проверка аргументов командной строки
    :param args: аргументы командной строки
    :return: 0 - если нет аргументов, 1 - если ошибка, 2 - если корректно
    """
    args_b = bool(args.str) + bool(args.file) + bool(args.substr)
    if not args_b:
        return 0
    if not (args.str or args.file):
        print("Please, enter strings (--str) or a file name (--file)")
        print("Nowhere to search in")
        return 1
    elif args.file:
        if os.path.exists(args.file):
            read_from_file(args.file)
        else:
            print("This filename is incorrect")
    if not args.substr:
        print("Please, enter keywords (--substr)")
        print("Nothing to search")
        return 1
    else:
        substr = args.substr
        if isinstance(args.substr, list):
            substr = tuple(args.substr)
        case_sensitivity = args.cases if args.cases in (True, False) else True
        method = args.method if args.method in ("first", "last") else "first"
        count = args.cnt if args.cnt and args.cnt > 0 else None
        answer = search(args.str, substr, case_sensitivity, method, count)
        print_text(args.str, answer, args.substr)
        return 2


def read_from_file(file_name=None) -> str:
    """
    Считывание строк из файла
    :param file_name: имя файла для открытия
    :return: считанная строка или None
    """
    while not file_name:
        file_name = input("Please, enter a file name (with extension): ")
        if not os.path.exists(file_name):
            print("This filename is incorrect. Please, try again")
            file_name = None
    string = ""
    counter = 0
    with open(file_name, "r", encoding='utf-8') as file:
        for line in file:
            string += line
            counter += 1
            if counter > 10:
                break
    if (not string) or (string == " "):
        print("Read string is empty")
        string = None
    else:
        string = ' '.join(string.split("\n"))
    return string


def get_string(string: str) -> str:
    """
    Считывание строки, если она ещё не была добавлена
    :param string: строка для поиска
    :return: считанная строка
    """
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


def get_keys(keys: Union[tuple, str, None]) -> Union[tuple, str, None]:
    """
    Считывание ключевых слов, если они ещё не были добавлены
    :param keys: ключевые слова
    :return: считанные ключевые слова
    """
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


def print_menu() -> None:
    """
    Вывод в консоль главного меню приложения
    :return: None
    """
    print("------------------------MENU------------------------")
    print("1 - input a text")
    print("2 - input keywords")
    print("3 - default search keywords in the text")
    print("4 - advanced search keywords in the text")
    print("5 - exit")
    print("----------------------------------------------------")


def input_text() -> Union[str, None]:
    """
    Считывание строк для поиска
    :return: считанные строки
    """
    print("-----------------------INPUT-----------------------")
    print("1 - input from file")
    print("2 - input from console")
    print("3 - exit")
    print("---------------------------------------------------")
    command = input("Your command: ")
    strings = ""
    if command == "1":
        string = read_from_file()
        return string
    elif command == "2":
        for i in range(10):
            string = input("Enter string or 'quit': ")
            if string == "quit":
                break
            else:
                strings += string
        return strings
    elif command != "3":
        print("Wrong command")


def input_keywords() -> Union[tuple, str, None]:
    """
    Считывание списка ключевых слов
    :return: список ключевых слов
    """
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


def advanced_search(string: str, keywords: Union[tuple, str, None]) -> \
        Union[tuple, dict, None]:
    """
    Поиск подстрок с расширенным набором параметров
    :param string: строка для поиска
    :param keywords: искомые ключевые слова
    :return: результат поиска
    """
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


def print_text(string: str, found: Union[tuple, dict, None],
               key: Union[tuple, str, None]) -> None:
    """
    Цветной вывод найденных подстрок в консоль
    :param string: строка для поиска
    :param found: индексы найденных ключевых слов
    :param key: ключевые слова
    :return: None
    """
    if not found:
        "There are no substrings founded here"
        print(string)
    else:
        if isinstance(found, tuple):
            found = create_one_key(found, key)
        else:
            found = create_many_keys(found)
        init()
        color_id = 0
        colors = (
            Style.BRIGHT + Fore.BLUE + Back.RED,
            Style.BRIGHT + Fore.CYAN + Back.YELLOW,
            Style.BRIGHT + Fore.YELLOW + Back.CYAN,
            Style.BRIGHT + Fore.MAGENTA + Back.GREEN,
            Style.BRIGHT + Fore.GREEN + Back.MAGENTA,
        )
        reset = Style.RESET_ALL + Fore.RESET + Back.RESET
        counter = 0
        for i, char in enumerate(string):
            if i in found[counter]:
                print(colors[color_id] + char, end="")
            elif counter + 1 < len(found) and i in found[counter + 1]:
                counter += 1
                if color_id + 1 == len(colors):
                    color_id = 0
                else:
                    color_id += 1
                print(colors[color_id] + char, end="")
            else:
                print(reset + char, end="")
        print(Back.RESET)


def create_one_key(found: Union[tuple, None], key: str) -> list:
    """
    Создание массива индексов для одного ключа
    :param found: индексы найденных ключевых слов
    :param key: название искомого ключа
    :return: массива индексов
    """
    ids = []
    for i in range(len(found)):
        ids.append([])
        for j in range(len(key)):
            ids[i].append(found[i] + j)
    return ids


def create_many_keys(found: Union[dict, None]) -> list:
    """
    Создание массива индексов для нескольких ключей
    :param found: индексы найденных ключевых слов
    :return: массива индексов
    """
    ids = []
    curr_id = -1
    for key, value in found.items():
        if value:
            for i in range(len(value)):
                ids.append([])
                curr_id += 1
                for j in range(len(key)):
                    ids[curr_id].append(value[i] + j)
    return sorted(ids)


if __name__ == "__main__":
    main()
