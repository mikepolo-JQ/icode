def student_adding(s) -> int:
    sql_query = "select max(id) from student;"
    rows, _tot_time = s._fetchall(sql_query)
    last_student_id = rows[0][0]

    while True:
        name = input("Enter the Student's name: ")
        if name:
            break

    print("\tChoose the group id")
    rows = s._view("groups")
    group_id_list = list()
    for row in rows:
        group_id_list.append(row[0])

    while True:
        try:
            inp = input("Enter the student's group or enter \"+\" to add new: ")

            if inp == '+':
                group_id = group_adding(s)
                break

            group_id = int(inp)
        except ValueError:
            print("Check the entered data. I need id!")
            continue

        if group_id in group_id_list and group_id > 0:
            break
        print("Check the entered data. I need id from list of groups above!")

    sql_query = f"insert into student(id, full_name, group_id) values ({last_student_id + 1}, '{name.title()}'," \
                f" {group_id}) returning id;"

    row, _tot_time = s._fetchall(sql_query)
    s.connection.commit()

    print("OK! Student added.")
    return row[0][0]


def group_adding(s) -> int:
    global group_number

    rows = s._view("groups")
    group_id_list = list()
    for row in rows:
        group_id_list.append(row[0])

    while True:
        try:
            group_number = int(input("Enter the group number: "))
        except ValueError:
            print("Check the entered data. I need digit!")
            continue
        if group_number not in group_id_list and group_number > 0:
            break
        print("Check the entered data. This number already exists!")

    name = f"Group #{group_number}"
    sql_query = f"insert into groups(id, name) values ({group_number}, '{name}')" \
                f" returning id;"

    row, _tot_time = s._fetchall(sql_query)
    s.connection.commit()

    print("OK! Group added.")
    return row[0][0]


def subject_adding(s) -> int:
    sql_query = "select max(id) from subject;"
    rows, _tot_time = s._fetchall(sql_query)
    last_subject_id = rows[0][0]

    rows = s._view("subject")
    subjects_names_list = list()
    for row in rows:
        subjects_names_list.append(row[1].lower())

    while True:
        subject_name = input("Enter the subject name: ").lower()

        if subject_name and subject_name not in subjects_names_list:
            break
        print("Check the entered data. This name already exists!")

    sql_query = f"insert into subject(id, name) values ({last_subject_id + 1}, '{subject_name.title()}')" \
                f" returning id;"

    row, _tot_time = s._fetchall(sql_query)
    s.connection.commit()

    print("OK! Subject added.")
    return row[0][0]


def teacher_adding(s) -> int:
    global subject_id
    sql_query = "select max(id) from teacher;"
    rows, _tot_time = s._fetchall(sql_query)
    last_teacher_id = rows[0][0]

    while True:
        name = input("Enter the full name of the Teacher: ")
        if name:
            break

    print("\tChoose the subject id")
    rows = s._view("subject")
    subject_id_list = list()
    for row in rows:
        subject_id_list.append(row[0])

    while True:
        try:
            inp = input("Enter the subject or enter \"+\" to add new: ")

            if inp == '+':
                subject_id = subject_adding(s)
                break

            subject_id = int(inp)
        except ValueError:
            print("Check the entered data. I need id!")
            continue

        if subject_id in subject_id_list and subject_id > 0:
            break
        print("Check the entered data. I need id from list of groups above!")

    sql_query = f"insert into teacher(id, full_name, subject_id) values ({last_teacher_id + 1}, '{name.title()}', " \
                f"{subject_id}) returning id;"

    row, _tot_time = s._fetchall(sql_query)
    s.connection.commit()

    print("OK! Teacher added.")
    return row[0][0]
