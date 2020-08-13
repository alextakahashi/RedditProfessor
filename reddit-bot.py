import praw
import os
import string
import time
import numpy

from RMPWebScraper import RateMyProfWebScraper
from Courses import get_course_data

# Using .env file to read environmental variables
# from dotenv import load_dotenv

# load_dotenv()

SCHOOL = "University Of Illinois at Urbana-Champaign"


# Initializes the bot and returns the subreddit and the keyphrase used to call it
def initialize_bot():
    print("Start")
    reddit = praw.Reddit(client_id="4Fmc8A0V4diHiw",
                         client_secret="qAMunNBhqkNGGWMuz57Z7GA3K6E",
                         username="HackThisBot",
                         password="shadowaaries1752",
                         user_agent="RedditProfessor")

    subreddit = reddit.subreddit("bottest")
    keyphrase = "!prof "

    return subreddit, keyphrase


# Generates a reply from bot about course and professor information
def bot_reply(course, instructor):
    scraper = RateMyProfWebScraper(1112, instructor, SCHOOL)
    scraper.retrieve_rmp_info()

    prof_rating = scraper.get_rmp_info()
    percent_taking_again = scraper.get_take_again()
    difficulty = scraper.get_difficulty()

    if prof_rating[0] == "T":
        reply = (f"The professor teaching {course} is {instructor}."
                 + f"\nHe/She doesn't exist in the RMP directory ")
        return reply

    reply = (f"Found a professor for {course} on RateMyProfessor for you!"
             + f"\n\n Instructor {instructor}'s rating is: {prof_rating}."
             + f"\n\n The course difficulty is: {difficulty}"
             + f"\n\n{percent_taking_again} of students would take this class again.")

    return reply


def main():
    print("hjhhjhj")
    subreddit, keyphrase = initialize_bot()
    replied_to = []  # List to store ID's of comments replied to by bot to stop re-replying.
    instructors_shown = []  # List to store professors whose ratings have already been commented for that class.
    course_list = get_course_data()
    getFromComment(course_list, keyphrase)
    time.sleep(15)
    #getFromPost(course_list, keyphrase)
    

def getFromComment(course_list, keyphrase):
    
    subreddit, keyphrase = initialize_bot()
    for comment in subreddit.stream.comments():
        b = set()
        if keyphrase in comment.body and len(comment.body) > 5:
            # TODO: Check all the professors from the set with the same course and suggest
            # the professor with the best rating
            checkForComment = True
            print("check for comment is true")
            print(comment.body)
            
            if len(comment.body) < 6 : 
                """                  
                if comment in comments_read_list:                    
                # comment.save()
                    comments_read_list.add(comment)              
                    getFromPost(course_list, keyphrase)
                    """
                continue        
            
            coursetitle = comment.body.replace(keyphrase, '')   # "!prof CS 173" becomes "CS 173"
            print(coursetitle.split())
            coursesubj = coursetitle.split()[0]     # "CS"
            coursenum = coursetitle.split()[1]      # "173"            
            print(coursetitle)
            for course in course_list:
                if course.subject == coursesubj and course.number == coursenum:
                    
                    if course.instructor != '' or course.instructor !=' ':            
                        instructor = course.instructor         
                    else :
                        continue
                    course_name = course.subject + " " + course.number
                    if (course_name, instructor) not in b:
                        b.add((course_name, instructor))
                        if not comment.saved:
                                print(course_name)
                                scraper = RateMyProfWebScraper(1112, instructor,
                                                            "University Of Illinois at Urbana-Champaign")
                                scraper.retrieve_rmp_info()
                                prof_rating = scraper.get_rmp_info()
                                if prof_rating[0] == "T":
                                    comment.reply(f"The professor teaching {course_name} is {instructor}."
                                        + f"\nHe/She doesn't exist in the RMP directory ")                                   
                                    comment.save()
                                    continue
                                percent_taking_again = scraper.get_take_again()
                                difficulty = scraper.get_difficulty()
                                comment.reply(f"Take {course_name} with {instructor}."
                                            + f"\n\n{instructor}'s rating is: {prof_rating}."
                                            + f"\n\n The course difficulty is: {difficulty}"
                                            + f"\n\n{percent_taking_again} of students would take this class again.")
                                 # Adds comment ID in replied_to to prevent re-replying
                                # Adds instructor in list so that we don't stop at 1 comment if there are
                                # multiple instructors on CSV for this same course.
                                comment.save()
                                print('Bot replying to: ')  # prints to console for our information

                                print("Title: ",comment.body)

                                print("---------------------------------")

                                print()
                    instructors_shown = []
                    
def getFromPost(course_list, keyphrase) :  
    
    
    subreddit, keyphrase = initialize_bot()
    comments_called = set()
    print("Second reached")
    for submission in subreddit.stream.submissions():             
        b = set()
        for course in course_list:            
            course_check = course.subject + " " + course.number
            if course.instructor != '' or course.instructor !=' ':            
                instructor = course.instructor         
            else :
                continue
            if (course_check, instructor) not in b:
                b.add((course_check, instructor)) 
            else :
                continue
            #print(course_check)
            if course_check in submission.selftext:
                for comment in submission.comments:                  
                    if comment in comments_called :
                        continue
                    comments_called.add(comment.body)                                       
                    bot_reply(course, instructor)
    
    


if __name__ == '__main__':    
    while True:
        main()
