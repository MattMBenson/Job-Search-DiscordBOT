import re
from bs4 import BeautifulSoup
import requests

class jobPosting:
    def __init__(self, jobTitle="None", jobCompany="None",jobLink="None"):
        base_indeed_url = "https://ca.indeed.com" 
        self.jobTitle = jobTitle
        self.jobCompany = jobCompany
        self.jobLink = "<" + base_indeed_url + jobLink + ">"

    def setJobTitle(self, val:str):
        self.jobTitle = val
    def setJobLocation(self, val:str):
        self.jobLocation = val
    def setJobLink(self, val:str):
        self.jobLink = val

class scrapeIndeed:
    #default:
    #def __init__(self, searchTerm = "winter 2021 internship", location = "canada", timespan ="14"):
    def __init__(self, searchTerm, location, timespan):
        self.searchTerm = searchTerm
        self.location = location
        self.timespan = timespan

    def collectPostings(self) -> list:
        base_indeed_url = "https://ca.indeed.com/jobs?q="
        r = requests.get(self.formatURL(base_indeed_url,0))
        #print(self.formatURL(base_indeed_url,0))
        soup = BeautifulSoup(r.content, 'html5lib')

        hrefList = [] 
        jobResults = []
        info = soup.find_all('a',{'class':re.compile('^tapItem fs-unmask result job_.*')})
        for item in info:
            href = item.get('href')
            title = item.find(class_="heading4 color-text-primary singleLineTitle tapItem-gutter").text.strip()
            if title[0:3] == "new":
                title = title[3:]
            company = item.find(class_="companyName").text.strip()
            aResult = jobPosting(title,company,href)
            jobResults.append(aResult)
        return jobResults
        
    def formatURL(self, baseURL, pageNum=0) -> str:
        resultant = ""
        resultant += baseURL + self.inputFix(self.searchTerm) + "&l=" + self.inputFix(self.location) + "&fromage=" + self.timespan + "&start=" + str(pageNum)
        return resultant

    def inputFix(self, term) -> str:
        resultant = ""
        for i in range (0,len(term)):
            if term[i] == " ":
                resultant+= "+"
            else:
                resultant+= term[i]
        return resultant



