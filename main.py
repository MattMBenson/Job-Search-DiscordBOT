from scrapers import *

def textSampleMessage(position:jobPosting):
    print("Company:", position.jobCompany)
    print("Position:", position.jobTitle)
    print("Link:", position.jobLink)

#TEST BENCH#->
def main():
    scrapeForMe = scrapeIndeed("associate","toronto","3")
    foundPositions = scrapeForMe.collectPostings()
    

if __name__ == '__main__':
    main()