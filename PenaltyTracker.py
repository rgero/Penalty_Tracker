import urllib,json, sys, os, shutil, httplib
from datetime import *
from Penalty import *
from ftplib import FTP
from DatabaseManager import *
    
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
        if (playerTeamName.lower().find("canadiens") != -1):
          playerTeamName = "Montreal Canadiens"
        
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

def run():
    '''
        This is the main function. I had to create this to allow me to get this entire script under test with the UnitTest framework
    '''
    
    dbLoc = "/home/roymond/Website/RoymondNET/PenaltyTracker/static/season.db"  
    #Create the DatabaseManager   
    dbManager = DatabaseManager(dbLoc)

    date = formatDate() #If the tracker missed a day, put a string of the date in this function.
    gameURLS = getData(date)
    if ( len(gameURLS) ) > 0:
        newPenaltyString = ""
        for game in gameURLS:
            penaltyList = processGame(game,date)
            for penalty in penaltyList:
              dbManager.insertData(penalty.formatForSQL())

try:
  sys.argv[1]
  run()
except IndexError:
  print "This is running from Unit Test"
  pass #If this is ran from the unit test, nothing extra runs.
    
