'''
	This code is to grab the boxscore HTML file for every game that happened the previous night
	It is going to be using the following modules:
		urllib - To open the desired webpages, read them or save them to disk.
		os - To create the directories corresponding to the correct date.

	This program was written by Roy W. Gero.
	If you have questions, comments or concerns please contact him on GitHub
'''
import urllib,os
from datetime import date, timedelta as td

startOfSeason = date(2014,10,8) #This is the official start of the regular season
today = date.today()
delta = today - startOfSeason

daysToGet = []
checkedDays=[]

for i in range(delta.days + 1):
	dateInQuestion = startOfSeason + td(days=i)
	if not os.path.exists("GameLogs\\"+str(dateInQuestion)):
		dateInQuestion = str(dateInQuestion)
		dateInQuestion = dateInQuestion[5:7] + "/" + dateInQuestion[8::] + "/" + dateInQuestion[0:4]
		todayFormatted = str(today)
		todayFormated = todayFormatted[5:7] + "/" + todayFormatted[8::] + "/" + todayFormatted[0:4]
		if dateInQuestion not in todayFormated:
			daysToGet.append( str(dateInQuestion))

'''	
	To save time, I am keeping track of all the days that don't have games.
	This is so they can be ignored when running this code later.
'''
try:
	file = open("No Game Days.txt",'r')
	checkFile = file.read()
	for i in daysToGet:
		if i not in checkFile:
			checkedDays.append(i)		
except NameError:
	pass
	#I want this to do nothing because if the file doesn't exist, it will be created later.

		
		
		
counterDay = 0
for i in checkedDays:
	counterDay +=1
	#Prints a message to show that the process is running
	print "Processing %s which is the %d element out of %d" % (i, counterDay, len(checkedDays))
	
	#The desired webpage to see all the games that happened the previous day.
	#The trend was noticed by looking at the URL's for all the pages.
	desiredURL = "http://www.nhl.com/ice/scores.htm?date=" + i + "&season=20142015"
	desiredWebsite = urllib.urlopen(desiredURL)
	websiteData = desiredWebsite.read()

	#Looking at the source code, I can see a reference to the current date after the "datepicker" query.
	#Using this I can get the date and format it in a way that is consistent with my other folders. (YYYY-MM-DD)
	#Note: This is extremely lazy since... time.date is in the correct format and I have to convert it to the wrong  format for the URL
	dateStart = websiteData.find("jQuery.datepicker.parseDate('mm/dd/yy',")+len("jQuery.datepicker.parseDate('mm/dd/yy', '")
	dateEnd = websiteData[dateStart::].find("');")+dateStart
	date = websiteData[dateStart:dateEnd]
	dateFormat = date[len(date)-4::] + "-" + date[0:2] + "-" + date[3:5]

	games = [] # Creates a blank array to store the boxscore URLs found on the page.

	#This is a simple search through the webpage's HTML. It relies on the fact that there will be at least one game.
	found = 0
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

	folder = "GameLogs\\" + dateFormat #The destined folder to save the filter
	if len(games)!=0 and not os.path.exists(folder): #Makes sure the folder does not exist. If it does, this doesn't run.
		counter = 0
		os.makedirs(folder) #Makes the directory for storing the files.
		for i in games:
			counter +=1
			location = "GameLogs\\" + dateFormat + "\\" +  str(counter) + ".htm"
			urllib.urlretrieve(i,location) #Downloads the file to the correct directory
	else:
		'''Checks to see if the file exists'''
		while True:
			try:
				file = open("No Game Days.txt",'a+')
				break
			except NameError:
				file = open("No Game Days.txt",'w')
				break
		file.write("\n" + date)
		file.close()