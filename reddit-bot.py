import praw
import os
import time
import RMPScraperTool
import Courses

# Using .env file to read environmental variables
from dotenv import load_dotenv
load_dotenv()

# TODO: initialize the reddit bot
def main():
    print("Ce")
    reddit = praw.Reddit(client_id = "4Fmc8A0V4diHiw", 
                         client_secret = "qAMunNBhqkNGGWMuz57Z7GA3K6E",
                         username = "HackThisBot",
                         password = "shadowaaries1752",
                         user_agent = "RedditProfessor")
    
    subreddit = reddit.subreddit("UIUC")
    keyphrase = "!prof"
    
    course_list = Courses.load_data( "2020-fa.csv")
    for submission in subreddit.stream.submissions():             
        
        b = set()
        for course in course_list:
            
            course_check = course.subject + " " + course.number
            instructor = course.instructor
            
            if (course_check, instructor) not in b:
                b.add((course_check, instructor)) 
            else :
                continue
            #print(course_check)
            if course_check in submission.selftext:
                for comment in submission.comments:           
                    try :
                        if keyphrase in comment.body:                                   
                            comment.reply(f"Take this class {course_check} with {instructor} ")
                            print("Sd")
                    except :
                        print("triedd")
    return

"""
if __name__ == '__initializeBot__':
    initializeBot() 
"""


if __name__ == '__main__':
    main()