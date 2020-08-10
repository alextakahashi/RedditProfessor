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
course_list = set()

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load courses
    
    if directory is None:
        directory = "2020-fa.csv"
    
    #removed f string replaced with normal string 
    with open(directory, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            subject = row["Subject"]
            number = row["Number"]
            name = row["Name"]
            description = row["Description"]
            instructor = row["Instructors"]

            # creating a course instance and appending it to the list
            course_list.add(Courses(subject, number, name, description, instructor))
    return course_list
# TODO: Do what is required with the course list
