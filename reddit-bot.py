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
        
        b = set()
        for course in course_list:
            
            course_check = course.subject + " " + course.number
            if course.instructor != '' or course.instructor !=' ':
                a = course.instructor.split(",")
            if (len(a) == 1 or a[0] == ''):
                continue
            
            instructor = a[0].strip() + " " + a[1].strip()           
            if (course_check, instructor) not in b:
                b.add((course_check, instructor)) 
            else :
                continue
            #print(course_check)
            if course_check in submission.selftext:
                for comment in submission.comments:           
               
                        if keyphrase in comment.body:
                            # TODO: Check all the professors from the set with the same course and suggest 
                            # the professor with the best rating
                            
                            print("before")
                            aapi = RateMyProfWebScraper(schoolId=1112, teacher=instructor)
                            aapi.retrieveRMPInfo()
                            rating = aapi.getRMPInfo()                                                   
                            comment.reply(f"Class : {course_check}. Instructor RMP rating : {rating}")
                        
                   

"""
if __name__ == '__initializeBot__':
    initializeBot() 
"""


if __name__ == '__main__':
    main()