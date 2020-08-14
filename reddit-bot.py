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
replied_to = set()


# Initializes the bot and returns the subreddit and the keyphrase used to call it
def initialize_bot():
    print("Start")
    reddit = praw.Reddit(client_id="4Fmc8A0V4diHiw",
                         client_secret="qAMunNBhqkNGGWMuz57Z7GA3K6E",
                         username="HackThisBot",
                         password="shadowaaries1752",
                         user_agent="RedditProfessor")

    subreddit = reddit.subreddit("bottest")
    keyphrase = "!prof"

    return subreddit, keyphrase


# Generates a reply from bot about course and professor information
def bot_reply(course, instructor):
    scraper = RateMyProfWebScraper(1112, instructor, SCHOOL)
    scraper.retrieve_rmp_info()

    prof_rating = scraper.get_rmp_info()
    percent_taking_again = scraper.get_take_again()
    difficulty = scraper.get_difficulty()

    if prof_rating[0] == "T":
        if len(instructor) == 0 or len(instructor) == 1:
                instructor = "not decided yet"       
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
        
        if comment.id in replied_to:
            continue
        
        b = set()
        if keyphrase in comment.body and len(comment.body) >= len(keyphrase):
            # TODO: Check all the professors from the set with the same course and suggest
            # the professor with the best rating
            checkForComment = True
            print("check for comment is true")
            print(comment.body)
            
            if comment.body == keyphrase:
                if not comment.saved:                                 
                    post = comment.submission.selftext
                    course_load = set()
                    instructor_temp = ""
                    for course_temp in course_list: 
                        title = (course_temp.subject + " " +  course_temp.number)               
                        if (course_temp.subject + " " + course_temp.number) in post:                            
                            reply = bot_reply(title, course_temp.instructor) 
                            print(reply)
                            course_load.add(reply)                    
                    print(course_load)
                    for i in course_load:
                        comment.reply(i)                   
                    
                comment.save()
                replied_to.add(comment)               
                continue        
                
            coursetitle = comment.body.replace(keyphrase, '')   # "!prof CS 173" becomes "CS 173"
            print(coursetitle.split())
            try:
                coursesubj = coursetitle.split()[0]     # "CS"
                coursenum = coursetitle.split()[1] 
            except :
                comment.reply("Please put spaces between words")     # "173"            
            print(coursetitle)
            for course in course_list:
                if course.subject == coursesubj and course.number == coursenum:
                    
                    if course.instructor != '' or course.instructor !=' ':            
                        instructor = course.instructor         
                    else :
                        instructor = "unassigned"
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
                                    if len(instructor) == 0 or len(instructor) == 1:
                                        instructor = "not decided yet"                                    
                                    comment.reply(f"The professor for this {course_name} is {instructor}."
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
        replied_to.add(comment.id)     
                    
 

if __name__ == '__main__':    
    while True:
        main()