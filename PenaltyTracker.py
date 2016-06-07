import urllib,json, sys, os, shutil, httplib
from datetime import *
from Penalty import *
from ftplib import FTP
from credientials import *


def uploadFile(file):
    '''Uploads the file to the website
    Note: Does not return anything
    The credientials are also stored locally.
    '''
    address = credientials["address"]
    user = credientials["username"]
    password = credientials["password"]

    ftp = FTP(address)
    ftp.login(user, password)
    
    ftp.storlines("STOR " + file, open(file, 'r'))
    ftp.close()
    
def backupData(desiredFileName, todaysDate):
    ''' Since there is a chance of data corruption it is good to backup the index file.
    '''
    if not os.path.exists('.\\defunct_files\\'):
        shutil.os.mkdir('.\\defunct_files\\')
    if not os.path.exists('.\\defunct_files\\old_pages'):
        shutil.os.mkdir('.\\defunct_files\\old_pages')
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
    
    todaysDate = str(date.today(desiredFileName)) # This is for the generation date at the bottom of the page.
    backupData(desiredFileName, todaysDate)
        
    
    newFile = open(desiredFileName,'w')
    locationOfNote = indexFileRead.find("<!-- INSERT DATA HERE -->")
    locationOfDate = indexFileRead.find("<B id=\"newDate\">") +  len("<B id=\"newDate\">")
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
    if len(args) == 0: #This allows me to specify dates for testing / in case I miss a date.
        today = date.today()- timedelta(1)
        dateAsString = str(today)
    else:
        dateAsString = args[0]
    return dateAsString
    
def processGame(game, date):
    gamePenaltyList = []
    gamePenaltyList[:] = []
    
    gameData = urllib.urlopen(game)
    jsonData = json.load(gameData)
    
    #Added a special case for Montreal because they have an accent.
    awayTeam = jsonData["gameData"]["teams"]["away"]["name"]
    if (awayTeam.lower().find("canadiens") != -1):
        awayTeam = "Montreal Canadiens"
    homeTeam = jsonData["gameData"]["teams"]["home"]["name"]
    if (homeTeam.lower().find("canadiens") != -1):
        homeTeam = "Montreal Canadiens"
    
    refs = []
    refs[:] = []
    
    for i in jsonData["liveData"]["boxscore"]["officials"]:
        if i["officialType"].lower() == "referee":
            refs.append(i["official"]["fullName"])
            
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
        
        if "PS-" not in penaltyName:
            newPenalty = Penalty(playerName, playerTeamName, penaltyName, location, opponentTeamName, dateFormatted, refs)
            gamePenaltyList.append(newPenalty)
            
    return gamePenaltyList
        
    
def getData(date):
    '''
        Looks for game entries on the new input stream
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
        sys.exit(-1)   
    gameURLS = []
    gameURLS[:] = []
    try:
        for i in jsonData['dates'][0]['games']:
            gameURLS.append( gameDataURLprefix + i["link"] )
    except IndexError:
        print "No games today!"
        sys.exit(0)
        
    return gameURLS
    
def getPenaltyListAsString(penaltyList):
    data = ""
    for penalty in penaltyList:
        data += penalty.printTable() + "\n"
    return data
    
def uploadToParse(penaltyList):
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
    