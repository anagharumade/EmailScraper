from bs4 import BeautifulSoup
import re
import urllib2
from operator import itemgetter
import time
import sys
import requests
import csv

def geturl(input):
    print "in geturl"
    freq={}
    inlink={}
    html=None
    fin = open (input) #Open file containing list of urls
    for line in fin: # For every line
        url = line.strip().lower()

        for i in range(5): # try 5 times
                try:
                    #use the browser to access the url
                    response = requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                    html = response.content # get the html\
                    break # we got the file, break the loop
                except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                    print 'failed attempt',i
                    time.sleep(2) # wait 2 secs
                    print url

        if not html: continue # couldnt get the page
        else:
            soup = BeautifulSoup(html, "html5lib") # parse the html

            href=set()
            for link in soup.find_all('a', attrs={'href': re.compile("contact")}):
                href.add(link.get('href'))
            for link in soup.find_all('a', attrs={'href': re.compile("about")}):
                href.add(link.get('href'))
            for link in soup.find_all('a', attrs={'href': re.compile("team")}):
                href.add(link.get('href'))
            for link in soup.find_all('a', attrs={'href': re.compile("who")}):
                href.add(link.get('href'))
            for link in soup.find_all('a', attrs={'href': re.compile("we")}):
                href.add(link.get('href'))
            for link in soup.find_all('a', attrs={'href': re.compile("us")}):
                href.add(link.get('href'))
            for link in soup.find_all('a', attrs={'href': re.compile("bio")}):
                href.add(link.get('href'))
            for link in soup.find_all('a', attrs={'href': re.compile("info")}):
                href.add(link.get('href'))

            inlink[url]=href

    fin.close()

    return inlink


def getemail(inlink):
    print "in getemail"

    freq = {}

    html = None
    for key, value in inlink.iteritems(): # For every value in dictionary
        uniemails=set()
        links = {}
        for item in value:
            if item.startswith('http'):
                url = item.strip().lower()

                for i in range(5): # try 5 times
                    try:
                        #use the browser to access the url
                        response = requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                        html = response.content # get the html\
                        break # we got the file, break the loop
                    except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                        time.sleep(2) # wait 2 secs

                if not html: continue # couldnt get the page
                else:
                    emails=list() # Variable to store email ids
                    emails.append(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", html, re.I)) #Find email ids in html ignoring case
                    links[url]=emails
            else:
                url = key + item

                for i in range(5): # try 5 times
                    try:
                        #use the browser to access the url
                        response = requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                        html = response.content # get the html\
                        break # we got the file, break the loop
                    except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                        time.sleep(2) # wait 2 secs

                if not html: continue # couldnt get the page
                else:
                    emails=list() # Variable to store email ids
                    emails.append(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", html, re.I)) #Find email ids in html ignoring case
                    links[url]=emails

            """for email in emails:
                for e in email:
                    uniemails.add(e)

            links[item]=uniemails"""
            #print links
        freq[key]=links

    return freq


def writecsv(dic):
    print "in writecsv"
    """with open('href.csv', 'wb') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, dic.keys())
        w.writeheader()
        w.writerow(dic)"""

    with open('email.csv', 'wb') as csv_file:  # Just use 'w' mode in 3.x
        we = csv.writer(csv_file)
        we.writerow(["URL", "EMAIL ID", "SUBURL"])
        with open('href.csv', 'wb') as csv_file:  # Just use 'w' mode in 3.x
            wh = csv.writer(csv_file)
            wh.writerow(["URL", "SUBURL"])
            for url, suburl in dic.items():
                for sub, listemails in suburl.items():
                    for emails in listemails:
                        for email in emails:
                            if not email:
                                wh.writerow([url, sub])
                            else:
                                we.writerow([url, email, sub])


if __name__=='__main__':

    writecsv(getemail(geturl('input.txt')))
