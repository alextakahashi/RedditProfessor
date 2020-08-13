import csv
import sys


class Courses:

    def __init__(self, subject, number, name, description, instructor):
        self.subject = subject
        self.number = number
        self.name = name
        self.description = description
        self.instructor = instructor


# Contains the list of courses and its associated attributes
course_list = set()


# Reads and stores the course data in a set
def load_course_data(directory):
    # Load data from CSV files into memory.

    # Load courses

    # Removed f string replaced with normal string 
    with open(directory, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            subject = row["Subject"]
            number = row["Number"]
            name = row["Name"]
            description = row["Description"]
            instructor = row["Instructors"]

            # Creating a course instance and adding it to the set
            course_list.add(Courses(subject, number, name, description, instructor))


# Returns the course data
def get_course_data():
    # This will have to be updated after every semester
    directory = input("Input your csv file with professors ")
    print(directory)
    if directory == '':
        directory = "course_data/2020-fa.csv"
    load_course_data(directory)
    return course_list
