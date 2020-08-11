import praw
import os
import time
from RMPScraperTool import RateMyProfWebScraper
import numpy
from Courses import get_course_data

# Using .env file to read environmental variables
from dotenv import load_dotenv
load_dotenv()

def main():
    print("Ce")
    reddit = praw.Reddit(client_id = "4Fmc8A0V4diHiw", 
                         client_secret = "qAMunNBhqkNGGWMuz57Z7GA3K6E",
                         username = "HackThisBot",
                         password = "shadowaaries1752",
                         user_agent = "RedditProfessor")
    
    subreddit = reddit.subreddit("UIUC")
    keyphrase = "!prof"
    
    course_list = get_course_data()
    
    for submission in subreddit.stream.submissions():             
        
        course_info_set = set()
        for course in course_list:
            
            course_type = course.subject + " " + course.number
            if course.instructor != '' or course.instructor !=' ':
                a = course.instructor.split(",")
            if (len(a) == 1 or a[0] == ''):
                continue
            
            instructor = a[0].strip() + " " + a[1].strip()           
            if (course_type, instructor) not in course_info_set:
                course_info_set.add((course_type, instructor))
            else :
                continue
            #print(course_type)
            if course_type in submission.selftext:
                for comment in submission.comments:           
               
                        if keyphrase in comment.body:
                            
                            # print("before")
                            rmp_info = RateMyProfWebScraper(
                                schoolId=1112, teacher=instructor, schoolName="University of Illinois")
                            rmp_info.retrieveRMPInfo()
                            prof_rating = rmp_info.getRMPRating()
                            percent_taking_again = rmp_info.getTakeAgainPercent() 
                            print(instructor)
                            # TODO: Limit showing the info to only one time
                            comment.reply(f"Take {course_type} with {instructor}."
                            + f"\n{instructor}'s rating is {prof_rating}."
                            + f"\n{percent_taking_again} of students would take this class again!")
                        
                   

"""
if __name__ == '__initializeBot__':
    initializeBot() 
"""


if __name__ == '__main__':
    main()
