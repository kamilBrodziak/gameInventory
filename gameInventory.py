# This is the file where you must work. Write code in the functions, create new functions,
# so they work according to the specification

# Displays the inventory.


def display_inventory(inventory):
    print("Inventory:")
    total_amount = 0
    for element in inventory:
        print(str(inventory[element]) + " " + element)
        total_amount += inventory[element]
    print("Total number of items: " + str(total_amount))
    pass


# Adds to the inventory dictionary a list of items from added_items.
def add_to_inventory(inventory, added_items):
    for item in added_items:
        try:
            inventory[item] += 1
        except KeyError:
            inventory[item] = 1
    pass


# Takes your inventory and displays it in a well-organized table with
# each column right-justified. The input argument is an order parameter (string)
# which works as the following:
# - None (by default) means the table is unordered
# - "count,desc" means the table is ordered by count (of items in the inventory)
#   in descending order
# - "count,asc" means the table is ordered by count in ascending order
def count_length_and_items_number(word, inv, amount_or_item):
    length = len(word)
    items_number = 0
    for one_tuple in inv:
        x = len(str(one_tuple[amount_or_item]))
        if x > length:
            length = x
        items_number += one_tuple[1]
    return length, items_number


def print_only_table(max_length_count, max_length_item,
                     tuples_list_inv, items_number):
    print("Inventory: \n")
    table_head = (max_length_count - len("count")) * " " + "count" + \
        4 * " " + (max_length_item - len("item name")) * " " + "item name"
    print(table_head)
    print(len(table_head) * "-")
    for i in range(len(tuples_list_inv)):
        print((max_length_count - len(str(tuples_list_inv[i][1]))) * " " + str(tuples_list_inv[i][1]) + 4 * " " +
              (max_length_item - len(tuples_list_inv[i][0])) * " " + tuples_list_inv[i][0])
    print(len(table_head) * "-")
    print("Total numbers of items: " + str(items_number))


def change_dict_into_list_of_tuples(inventory):
    tuples_list_inv = []
    for item in inventory:
        one_tuple = (item, inventory[item])
        tuples_list_inv.append(one_tuple)
    return tuples_list_inv


def print_table(inventory, order=None):
    items_number = 0
    if order is not None:
        is_reversed = True if order == "count,desc" else False
        tuples_list_inv = sorted(
            inventory.items(),
            key=lambda x: x[1],
            reverse=is_reversed)
        max_length_count = len(tuples_list_inv[0][0]) if is_reversed else len(
            str(tuples_list_inv[len(tuples_list_inv) - 1][1]))
        if len("count") > max_length_count:
            max_length_count = len("count")
        max_length_item, items_number = count_length_and_items_number(
            "item name", tuples_list_inv, 0)
    else:
        tuples_list_inv = change_dict_into_list_of_tuples(inventory)
        max_length_count, items_number = count_length_and_items_number(
            "count", tuples_list_inv, 1)
        max_length_item, items_number = count_length_and_items_number(
            "item name", tuples_list_inv, 0)
    print_only_table(
        max_length_count,
        max_length_item,
        tuples_list_inv,
        items_number)
    pass


# Imports new inventory items from a file
# The filename comes as an argument, but by default it's
# "import_inventory.csv". The import automatically merges items by name.
# The file format is plain text with comma separated values (CSV).
def import_inventory(inventory, filename="import_inventory.csv"):
    with open(filename, 'r') as invfile:
        temp_invent_string = invfile.read()[:-1]
    inventory_list = temp_invent_string.split(",")
    add_to_inventory(inventory, inventory_list)
    pass


# Exports the inventory into a .csv file.
# if the filename argument is None it creates and overwrites a file
# called "export_inventory.csv". The file format is the same plain text
# with comma separated values (CSV).
def convert_dict_into_string(inventory):
    string = ""
    for element in inventory:
        amount = inventory[element]
        while amount > 0:
            string += element + ","
            amount -= 1
    return string[:-1]


def export_inventory(inventory, filename="export_inventory.csv"):
    export_string = convert_dict_into_string(inventory)
    with open(filename, 'w') as invexport:
        invexport.write(export_string)
    pass
