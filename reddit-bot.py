import praw
import os
import string

import time
from RMPWebScraper import RateMyProfWebScraper
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
    
    subreddit = reddit.subreddit("testingground4bots")
    keyphrase = "!prof"
    
    course_list = get_course_data()
    
    for submission in subreddit.stream.submissions():             
        
        b = set()
        for course in course_list:
            course_name = course.subject + " " + course.number
            if len(course.instructor) != 0:            
                instructor = course.instructor         
            else :
                continue
            if (course_name, instructor) not in b:
                b.add((course_name, instructor)) 
            else :
                continue
            #print(course_check)
            if course_name in submission.selftext:
                for comment in submission.comments:  
                        if keyphrase in comment.body:
                            # TODO: Check all the professors from the set with the same course and suggest 
                            # the professor with the best rating
                            
                            print(instructor)
                            scraper = RateMyProfWebScraper(1112, instructor, "University Of Illinois at Urbana-Champaign")
                            scraper.retrieveRMPInfo()
                            prof_rating = scraper.getRMPInfo()
                            if prof_rating[0] == "T":                     
                                comment.reply(f"The professor teaching {course_name} is {instructor}."
                                              + f"\nHe/She doesn't exist in the RMP directory ")
                                continue
                            percent_taking_again = scraper.getTakeAgain()
                            difficulty = scraper.getDifficulty()
                            comment.reply(f"Take {course_name} with {instructor}."
                            + f"\n{instructor}'s rating is {prof_rating}."
                            + f"\n The course difficulty is {difficulty}"
                            + f"\n{percent_taking_again} of students would take this class again!")                                                   
                        
                   

if __name__ == '__main__':
    main()