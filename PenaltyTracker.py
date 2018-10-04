import json, sys, os, shutil, http.client
from urllib import request, error, parse, robotparser
from datetime import *
from Penalty import *
from DatabaseManager import *
import ssl

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
    context = ssl._create_unverified_context()
    response = request.urlopen(game, context=context).read().decode('UTF-8')
    jsonData = json.loads(response)

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
        if "PS-" not in penaltyName and "PS - " not in penaltyName:
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
        context = ssl._create_unverified_context()
        websiteData = request.urlopen(full_url, context=context).read().decode('UTF-8')
        jsonData = json.loads(websiteData)
    except:
        print("Error")
        sys.exit(-1)   #If we can't load the page, exit with an error.

    gameURLS = [] # This list is going to contain the URLs pointing to games as strings.
    gameURLS[:] = []
    try:
        numberOfDates = len(jsonData['dates'])
        for date in range(0, numberOfDates):
          gameDay = jsonData['dates'][date]["date"]
          for i in jsonData['dates'][date]['games']:
              gameURLS.append( (gameDataURLprefix + i["link"], gameDay) )
    except IndexError:
        # If there are no games, there is no sense in updating anything, so it should exit.
        print("No games today!")
        sys.exit(0)

    return gameURLS

def run(**kwargs):
    if "dbLoc" not in kwargs:
        dbLoc = "/home/roymond/Website/RoymondNET/PenaltyTracker/static/penaltytracker/season.db"
    else:
        dbLoc = kwargs["dbLoc"]

    #Create the DatabaseManager
    dbManager = DatabaseManager(dbLoc, "Regular_18_19")

    if "date" in kwargs:
        date = formatDate( kwargs["date"] )
    else:
        date = formatDate()

    gameURLS = getData(date)
    if ( len(gameURLS) ) > 0:
        for game in gameURLS:
            gameURL = game[0]
            date = game[1]
            penaltyList = processGame(gameURL,date)
            for penalty in penaltyList:
              dbManager.insertData(penalty.formatForSQL())

if __name__ == "__main__":
    run()
