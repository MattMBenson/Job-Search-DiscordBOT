import requests
from bs4 import BeautifulSoup, StopParsing

class scrapeIndeed:
    #def __init__(self, searchTerm = "", location = "", timespan = "3"):
    def __init__(self, searchTerm = "winter 2021 internship", location = "vancouver", timespan ="14"):
        self.searchTerm = searchTerm
        self.location = location
        self.timespan = timespan

    def collectPostings():
        indeed_url = "https://ca.indeed.com/jobs?q="
        r = requests.get(indeed_url)
        soup = BeautifulSoup(r.content, 'html5lib')
        #set of listings
        indeed_listings = []
        pageList = soup.find('div',attrs={'id':'mosaic-provider-jobcards'})

    def formatURL(self, baseURL) -> str:
        resultant = ""
        resultant += baseURL + self.inputFix(self.searchTerm) + "&l=" + self.inputFix(self.location) + "&fromage=" + self.timespan
        return resultant

    def inputFix(self, term) -> str:
        resultant = ""
        for i in range (0,len(term)):
            if term[i] == " ":
                resultant+= "+"
            else:
                resultant+= term[i]
        return resultant


#test area
test = scrapeIndeed()
print(test.formatURL("https://ca.indeed.com/jobs?q="))
#print(test.inputFix("fall 2021 internship"))
