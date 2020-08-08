import csv
import sys

class Courses:

    def __init__(self, subject, number, name, description, instructor):
        self.subject= subject
        self.number = number
        self.name = name
        self.description = description
        self.instructor = instructor

# constains the list of courses and its associated attributes
course_list = []


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load courses
    with open(f"{directory}/2020-fa.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            subject = row["Subject"]
            number = row["Number"]
            name = row["Name"]
            description = row["Description"]
            instructor = row["Instructors"]

            # creating a course instance and appending it to the list
            course_list.append(Courses(subject, number, name, description, instructor))

# TODO: Do what is required with the course list
