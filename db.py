import json
import time
from typing import Union, Tuple

import psycopg2
import conf as settings

sql_queries = {
    'create_subject': "create table subject("
                      "id serial primary key,"
                      "name varchar(50) not null"
                      ");",

    'create_teacher': "create table teacher("
                      "id serial primary key,"
                      "full_name varchar(100) not null,"
                      "subject_id serial references subject(id)"
                      ");",

    "create_groups": "create table groups("
                     "id serial primary key,"
                     "name varchar(20) not null"
                     ");",

    "create_student": "create table student("
                      "id serial primary key,"
                      "full_name varchar(100) not null,"

                      "group_id serial references groups(id) not null"
                      ");",

    "create_subject_groups": "create table subject_groups("
                             "id serial primary key,"
                             "subject_id serial references subject(id),"
                             "group_id serial references groups(id)"
                             ");"
}


def view_result(file_name: str, data: Union[dict, list], total_time: str) -> None:
    with open(f'task_4/{file_name}.json', 'w') as result_file:
        json.dump(data, result_file)

    print(f'Result in {file_name}.json\nTotal time: {total_time}')


class DB:
    def __init__(self):
        # Connect to the database
        connection = psycopg2.connect(host=settings.HOST,
                                      port=settings.PORT,
                                      user=settings.USERNAME,
                                      password=settings.PASSWORD,
                                      database=settings.DATABASE_NAME)

        self.connection = connection
        self.tables_names = ['subject', 'teacher', 'groups', 'student', "subject_groups"]
        print("Successfully connected...")

    def __disconnect__(self):
        self.connection.close()
        print('Connection close...')

    def __execute_and_commit(self, sql_query: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query)
            self.connection.commit()

    def __fetchall(self, sql_query: str) -> Tuple[Union[dict, list], str]:
        with self.connection.cursor() as cursor:
            start = time.time()

            cursor.execute(sql_query)
            rows = cursor.fetchall()

            finish = time.time()
            return rows, f'{finish - start:.2f}'

    # CREATE tables
    def create_table(self) -> bool:
        # if not tables_names:
        tables_names = self.tables_names

        for table_name in tables_names:
            sql_query = sql_queries[f'create_{table_name}']
            self.__execute_and_commit(sql_query)

            print(f"Table {table_name} created successfully")

        return True

    # DROP tables
    def drop_table(self) -> bool:

        print("Are u sure u want to delete all tables from the DB? (Yes/No)\n")

        while True:
            check = input(" > ")
            if check in ["Yes", "y", "Y", "yes"]:
                # if not tables_names:
                tables_names = self.tables_names

                for table_name in tables_names:
                    self.__execute_and_commit(f"DROP TABLE {table_name} CASCADE;")
                    print(f"Table {table_name} drop successfully")

                return True

            elif check == "No":
                return True

    def insert_data(self) -> bool:
        self.insert_from_json(table_name="groups")
        self.insert_from_json(table_name="student")

        self.insert_from_json(table_name="subject")
        self.insert_from_json(table_name="teacher")
        return True

    # INSERT data from JSON FILE to the DataBase
    def insert_from_json(self, table_name) -> None:

        insert_settings_data_dict = {
            "student": {
                "file_name": "students2.json",
                "file_field_list": ["name", "group"],
                "value_string": "('{}', {})",
                "db_field_string": "student(full_name, group_id)"
            },
            "groups": {
                "file_name": "groups.json",
                "file_field_list": ["id", "name"],
                "value_string": "({}, '{}')",
                "db_field_string": "groups(id, name)"
            },
            "subject": {
                "file_name": "subjects.json",
                "file_field_list": ["id", "name"],
                "value_string": "({}, '{}')",
                "db_field_string": "subject(id, name)"
            },
            "teacher": {
                "file_name": "teachers.json",
                "file_field_list": ["id", "name", "subject"],
                "value_string": "({}, '{}', {})",
                "db_field_string": "teacher(id, full_name, subject_id)"
            },
        }

        conf = insert_settings_data_dict[table_name]

        with open(conf["file_name"]) as file:
            data = json.load(file)

        values = str()

        start = time.time()

        for someone in data:
            values += conf["value_string"].format(*list(someone[field_name] for field_name in conf["file_field_list"]))

            if someone['id'] != data[-1]['id']:
                values += ', '

        self.__execute_and_commit(f"insert into {conf['db_field_string']} values " + values + ';')

        finish = time.time()
        print(f"Insert {table_name} successfully! Total time: {finish - start:.2f}")
