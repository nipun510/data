#!/usr/bin/python

from utils import web_utils as wu
import requests

from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'

headers = {'User-Agent': user_agent}
nextPageBaseUrl = 'https://www.nseindia.com/sme/marketinfo/corporates/annualreports/'
downloadLinkBaseUrl = 'https://www.nseindia.com/'

def getInfo(soupElement):
    name=soupElement.findAll('td')[0].getText()
    desc=soupElement.findAll('td')[1].getText()
    reportlink=downloadLinkBaseUrl + soupElement.findAll('td')[2].select('a')[0].get_attribute_list('href')[0]
    return (name, desc, reportlink)

def getPageInfo(soupPage):
    return [getInfo(elem) for elem in soupPage]

def getNextPageUrl(currentSoupPage):
    return currentSoupPage.findAll('table')[0].select('tr')[-2].select('td')[0].select('a')[-1].get_attribute_list('href')[-1]


def getData(url):
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup

def fetchPageData(url):
    print(url)
    soup = getData(url)
    tableRows = soup.findAll('tr', {'class': 'alt'})
    info = getPageInfo(tableRows)
    nextUrl = getNextPageUrl(soup)
    return (info, nextPageBaseUrl + nextUrl)

def prepareDownloadLinks(result):
    return [ item[2] for item in result]

def downloadData(linksList, baseDir):
    for link in linksList:
        wu.downloadFile(link, baseDir)

def scrapData(url='https://www.nseindia.com/sme/marketinfo/corporates/annualreports/latestAnnualReports.jsp?currentPage=1'):
    result = []
    visitedList = {}

    data , nextUrl = fetchPageData(url)
    visitedList[url] = True
    url = nextUrl

    result = result + data

    while url:
        if url in visitedList:
            url = None
            continue
        data, nextUrl = fetchPageData(url)
        visitedList[url] = True
        url = nextUrl
        result = result + data
        print('**** One Page Data Completed *********')
    downloadData(prepareDownloadLinks(result), '/home/nikumar/tmp/')
    return result
