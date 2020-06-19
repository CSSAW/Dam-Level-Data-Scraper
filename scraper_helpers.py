from bs4 import BeautifulSoup
import os
import urllib
import pickle
import requests
import sys
import pandas as pd
import io
import datetime
import time

# gets all of the Internet Archive URLs for a specific province
def getArchivedURLs(province, daysInterval=7, sleep=1):
    urls = set()
    delta = datetime.timedelta(days=daysInterval)
    startDate = datetime.date(2010, 1, 1) # there are no webpages before 2010
    endDate = datetime.date.today()

    print("Starting scrapping...")

    while(startDate <= endDate):
        archiveUrl = "http://archive.org/wayback/available?url=www.dwa.gov.za/Hydrology/Weekly/ProvinceWeek.aspx?region="
        archiveUrl += province + "&timestamp=" + str(startDate.year) + str(startDate.month) + str(startDate.day)

        try:
            data = requests.get(archiveUrl).json()
            urls.add(getURL(data))
        except:
            print("Something went wrong when finding a URL for the date " + str(startDate))

        startDate += delta # increment days by the interval
        time.sleep(sleep) # doing things too quickly causes problems

    print("Found URLs for " + province)
    
    return sorted(urls)

def getTableData(url, date):
    soup = BeautifulSoup(requests.get(url).text, features="html.parser")
    table = soup.find(findTableHTML)
    rows = table.findAll(lambda tag: tag.name=='tr') # get every row with the tag 'tr'

    cleanTable = list()

    for row in rows:
        cleanRow = [date]
        for data in row.find_all("td"):
            data = data.get_text(strip=True).replace('#', '') # remove HTML tags and the "latest available data" indicator
            if data != "Photo" and data != "Indicators": # these parts are useless to us
                cleanRow.append(data)

        if "Total" not in cleanRow and "Last Week" not in cleanRow and len(cleanRow) > 1: # exclude lines we don't want
            cleanTable.append(cleanRow)

    return pd.DataFrame(data=cleanTable, columns=["Date", "Dam", "River", "FSC", "This week", "Last Week", "Last Year"])

def findTableHTML(tag):
    # filter for the table of data by looking through tags
    # gets a table that has a header with "Dam" but doesn't include extraneous stuff
    return tag.name == "table" and tag.find(lambda header: (header.name == "th" or header.name == "h3") and header.text == "Dam") and "Means latest available data" not in tag.text

def getURL(json):
    return json["archived_snapshots"]["closest"]["timestamp"][:8], json["archived_snapshots"]["closest"]["url"]

def getProvinces(fileName):
    return open(fileName, "r").readlines()