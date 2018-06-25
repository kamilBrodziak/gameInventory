def count_length_and_items_number(word, inv, amount_or_item):
    length = len(word)
    items_number = 0
    for one_tuple in inv:
        x = len(str(one_tuple[amount_or_item]))
        if x > length:
            length = x
        items_number += one_tuple[1]
    return length, items_number

def print_only_table(max_length_count, max_length_item, tuples_list_inv, items_number):
    print("Inventory: \n")
    table_head =(max_length_count - len("count")) * " " + "count" + 4 * " " + (max_length_item - len("item name")) * " " + "item name" 
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

def print_table(inventory, order):
    items_number = 0
    if order != "":
        is_reversed = True if order == "count,desc" else False
        tuples_list_inv = sorted(inventory.items(), key = lambda x: x[1], reverse=is_reversed)
        max_length_count = len(tuples_list_inv[0][0]) if is_reversed == True else len(str(tuples_list_inv[len(tuples_list_inv)-1][1]))
        if len("count") > max_length_count:
            max_length_count = len("count")
        max_length_item, items_number = count_length_and_items_number("item name", tuples_list_inv, 0)
    else:
        tuples_list_inv = change_dict_into_list_of_tuples(inventory)
        max_length_count, items_number = count_length_and_items_number("count", tuples_list_inv, 1)
        max_length_item, items_number = count_length_and_items_number("item name", tuples_list_inv, 0)
    print_only_table(max_length_count, max_length_item, tuples_list_inv, items_number)


def import_inventory(inventory, filename):
    try:
        invfile = open(filename, 'r')
    except FileNotFoundError:
        invfile = open("import_inventory.csv", 'r')
    temp_invent_string = invfile.read()
    print(temp_invent_string)
    inventory_list = temp_invent_string.split(",")
    print(inventory_list)
    invfile.close()
    add_to_inventory(inventory, inventory_list)

def add_to_inventory(inventory, added_items):
    for item in added_items:
        try:
            inventory[item] += 1
        except KeyError:
            inventory[item] = 1

def convert_dict_into_string(inventory):
    string = ""
    for element in inventory:
        amount = inventory[element]
        while amount > 0:
            string += element + ","
            amount-=1
    return string

def export_inventory(inventory, filename):
    if filename == "":
        filename = "export_inventory.csv"
    export_string = convert_dict_into_string(inventory)
    with open(filename, 'w') as invexport:
        invexport.write(export_string) 


inv = {'rope': 1, 'torch': 6, 'gold coin': 42, 'dagger': 1, 'arrow': 12}
dragon_loot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
import_inventory(inv, "fx")
add_to_inventory(inv, dragon_loot)
export_inventory(inv,"")
print_table(inv, "count,desc")
add_to_inventory(inv, dragon_loot)