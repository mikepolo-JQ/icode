from db import DB


help_string = """
\tList of commands:

?\t\tGet list of commands
create\t\tCreate tables student, rooms and student_room for m2m rel
drop\t\tDrop all tables
insert\t\tEnter data from json file to the database
end\t\tExit from Program
clear\t\tClear the terminal

view\t\tViewing of Data
add\t\tAdding Data
delete\t\tDelete Data
"""


def print_command_list(_x):
    print(help_string)
    return True


def clear(_x):
    import os
    os.system('clear||cls')
    return True


command_dict = {
    'create': DB.create_table,
    'drop': DB.drop_table,
    'end': lambda _x: False,
    'insert': DB.insert_data,
    'clear': clear,
    '?': print_command_list,

    "view": DB.viewing_data,
    "add": DB.adding_data,
}


try:
    # Connect to the database
    db_helper = DB()

    try:
        print('Welcome! Enter "?" to see the list of available commands.')
        while True:

            command = input("\nicode >>> ").lower()

            try:
                handler = command_dict[command]
            except KeyError as ex:
                print("Bed request! Try '?' for see command list.")
                continue

            result = handler(db_helper)

            if not result:
                print('Bye!')
                break

    finally:
        db_helper.__disconnect__()

except Exception as ex:
    print("Connection refused..")
    print('Exception:\n', ex)
