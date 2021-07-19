from bs4 import BeautifulSoup
import requests

class scrapeIndeed:
    #def __init__(self, searchTerm = "intern", location = "toronto", timespan = "14"):
    def __init__(self, searchTerm = "winter 2021 internship", location = "vancouver", timespan ="14"):
        self.searchTerm = searchTerm
        self.location = location
        self.timespan = timespan

    def collectPostings(self, page="0"):
        base_indeed_url = "https://ca.indeed.com/jobs?q="
        r = requests.get(self.formatURL(base_indeed_url,page))
        soup = BeautifulSoup(r.content, 'html5lib')
        #set of listings

        setPostings = soup.find_all(class_="resultContent")
        print(setPostings)

    
    def formatURL(self, baseURL, nextPage=0) -> str:
        resultant = ""
        resultant += baseURL + self.inputFix(self.searchTerm) + "&l=" + self.inputFix(self.location) + "&fromage=" + self.timespan + "&start=" + str(nextPage)
        return resultant

    def inputFix(self, term) -> str:
        resultant = ""
        for i in range (0,len(term)):
            if term[i] == " ":
                resultant+= "+"
            else:
                resultant+= term[i]
        return resultant

def main():
    #test area
    test = scrapeIndeed()
    test.collectPostings(0) #page 1
    test.collectPostings(10) #page 2
    test.collectPostings(20) #page 3
    
if __name__ == '__main__':
    main()

