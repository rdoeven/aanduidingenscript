import urllib.request
import os
import zipfile
import csv
import pickle
import datetime
from datetime import timedelta

#params

dataFolder = "data"
credsfolder = "creds"
files = {
    "nationale.zip" : 'http://static.belgianfootball.be/project/publiek/download/natdesdownP.zip',
    "WVlaanderen.zip" : 'http://static.belgianfootball.be/project/publiek/download/wvldesdownP.zip'
}

class Match:

	def __init__(self, division, date, time, home, away, status):
		date = date.split("/")
		time = time.split(":")
		self.division = division
		self.date = datetime.datetime(year = int(date[2]), month= int(date[1]), day= int(date[0]), hour= int(time[0]), minute= int(time[1]))
		self.home = home
		self.away = away
		if status == "":
			status = "as planned"
		self.status = status

	def getISOTime(self):
		return self.date.isoformat()
	
	def getmatch(self):
		return f"({self.division}) {self.home}-{self.away}"
	
	def getStatus(self):
		return self.status
	
	def __str__(self):
		return f"{str(self.date)} ~ {self.division} ~ {self.home}-{self.away} ~ {self.status}"

	def __eq__(self, other):
		return self.date == other.date and self.division == other.division and self.home == self.home and self.away == other.away

def unzipfile(_file):
    with zipfile.ZipFile(_file,"r") as zip_ref:
        ufile = zip_ref.namelist()[0]
        zip_ref.extractall(os.getcwd() + "/" + dataFolder)
    return ufile

def updateFile(filename, url):
    urllib.request.urlretrieve(url, os.getcwd()+ "/" + dataFolder + "/" + filename)
    return unzipfile(dataFolder + '/' + filename)

def extractdata(name, _file):
    matches = list()
    with open(dataFolder + "/" + _file, errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if row[6].lower() == name.lower():
                matches.append(Match(row[0], row[1], row[2], row[3], row[4], row[5]))
    return matches


def LoadData(name):
    matches = list()
    ufiles = list()
    for _file in files:
        ufiles.append(updateFile(_file, files[_file]))
    
    for _file in ufiles:
        matches.extend(extractdata(name, _file))
    
    return matches