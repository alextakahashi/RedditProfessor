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

    subreddit = reddit.subreddit("testingground4bots")
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
        print(f"The professor teaching {course} is {instructor}."
              + f"\nHe/She doesn't exist in the RMP directory ")
        return False

    reply = (f"Found a professor for {course} on RateMyProfessor for you!"
             + f"\n\n Instructor {instructor}'s rating is: {prof_rating}."
             + f"\n\n The course difficulty is: {difficulty}"
             + f"\n\n{percent_taking_again} of students would take this class again.")

    return reply


def main():
    subreddit, keyphrase = initialize_bot()

    replied_to = []  # List to store ID's of comments replied to by bot to stop re-replying.
    instructors_shown = []  # List to store professors whose ratings have already been commented for that class.

    course_list = get_course_data()

    for submission in subreddit.stream.submissions():

        b = set()
        for comment in submission.comments:
            if keyphrase in comment.body:
                # TODO: Check all the professors from the set with the same course and suggest
                # the professor with the best rating
                coursetitle = comment.body.replace(keyphrase, '')  # "!prof CS 173" becomes "CS 173"
                coursesubj = coursetitle.split()[0]  # "CS"
                coursenum = coursetitle.split()[1]  # "173"

                for course in course_list:
                    if course.subject == coursesubj and course.number == coursenum:  # Match "CS" and "173" with CSV
                        instructor = course.instructor
                        course_name = course.subject + " " + course.number

                        if (course_name, instructor) not in b:
                            b.add((course_name, instructor))

                            print(instructor)
                            if not comment.saved:
                                if (comment.id not in replied_to) and (instructor not in instructors_shown):
                                    if (bot_reply(course_name, instructor) == False):
                                        continue

                                    comment.reply(bot_reply(course_name, instructor))
                                    replied_to.append(comment.id)  # Adds comment ID in replied_to.
                                    # Adds instructor in list so that we don't stop at 1 comment if
                                    # there are multiple instructors on RMP for this same course.
                                    instructors_shown.append(instructor)
                                    comment.save()

                                    print('Bot replying to: ')  # prints bot reply info to log.
                                    print("Title: ", submission.title)
                                    print("Text: ", submission.selftext)
                                    print("Score: ", submission.score)
                                    print("---------------------------------")

                                    print()
                        instructors_shown = []


if __name__ == '__main__':
    main()
