import re, requests
from lxml import etree
import logging
from bs4 import BeautifulSoup
import json
INFO_NOT_AVAILABLE = "Check request please"
class RateMyProfWebScraper:
    def __init__(self, schoolId, teacher, schoolName):
        self.pageData = ""
        self.rating = ""
        self.takeAgain = ""
        self.teacherName = teacher
        self.index = -1
        self.schoolId = schoolId
        self.schoolName = schoolName


    def retrieveRMPInfo(self):
        """
        :function: initialize the RMP data
        """
        if self.teacherName is None or self.teacherName == "" :
            self.rating = INFO_NOT_AVAILABLE
            return
        url_list = list()
        if self.index == -1:            
            #making request to the RMP page
            name_list = self.schoolName.split(" ")
            school_url_name = ""
            print(name_list)
            for s in name_list :
                
                if "-" in s :
                    hyphen_break = s.split("-")
                    school_url_name +=  hyphen_break[0] + "+" + "-" + "+" + hyphen_break[1]
                    continue
                
                school_url_name += s + "+" 
            if "-" not in self.schoolName:
                school_url_name = school_url_name[0:len(school_url_name) - 1]
            print(school_url_name)     
            page = ""    
            instructor = (self.teacherName.split(","))
            fName = instructor[1].strip()
            lName = instructor[0]      
            print(lName, fName)

            ##url = f"https://www.ratemyprofessors.com/search.jsp?queryoption=HEADER&queryBy \
           ## =teacherName&schoolName={school_url_name}&schoolID=1112&query={lName}"
            
            url = f"https://www.ratemyprofessors.com/search.jsp?queryoption=HEADER&queryBy=teacherName&schoolName={school_url_name}&schoolID=1112&query={lName}"
            print(url)
            page = requests.get(url)
            self.pageData = page.text           
            soup = BeautifulSoup(page.text, 'html.parser')
            name = ""
            prof_content = soup.find_all(class_ = "main")
            prof_ids = re.findall(r'ShowRatings\.jsp\?tid=\d+', self.pageData)
            tup = ()
          
            for i in range(len(prof_content)):
                
                
                name_break = prof_content[i].contents[0].split(",")
                #print(name_break)
                first = name_break[1].strip()
                fInitial = first[0]
                last = name_break[0]
               # print(prof_content[i].contents[0].split(","))
                print (last,fInitial)
                #print(lName, fName)
                if last == lName and fInitial == fName:
                    tup = ((lName, prof_ids[i]))
                    break
                    
            
            print(tup)
            """
            first, last = number_of_prof_content.split('-')
            num_of_prof = int(last[0])
            print(num_of_prof)
            for i in num_of_prof:
                
            """
                
            
            #print(self.pageData)
            pageDataTemp = re.findall(r'ShowRatings\.jsp\?tid=\d+', self.pageData)
           # print(pageDataTemp)
            required_url = ""
            for i in pageDataTemp:
                
                if tup[1] == i :
                    
                    
                    required_url =  "https://www.ratemyprofessors.com/" + i
                
           
            print(required_url)
            page = requests.get(required_url)
            soup = BeautifulSoup(page.text, 'html.parser')          
            rating_list = soup.find_all(class_ = 'RatingValue__Numerator-qw8sqy-2 gxuTRq')            
            take_again = soup.find_all(class_ = 'FeedbackItem__FeedbackNumber-uof32n-1 bGrrmf')            
            self.rating = rating_list[0].contents[0]  
            self.takeAgain = take_again[0].contents[0]         

    def getRMPInfo(self):
        """
        :return: RMP rating.
        """

        if self.rating == INFO_NOT_AVAILABLE:
            return INFO_NOT_AVAILABLE

        return self.rating + "/5.0"
    
    def getTakeAgain(self):
      return self.takeAgain

