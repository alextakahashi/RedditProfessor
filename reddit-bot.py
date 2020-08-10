import praw
import os
import time

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
    
    for comment in subreddit.stream.comments():
        try :
            if (keyphrase in comment.body) :
                comment.reply("yay")
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