'''
	This program was written by Roy W. Gero.
	If you have questions, comments or concerns please contact him on GitHub
'''
import urllib, sys
from ftplib import FTP
from datetime import date
from scanning_games import *
from credientials import *

def uploadFile(fileName):
	address = credientials["address"]
	user = credientials["username"]
	password = credientials["password"]
	fileName = ".\\" + fileName
	
	ftp = FTP(address)
	ftp.login(user, password)
	ftp.storlines("STOR " + fileName, open(fileName, 'r'))
	ftp.close()


def formatDate(*args):
	'''
		Looks at the system to determine the date
		Converts the date to the proper format
		
		DateTimes format is YYYY-MM-DD
		
		Returns: String in the format of MM/DD/YYYY
	'''
	if len(args) == 0:
		today = date.today()
		dateAsString = str(today)
	else:
		dateAsString = args[0]
	return dateAsString[5:7] + "/" + dateAsString[8::] + "/" + dateAsString[0:4]

def dateProcessing(dateToProcess, *args):
	'''
		Input: 
			dateToProcess - string - MM/DD/YYYY
		
	'''
	desiredURL = "http://www.nhl.com/ice/scores.htm?date=" + dateToProcess
	desiredWebsite = urllib.urlopen(desiredURL)
	websiteData = desiredWebsite.read()
	
	#I might want to pass this in to the function so I can leverage it in my unit testing.
	if len(args) == 0:
		upload = True
		fileName = "MasterPenaltyList.txt"
		MasterPenaltyList = open(fileName, 'a')
	else:
		upload = False
		fileName = args[0]
		MasterPenaltyList = open(fileName, 'w')
	
	
	found = 0
	games = []
	while found!=-1:
		'''	After inspecting the HTML of the source page, I can see that every boxscore is a simple HTML link
			From this, I can easily find each instance of a boxscore link and the URL by finding the word "BOXSCORE"
			and then looking at the data backwards to find the start of the link tag.
		'''
		found = websiteData.find("\">BOXSCORE")
		startOfLink = websiteData[found:0:-1].find("\"=ferh")
		if found!=-1:
			gameURL = websiteData[found-startOfLink+1:found]
			games.append(gameURL)
		websiteData = websiteData[found+1::] #Have to offset found by one so the search doesn't repeat itself
	
	if len(games) > 0:
		for i in games:
			gamePage = urllib.urlopen(i)
			gameData = gamePage.read()
			results = processData(gameData)
			for j in results:
				MasterPenaltyList.write(j.printEvent() + "\n")
	else:
		MasterPenaltyList.write("\nNo games on " + dateToProcess + "\n\n")
	MasterPenaltyList.close()
	
	if upload:
		uploadFile(fileName)
	
try:
	sys.argv[1]
	dateProcessing(formatDate())
except IndexError:
	pass #If this is ran from the unit test, nothing extra runs.
