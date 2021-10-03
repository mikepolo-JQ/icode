import json

# data = ["Algebra",
#         "Art",
#         "Biology",
#         "Chemistry",
#         "Computer science",
#         "English",
#         "Foreign language",
#         "Geography",
#         "Geometry",
#         "Health",
#         "History",
#         "Literature",
#         "Mathematics",
#         "Music",
#         "Pe",
#         "Physics",
#         "Psychology",
#         "Reading",
#         "Science",
#         "Social studies"
#         ]
#
# file_data = []
# i = 0
#
# for subject in data:
#     i += 1
#     file_data += [{
#         "id": i,
#         "name": subject
#     }]
#
#
# with open("subjects.json", 'w') as file:
#     json.dump(file_data, file, indent=4)


# with open('students.json') as file:
#     student_data = json.load(file)
#
# student_file = []
# teacher_file = []
#
# i = 0
# subject_id = 0
# for student in student_data:
#     if student['group'] <= 25:
#         continue
#
#     # i += 1
#     # student_file += [{
#     #     "id": i,
#     #     "name": student["name"],
#     #     "group": student["group"],
#     # }]
#     i += 1
#     subject_id += 1
#     teacher_file += [{
#         "id": i,
#         "name": student['name'],
#         "subject": subject_id
#     }]
#
#     if subject_id >= 20:
#         subject_id = 0
#
#     if i >= 50:
#         break
#
#
# # with open("students2.json", 'w') as file:
# #     json.dump(student_file, file, indent=4)
#
# with open("teacher.json", 'w') as file:
#     json.dump(teacher_file, file, indent=4)


# with open('groups.json') as file:
#     groups_data = json.load(file)

i = 0
groups_file = []
k = 0
idk = 0
for group_id in range(25):
    for subject_id in range(5):
        groups_file += [{
            "id": idk + 1,
            "group": group_id + 1,
            "subject": subject_id + 1 + k,
        }]
        idk += 1

    k += 5
    if k >= 20:
        k = 0

# with open("students2.json", 'w') as file:
#     json.dump(student_file, file, indent=4)

with open("subject_groups.json", 'w') as file:
    json.dump(groups_file, file, indent=4)
