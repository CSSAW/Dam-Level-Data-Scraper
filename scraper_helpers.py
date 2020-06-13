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

def getProvinces(fileName):
    return open(fileName, "r").readlines()