'''
	This program was written by Roy W. Gero.
	If you have questions, comments or concerns please contact him on GitHub
'''
import urllib, sys, shutil
from ftplib import FTP
from datetime import *
from scanning_games import *
from credientials import *

def uploadFile(files):
	'''Uploads the file to the website
	   Note: Does not return anything
	   The credientials are also stored locally.
	'''
	address = credientials["address"]
	user = credientials["username"]
	password = credientials["password"]
	
	ftp = FTP(address)
	ftp.login(user, password)
	
	ftp.storlines("STOR " + files[0], open(files[0], 'r'))
	ftp.storlines("STOR " + files[1], open(files[1], 'r'))
	ftp.close()
	
def htmlGenerator(newSection, desiredFileName, dt):
	'''	Opens the local copy of the index.html file and appends it with the new penalty data
		INPUTS: 
			newSection - The new section to be written to the file
			desiredFileName - the name of the file we're writing to. JUST THE NAME. Do not open.
	'''

	indexFile = open(desiredFileName,'r')
	indexFileRead = indexFile.read()
	indexFile.close()
	
	#Renaming and moving the file (it's good to have backups.)
	todaysDate = str(date.today())
	
	if (dt == ""):
		dt = todaysDate
	
	newName = ".\\defunct_files\\old_pages\\" + desiredFileName + "_" + todaysDate + ".html"
	shutil.copy(desiredFileName, newName)
	
	newFile = open(desiredFileName,'w')
	locationOfNote = indexFileRead.find("<!-- INSERT DATA HERE -->")
	locationOfDate = indexFileRead.find("<B id=\"newDate\">") +  len("<B id=\"newDate\">")
	midSection = indexFileRead[locationOfNote:locationOfDate]
	locationOfEnd = indexFileRead[::-1].find(">b/<") + len(">b/<") #The tag has to be backwards.
	endingData = indexFileRead[len(indexFileRead)-locationOfEnd::] #Storing the data after the last entry since it will be overwritten
	newFile.write(indexFileRead[0:locationOfNote-1] + newSection + "\n\t\t"+ midSection + dt + endingData)
	newFile.close()


def formatDate(*args):
	'''
		Looks at the system to determine the date
		Converts the date to the proper format
		
		DateTimes format is YYYY-MM-DD
		
		Returns: String in the format of MM/DD/YYYY
	'''
	if len(args) == 0: #This if statement allows me to use this function in unit testing.
		today = date.today()- timedelta(1)
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
	newPenalties = "" # Has to start as a new line.
	files = ["MasterPenaltyList.txt","index.html"]
	
	#	I added the need to specify a second argument to this function so that I can
	#	stop it from running if I am running it through the unit tester. I might switch
	#	the cases around, as I should have that second argument if I'm testing.
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
	
	if len(games) > 0: #If the number of games on that day are greater than 0, go through each game
		newPenalties = "\n"
		for i in games:
			gamePage = urllib.urlopen(i)
			gameData = gamePage.read()
			results = processData(gameData)
			for j in results:
				newPenalties += j.printTable() + "\n"		#Adding this line to print to the table.
				MasterPenaltyList.write(j.printEvent() + "\n")
	else:
		MasterPenaltyList.write("\nNo games on " + dateToProcess + "\n\n")
	MasterPenaltyList.close()
	
	if upload: #If I'm not running this in a unit test, upload the file to the website.
		htmlGenerator(newPenalties, "index.html", "")
		uploadFile(files)
	
try:
	sys.argv[1]
	dateProcessing(formatDate())
except IndexError:
	pass #If this is ran from the unit test, nothing extra runs.
