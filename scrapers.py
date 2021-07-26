import re
from bs4 import BeautifulSoup
import requests

class JobPosting:
    def __init__(self, job_title = "None", job_company = "None",job_link = "None"):
        website_url = "https://ca.indeed.com"
        self.job_title = job_title
        self.job_company = job_company
        self.job_link = "<" + website_url + job_link + ">"

    def set_title(self, val):
        self.job_title = val
    def set_company(self, val):
        self.job_company = val
    def set_link(self, val):
        self.job_link = val

class ScrapeIndeed:
    def __init__(self, search_term, location, time_span):
        self.search_term = search_term
        self.location = location
        self.time_span = time_span

    def collect_postings(self) -> list:
        base_indeed_url = "https://ca.indeed.com/jobs?q="
        req = requests.get(self.format_url(base_indeed_url, 0))
        soup = BeautifulSoup(req.content, 'html.parser')

        job_results = []
        info = soup.find_all('a',{'class':re.compile('^tapItem fs-unmask result job_.*')})
        for item in info:
            href = item.get('href')
            title = item.find(class_="heading4 color-text-primary singleLineTitle tapItem-gutter").text.strip()
            if title[0:3] == "new":
                title = title[3:]
            company = item.find(class_="companyName").text.strip()
            result = JobPosting(title,company,href)
            job_results.append(result)
        return job_results

    def format_url(self, base_url, page_num=0) -> str:
        resultant = ""
        resultant += base_url + self.input_fix(self.search_term) + "&l=" + self.input_fix(self.location) + "&fromage=" + self.time_span + "&start=" + str(page_num)
        return resultant

    def input_fix(self, term) -> str:
        resultant = ""
        for i in range (0, len(term)):
            if term[i] == " ":
                resultant += "+"
            else:
                resultant += term[i]
        return resultant
