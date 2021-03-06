import json
import time
from typing import Union, Tuple
from prettytable import PrettyTable

import psycopg2
import conf as settings
import utils

sql_queries = {
    'create_subject': "create table subject("
                      "id serial primary key,"
                      "name varchar(50) not null"
                      ");",

    'create_teacher': "create table teacher("
                      "id serial primary key,"
                      "full_name varchar(100) not null,"
                      "subject_id serial references subject(id) on delete cascade"
                      ");",

    "create_groups": "create table groups("
                     "id serial primary key,"
                     "name varchar(20) not null"
                     ");",

    "create_student": "create table student("
                      "id serial primary key,"
                      "full_name varchar(100) not null,"

                      "group_id serial references groups(id) on delete cascade "
                      ");",

    "create_groups_subject": "create table groups_subject("
                             "id serial primary key,"
                             "subject_id serial references subject(id) on delete cascade,"
                             "group_id serial references groups(id) on delete cascade"
                             ");",

    "viewing_student": "select s.id as id, s.full_name, g.name from student s left join groups g on g.id = s.group_id;",

    "viewing_groups": "select g.id, g.name, count(s.id) from groups g left join student s on g.id = s.group_id group "
                      "by g.id order by g.id",

    "viewing_subject": "select s.id, s.name, array_to_string(array_agg(t.full_name), ', ') from subject s left join "
                       "teacher t on s.id = t.subject_id group by s.id order by s.id;",

    "viewing_teacher": "select t.id, t.full_name, s.name from teacher t left join subject s on s.id = t.subject_id"
                       " order by t.id;",

    "viewing_groups_subject": "select g.id, g.name, array_to_string(array_agg(s.name), ', ') from groups g left join"
                              " groups_subject sg on g.id = sg.group_id left join subject s on sg.subject_id = s.id"
                              " group by g.name, g.id;",

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
        self.tables_names = ['subject', 'teacher', 'groups', 'student', "groups_subject"]
        print("Successfully connected...")

    def __disconnect__(self):
        self.connection.close()
        print('Connection close...')

    def _execute_and_commit(self, sql_query: str) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query)
            self.connection.commit()

    def _fetchall(self, sql_query: str) -> Tuple[Union[dict, list], str]:
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
            self._execute_and_commit(sql_query)

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
                    self._execute_and_commit(f"DROP TABLE {table_name} CASCADE;")
                    print(f"Table {table_name} drop successfully")

                return True

            elif check == "No":
                return True

    def insert_data(self) -> bool:
        self.insert_from_json(table_name="groups")
        self.insert_from_json(table_name="student")

        self.insert_from_json(table_name="subject")
        self.insert_from_json(table_name="teacher")

        self.insert_from_json(table_name="groups_subject")
        return True

    # INSERT data from JSON FILE to the DataBase
    def insert_from_json(self, table_name: str) -> None:

        insert_settings_dict = {
            "student": {
                "file_name": "students.json",
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
            "groups_subject": {
                "file_name": "groups_subject.json",
                "file_field_list": ["id", "subject", "group"],
                "value_string": "({}, {}, {})",
                "db_field_string": "groups_subject(id, subject_id, group_id)"
            },
        }

        conf = insert_settings_dict[table_name]

        with open(f"jsons/{conf['file_name']}") as file:
            data = json.load(file)

        values = str()

        start = time.time()

        for someone in data:
            values += conf["value_string"].format(*list(someone[field_name] for field_name in conf["file_field_list"]))

            if someone['id'] != data[-1]['id']:
                values += ', '

        self._execute_and_commit(f"insert into {conf['db_field_string']} values " + values + ';')

        finish = time.time()
        print(f"Insert {table_name} successfully! Total time: {finish - start:.2f}")

    def viewing_data(self):
        print("\nEnter the name of the table, please\n")
        print("student\t\tLIST OF STUDENTS\ngroups\t\tLIST OF GROUPS\nsubject\t\tLIST OF SUBJECTS\n"
              "teacher\t\tLIST OF TEACHERS\ngroups_subject\tSUBJECT OF GROUPS")

        while True:
            table_name = input("\nicode/view >>> ").lower()
            if table_name in self.tables_names:
                _rows = self._view(table_name)
            elif table_name == "end":
                break
            else:
                print(f"Table with name \"{table_name}\" isn't found.\nTry again or enter \"end\" for exit")
        return True

    # VIEWING RECORDS
    def _view(self, table_name: str):

        viewing_settings_dict = {
            "student": {
                "title": "LIST OF STUDENTS",
                "field_names": ["id", "Student Full Name", "Group"]
            },
            "groups": {
                "title": "LIST OF GROUPS",
                "field_names": ["id", "Group", "Count of Students"]
            },
            "subject": {
                "title": "LIST OF SUBJECTS",
                "field_names": ["id", "Subject", "Teachers"]
            },
            "teacher": {
                "title": "LIST OF TEACHERS",
                "field_names": ["id", "Teacher Full Name", "Subject"],
            },
            "groups_subject": {
                "title": "SUBJECT OF GROUPS",
                "field_names": ["id", "Group", "Subjects"],
            },

        }

        sql_query = sql_queries[f'viewing_{table_name}']

        rows, tot_time = self._fetchall(sql_query)

        table = PrettyTable()

        conf = viewing_settings_dict[table_name]
        table.title = conf["title"]
        table.field_names = conf["field_names"]

        for row in rows:
            table.add_row(list(i for i in row))

        print(table)

        return rows

    def adding_data(self):
        print("\nEnter the name of the table, please\n")
        print("student\t\tADD STUDENTS\ngroups\t\tADD GROUP\nsubject\t\tADD SUBJECTS\n"
              "teacher\t\tADD TEACHERS\ngroups_subject\tADD SUBJECT FOR A GROUP")

        hendler_adding_dict = {
            "student": utils.student_adding,
            "groups": utils.group_adding,
            "subject": utils.subject_adding,
            "teacher": utils.teacher_adding,
            "groups_subject": utils.groups_subject_adding
        }

        while True:
            table_name = input("\nicode/add >>> ").lower()
            if table_name in self.tables_names:
                hendler_adding_dict[table_name](self)
            elif table_name == "end":
                break
            else:
                print(f"Table with name \"{table_name}\" isn't found.\nTry again or enter \"end\" for exit")
        return True

    def delete_data(self):
        print("\nEnter the name of the table, please\n")
        print("student\t\tDelete STUDENTS\ngroups\t\tDelete GROUP\nsubject\t\tDelete SUBJECTS\n"
              "teacher\t\tDelete TEACHERS\ngroups_subject\tDelete SUBJECT FOR A GROUP")

        while True:
            table_name = input("\nicode/delete >>> ").lower()
            if table_name in self.tables_names:
                utils.delete(self, table_name)
            elif table_name == "end":
                break
            else:
                print(f"Table with name \"{table_name}\" isn't found.\nTry again or enter \"end\" for exit")
        return True


