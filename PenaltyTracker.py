import urllib,json, sys, os, shutil, httplib
from datetime import *
from Penalty import *
from ftplib import FTP
from credientials import *


def uploadFile(file):
    '''
    Inputs:
        file - The file that will be uploaded.
    
    
    Uploads the file to the website. It does not return anything to report that it has been successful. Potential Enhancement.
    The credientials are also stored locally. On the server there is a specific user set up. The root directory for that user is the Penalty Tracker's root.
    '''
    address = credientials["address"]
    user = credientials["username"]
    password = credientials["password"]

    ftp = FTP(address)
    ftp.login(user, password)
    
    ftp.storlines("STOR " + file, open(file, 'r'))
    ftp.close()
    
def backupData(desiredFileName, todaysDate):
    ''' In order to guard against data corruption, this script creates a local back-up copy of any required file.
    
    Inputs:
        desiredFileName - This is the file that will be backed up
        
    Returns:
        There is no return value for this. Potential enhancement would be return a success signal.
    '''
    
    #Checking to see if the directories exist, if they don't create them.
    if not os.path.exists('.\\defunct_files\\'):
        shutil.os.mkdir('.\\defunct_files\\')
    if not os.path.exists('.\\defunct_files\\old_pages'):
        shutil.os.mkdir('.\\defunct_files\\old_pages')
        
    #Setting up the name and copying the file.
    newName = ".\\defunct_files\\old_pages\\" + desiredFileName + "_" + todaysDate + ".html"
    shutil.copy(desiredFileName, newName)
    


# Lifting this from the old generateHTML
def generateHTML(newSection, desiredFileName):
    '''    Opens the local copy of the index.html file and appends it with the new penalty data
        INPUTS: 
            newSection - The new section to be written to the file
            desiredFileName - the name of the file we're writing to. JUST THE NAME. Do not open.
    '''

    indexFile = open(desiredFileName,'r')
    indexFileRead = indexFile.read()
    indexFile.close()
    
    todaysDate = str(date.today()) # This is for the generation date at the bottom of the page.
    backupData(desiredFileName, todaysDate) # This function creates the local backup.
        
    
    newFile = open(desiredFileName,'w')
    locationOfNote = indexFileRead.find("<!-- INSERT DATA HERE -->") # This is the note that exists at the end of the previous dataset.
    locationOfDate = indexFileRead.find("<B id=\"newDate\">") +  len("<B id=\"newDate\">") #This is the location of the modified date
    midSection = indexFileRead[locationOfNote:locationOfDate]
    locationOfEnd = indexFileRead[::-1].find(">b/<") + len(">b/<") #The tag has to be backwards.
    endingData = indexFileRead[len(indexFileRead)-locationOfEnd::] #Storing the data after the last entry since it will be overwritten
    newFile.write(indexFileRead[0:locationOfNote-1] + newSection + "\n\t\t"+ midSection + todaysDate + endingData)
    newFile.close()


def formatDate(*args):
    '''
        Looks at the system to determine the date
        Converts the date to the proper format...
        
        This is to safe guard the NHL changing the date format again.
        
        DateTimes format is YYYY-MM-DD        
        Returns: String in the format of YYYY-MM-DD
    '''
    if len(args) == 0: #This allows me to specify dates for testing / in case the script misses a date.
        today = date.today()- timedelta(1)
        dateAsString = str(today)
    else:
        dateAsString = args[0]
    return dateAsString
    
def processGame(game, date):
    '''
        This function will parse game URL's JSON Stream.
      
        Inputs:
            game - string - This is the URL of the game.
            date - The date of the game.
        
        Returns:
            gamePenaltyList - List of Penalty Objects - This is the list of penalties that occur during the game.
    '''

    #Establishing and clearing the list of Penalties
    gamePenaltyList = []
    gamePenaltyList[:] = []
    
    #Getting the JSON data from the NHL website
    gameData = urllib.urlopen(game)
    jsonData = json.load(gameData)
    
    #Added a special case for Montreal because they have an accent.
    awayTeam = jsonData["gameData"]["teams"]["away"]["name"]
    if (awayTeam.lower().find("canadiens") != -1):
        awayTeam = "Montreal Canadiens"
    homeTeam = jsonData["gameData"]["teams"]["home"]["name"]
    if (homeTeam.lower().find("canadiens") != -1):
        homeTeam = "Montreal Canadiens"
    
    #Establishing and clearing the list of Referees
    refs = []
    refs[:] = []
    
    #Getting the referees for the game.
    for i in jsonData["liveData"]["boxscore"]["officials"]:
        if i["officialType"].lower() == "referee":
            refs.append(i["official"]["fullName"])
    
    #Getting the Penalty Data from the JSON stream.
    penaltyPlays = []
    penaltyPlays[:] = []
    for i in jsonData["liveData"]["plays"]["penaltyPlays"]:
        penaltyPlays.append(i)
    for j in penaltyPlays:
        penaltyEvent = jsonData["liveData"]["plays"]["allPlays"][j]
        playerName = penaltyEvent["players"][0]["player"]["fullName"]
        penaltyName = penaltyEvent["result"]["secondaryType"]
        playerTeamName = penaltyEvent["team"]["name"]
        
        if playerTeamName == awayTeam:
            location = False
            opponentTeamName = homeTeam
        else:
            location = True
            opponentTeamName = awayTeam
            
        dateFormatted = date[5:7] + "/" + date[8::] + "/" + date[0:4]
        
        #Checking to see if it was a penalty shot. At this time, the NHL does not consider Penalty Shots to count towards the team totals.
        if "PS-" not in penaltyName:
            newPenalty = Penalty(playerName, playerTeamName, penaltyName, location, opponentTeamName, dateFormatted, refs)
            gamePenaltyList.append(newPenalty)
            
    return gamePenaltyList
        
    
def getData(date):
    '''
        Looks for game entries on the NHL data stream
        Ideally it is looking for the "live" link because that contains all the penalty data.
   
        Input param : String : Formatted by the "formatDate"
    '''
    beginning_url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate="
    middle_url="&endDate="
    end_url="&expand=schedule.teams,schedule.linescore,schedule.broadcasts,schedule.ticket,schedule.game.content.media.epg&leaderCategories=&site=en_nhl&teamId="
    full_url = beginning_url + date + middle_url + date + end_url
    
    gameDataURLprefix = "https://statsapi.web.nhl.com"
    
    try:
        websiteData = urllib.urlopen(full_url)
        jsonData = json.load(websiteData)
    except:
        sys.exit(-1)   #If we can't load the page, exit with an error.
    
    gameURLS = [] # This list is going to contain the URLs pointing to games as strings.
    gameURLS[:] = []
    try:
        for i in jsonData['dates'][0]['games']:
            gameURLS.append( gameDataURLprefix + i["link"] )
    except IndexError:
        # If there are no games, there is no sense in updating anything, so it should exit.
        print "No games today!"
        sys.exit(0)
        
    return gameURLS
    
def getPenaltyListAsString(penaltyList):
    ''' This converts the penalty data to a string of HTML. This way I can put the data in the HTML file
    
        Input:
            penaltyList - a list of Penalties
        
        Returns:
            data - A string.
    '''
    data = ""
    for penalty in penaltyList:
        data += penalty.printTable() + "\n"
    return data
    
def uploadToParse(penaltyList):
    ''' This function will upload the penalty objects onto Parse-Application-Id
    
        Input:
            penaltyList - a list of Penalties
        
        Returns:
            Nothing at the moment. I should enhance this to return a status.
    '''
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    for penalty in penaltyList:
        connection.request('POST', '/1/classes/Penalties', json.dumps({
           "player": penalty.getPlayer(),
            "team": penalty.getTeam(),
            "penalty": penalty.getPenalty(),
            "date": penalty.getDate(),
            "opponent": penalty.getOpponent(),
            "location": penalty.getSide(),
            "referees" : penalty.getRefs()
         }), {
           "X-Parse-Application-Id": credientials["appID"],
           "X-Parse-REST-API-Key": credientials["restID"],
           "Content-Type": "application/json"
         })
        results = json.loads(connection.getresponse().read())
    
def run():
    '''
        This is the main function. I had to create this to allow me to get this entire script under test with the UnitTest framework
    '''
    

    date = formatDate() #If the tracker missed a day, put a string of the date in this function.
    gameURLS = getData(date)
    if ( len(gameURLS) ) > 0:
        newPenaltyString = ""
        for game in gameURLS:
            penaltyList = processGame(game,date)
            uploadToParse(penaltyList)
            newPenaltyString += getPenaltyListAsString(penaltyList)
        generateHTML(newPenaltyString, "index.html")
        uploadFile("index.html")


try:
	sys.argv[1]
	run()
except IndexError:
	pass #If this is ran from the unit test, nothing extra runs.
    