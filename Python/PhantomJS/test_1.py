import re, urlparse

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

link = 'https://l3com.taleo.net/careersection/l3_ext_us/jobsearch.ftl'

class TaleoJobScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS('/usr/local/bin/phantomjs')
        self.driver.set_window_size(1120, 550)

    def scrape(self):
        jobs = self.scrape_job_links()
        for job in jobs:
            print job

        self.driver.quit()

if __name__ == '__main__':
    scraper = TaleoJobScraper()
    scraper.scrape()


def scrape_job_links(self):
    self.driver.get(link)

    jobs = []
    pageno = 2

    while True:
        s = BeautifulSoup(self.driver.page_source)
        r = re.compile(r'jobdetail\.ftl\?job=\d+$')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            job = {}
            job['title'] = a.text
            job['url'] = urlparse.urljoin(link, a['href'])
            job['location'] = td[2].text
            jobs.append(job)

        next_page_elem = self.driver.find_element_by_id('next')
        next_page_link = s.find('a', text='%d' % pageno)

        if next_page_link:
            next_page_elem.click()
            pageno += 1
            sleep(.75)
        else:
            break

    return jobs


if __name__ == '__main__':
    scraper = TaleoJobScraper()
    scraper.scrape()
