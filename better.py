import os
import sys
from gameInventory import *


def cls():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def getChar(bits):
    try:
        import msvcrt
        return msvcrt.getch()
    except ImportError:
        import tty
        import sys
        import termios
        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            answer = sys.stdin.read(bits)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
        return answer


def print_item_in_inventory(tuples_list_inv, pos_start, x):
    with open("inventory_item" + str(x) + ".txt", 'r') as inv_item:
        string_repr = inv_item.read()
    name = tuples_list_inv[pos_start][0]
    amount = str(tuples_list_inv[pos_start][1])
    x, y = choose_number_of_chars(name)
    string_repr = string_repr.replace("var1" + x * " ", name + y * " ")
    x, y = choose_number_of_chars(amount)
    string_repr = string_repr.replace("var2" + x * " ", amount + y * " ")
    print(string_repr[:-1])


def print_table_footer(which_page, max_page, items_number):
    from math import ceil, floor
    print("|" + 61*"_" + "|")
    print("|" + 26 * " " + (3 - len(which_page)) * " " + which_page + " / " +
          max_page + (3 - len(max_page)) * " " + 26 * " " + "|")
    total_amount = "Total amount of items: " + str(items_number)
    print("|" + floor((61 - len(total_amount)) / 2) * " " +
          total_amount + ceil((61 - len(total_amount)) / 2) * " " + "|")
    print("|" + 61*"_" + "|")


def print_inventory(tuples_list_inv, items_number, pos, pos_start, pos_end):
    from math import ceil, floor
    cls()
    # print table head:
    with open("inventory.txt", 'r') as inventory_head:
        print(inventory_head.read()[:-1])
    # print item in inventory:
    while pos_start <= pos_end:
        x = 1 if pos_start == pos else 0  # 1 if item is chosen, 0 if not
        print_item_in_inventory(tuples_list_inv, pos_start, x)
        pos_start += 1
    # print page and total item number section:
    print_table_footer(str(ceil(pos_start / 5)), str(ceil(len(tuples_list_inv) / 5)), items_number)


def print_successful_screen():  # after importing/exporting inventory
    import time
    cls()
    print("\n\n\n\n\n\n\n\nSuccessful")
    time.sleep(2)


def print_menu(which_menu, option):
    cls()
    print("\n\n\n\n\n")
    with open(which_menu + str(option) + '.txt', 'r') as option:
        print(option.read())


def choose_number_of_chars(string):  # these numbers are neccessary to format table by length of string
    x = y = 0
    z = len(string)
    if z > 4:
        x = z - 4
    elif z < 4:
        y = 4 - z
    return x, y


def change_order(order, tuples_list_inv):
    is_reversed = True if order == "count,desc" else False
    tuples_list_inv = sorted(
        tuples_list_inv,
        key=lambda x: x[1],
        reverse=is_reversed)
    return tuples_list_inv


def change_option_to_inventory(tuples_list_inv):
    items_number = 0
    max_length = 0
    max_length_count, items_number = count_length_and_items_number(
        "count", tuples_list_inv, 1)
    max_length_item, items_number = count_length_and_items_number(
        "item name", tuples_list_inv, 0)
    max_length = max_length_item if max_length_item > max_length_count else max_length_count
    move_in_inventory(tuples_list_inv, max_length, items_number)


def move_in_inventory(tuples_list_inv, max_length, items_number):
    cls()
    last_item_id = len(tuples_list_inv) - 1
    pos_start = 0
    pos_end = 4 if last_item_id > 4 else last_item_id
    pos = 0
    while True:
        print_inventory(tuples_list_inv, items_number, pos, pos_start, pos_end)
        x = getChar(1)
        if x == '\x1b':
            x = getChar(2)
            if x == '[A' and pos > pos_start:  # move up
                pos -= 1
            elif x == '[B' and pos < pos_end:  # move down
                pos += 1
            elif x == '[D' and pos_start - 5 >= 0:  # move page left
                pos_start -= 5
                pos_end = pos_end - 5 if pos_end - 5 > 4 else 4
                pos = pos_start
            elif x == '[C' and pos_start + 5 <= last_item_id:  # move page right
                pos_start += 5
                pos = pos_start
                pos_end = pos_end + 5 if pos_end + 5 <= last_item_id else last_item_id
        elif x == '[':  # change ordering to descending
            tuples_list_inv = change_order("count,desc", tuples_list_inv)
        elif x == ']':  # change ordering to ascending
            tuples_list_inv = change_order("count,asc", tuples_list_inv)
        elif x == 'i' or x == 'I':
            break


def arrows_up_down(lower, option):  # moving in menu
    x = getChar(2)
    if x == '[A':
        if option > 0:
            option -= 1
    elif x == '[B':
        if option < lower:
            option += 1
    return option


def add_items_to_inventory(inv):
    cls()
    print("\n\n\n\n\n\n\n\n" + "What do you want to add?")
    items_list = input("Write it in single line.\n" +
                       "If you want to add multiple things, write as in example: arrow, bone, arrow, arrow, gold\n" +
                       "If name is builded by multiple word, write it as in example: gold coin, arrow, siler bow\n"
                       + "If you don't want to add anything, don't write anything.\n").split(", ")
    if len(items_list) == 1 and (items_list[0] == " " or items_list[0] == ""):
        return
    add_to_inventory(inv, items_list)


def options(inv):  # second option in menu, print new inventory management options
    option = 0
    while True:
        print_menu('options', option)
        x = getChar(1)
        if x == '\x1b':
            option = arrows_up_down(3, option)
        elif x == '\n':
            if option == 0:
                add_items_to_inventory(inv)
            if option == 1:
                import_inventory(inv, "export_inventory.csv")
                print_successful_screen()
            if option == 2:
                export_inventory(inv, "export_inventory.csv")
                print_successful_screen()
            if option == 3:
                return


def menu(inv):
    option = 0
    while True:
        print_menu('menu', option)
        x = getChar(1)
        if x == '\x1b':
            option = arrows_up_down(2, option)
        elif x == '\n':
            if option == 0:
                change_option_to_inventory(change_dict_into_list_of_tuples(inv))
            if option == 1:
                options(inv)
            if option == 2:
                exit()


def main():
    menu({})


if __name__ == '__main__':
    main()
