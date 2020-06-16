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
def getArchivedURLs(province, daysInterval=7):
    urls = set()
    delta = datetime.timedelta(days=daysInterval)
    startDate = datetime.date(2010, 1, 1) # there are no webpages before 2010
    endDate = datetime.date.today()

    while(startDate < endDate):
        archiveUrl = "http://archive.org/wayback/available?url=www.dwa.gov.za/Hydrology/Weekly/ProvinceWeek.aspx?region="
        archiveUrl += province + "&timestamp=" + str(startDate.year) + str(startDate.month) + str(startDate.day)

        try:
            data = requests.get(archiveUrl).json()
            urls.add(data["archived_snapshots"]["closest"]["url"])
        except:
            print("Something went wrong when pulling the URL for the date " + str(startDate))

        startDate += delta # increment days by the interval
        time.sleep(1) # doing things too quickly causes problems
    
    return sorted(urls)

def getTableData(url):
    soup = BeautifulSoup(requests.get(url).text)
    table = soup.find(findTableHTML)
    rows = table.findAll(lambda tag: tag.name=='tr') # get every row with the tag 'tr'

    cleanTable = list()

    for row in rows:
        cleanRow = list()
        for data in row.find_all("td"):
            data = data.get_text(strip=True)
            if data != "Photo" and data != "Indicators": # these parts are useless to us
                cleanRow.append(data)

        if "Total" not in cleanRow and "Last Week" not in cleanRow and len(cleanRow) > 0: # exclude lines we don't want
            cleanTable.append(cleanRow)

    return cleanTable

def findTableHTML(tag):
    # filter for the table of data by looking through tags
    # gets a table that has a header with "Dam" but doesn't include extraneous stuff
    return tag.name == "table" and tag.find(lambda header: (header.name == "th" or header.name == "h3") and header.text == "Dam") and "Means latest available data" not in tag.text

def getProvinces(fileName):
    return open(fileName, "r").readlines()

print(getTableData("https://web.archive.org/web/20101007170516/http://www.dwa.gov.za/Hydrology/Weekly/ProvinceWeek.aspx?region=M"))