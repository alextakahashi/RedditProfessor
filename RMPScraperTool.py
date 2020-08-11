import re, requests
from lxml import etree
import logging
from bs4 import BeautifulSoup
import json

INFO_NOT_AVAILABLE = "Info currently not available"

class RateMyProfWebScraper:

    # School id 1112 = University of Illinois at Urbana-Champaign.
    def __init__(self, schoolId, teacher, schoolName):
        self.pageData = ""
        self.rating = ""
        self.takeAgain = ""
        self.teacherName = teacher
        self.index = -1
        self.schoolId = schoolId
        self.schoolName = schoolName

    # This function retrieves and initializes the data of a professor of a given university
    def retrieveRMPInfo(self):
        if self.teacherName is None or self.teacherName == "" :
            self.rating = INFO_NOT_AVAILABLE
            return

        url_list = list()
        if self.index == -1:            
            # making request to the RMP page
            name_list = self.schoolName.split(",")
            school_url_name = ""
            for s in name_list :
                school_url_name += s + "+"      

            # TODO: Generalize the link for any professor
            url = f"https://www.ratemyprofessors.com/search.jsp?queryoption=HEADER&queryBy \
            =teacherName&schoolName={school_url_name}schoolID=1112&query=Geoffrey+Herman"
            page = requests.get(url)
            self.pageData = page.text
            # print(self.pageData)
            pageDataTemp = re.findall(r'ShowRatings\.jsp\?tid=\d+', self.pageData)
            # print(pageDataTemp)

            for i in pageDataTemp:
                new_url = "https://www.ratemyprofessors.com/" + i
                url_list.append(new_url)
            page = requests.get(url_list[0])
            soup = BeautifulSoup(page.text, 'html.parser')          
            rating_list = soup.find_all(class_ = 'RatingValue__Numerator-qw8sqy-2 gxuTRq')
            
            take_again = soup.findAll(class_ = 'FeedbackItem__FeedbackNumber-uof32n-1 bGrrmf')
            
            self.rating = rating_list[0].contents[0]  
            self.takeAgain = take_again[0].contents[0]         

    # This function returns the rating of the professor
    def getRMPRating(self):
        if self.rating == INFO_NOT_AVAILABLE:
            return INFO_NOT_AVAILABLE

        return self.rating + "/5.0"

    # This function returns the percentage of students taking the class again
    def getTakeAgainPercent(self):
      return self.takeAgain


# ScrapeObject = RateMyProfWebScraper(1112, "Geoffrey Herman", "University of Illinois")
# ScrapeObject.retrieveRMPInfo()
# rating = ScrapeObject.getRMPRating()
# print(rating)
# takeAgain = ScrapeObject.getTakeAgainPercent()
# print(takeAgain)