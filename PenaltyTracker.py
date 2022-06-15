from datetime import date, datetime, timedelta
from urllib import request
import json, os, ssl

from DatabaseManager import DatabaseManager
from Penalty import Penalty

class PenaltyTracker:

    def __init__(self):
        self.targetDate = date.today() - timedelta(1);
        self.databaseLocation = os.getenv("PT_DBLOC")
        self.timePeriod = os.getenv("PT_SEASON")

        if self.databaseLocation is not None and self.timePeriod is not None:
            self.databaseManager = self.createAndSetDatabaseManager()
        else:
            self.databaseManager = None

    ''' Setters '''
    def setDatabaseLocation(self, newLocation):
        self.databaseLocation = newLocation
        return self
    
    def setSeason(self, newSeason):
        self.timePeriod = newSeason
        return self

    def setTargetDate(self, newDate):
        try:
            if isinstance(newDate, date):
                self.targetDate = newDate
            elif isinstance(newDate, str):
                tryDate = datetime.strptime(newDate, '%Y-%m-%d')
                self.targetDate = newDate;
            else:
                raise Exception("Expected inputs for Target Date are a string in the YYYY-MM-DD format or a date object")
        except Exception as err:
            print("Exception Encountered:", err)

    def createAndSetDatabaseManager(self):
        try:
            if self.databaseLocation == "":
                raise Exception("No Database Location provided")
            if self.timePeriod == "":
                raise Exception("No Season provided")
            self.databaseManager = DatabaseManager(self.databaseLocation, self.timePeriod);
        except Exception as err:
            print("Exception Encountered:", err)

    def RunErrorChecking(self):
        try:
            if self.databaseLocation == "":
                raise Exception("No Database provided")
            if self.timePeriod == "":
                raise Exception("No Season provided")
            if self.databaseManager is None:
                raise Exception("No Database Manager defined")
            if self.targetDate is None:
                self.targetDate = date.today();
        except Exception as err:
            print("Exception Encountered:", err)

    def GetGameURLS(self):
        targetDate = str(self.targetDate)
        gameDataURLprefix = "https://statsapi.web.nhl.com"
        beginning_url = gameDataURLprefix + "/api/v1/schedule?startDate="
        middle_url="&endDate="
        full_url = beginning_url + targetDate + middle_url + targetDate

        try:
            context = ssl._create_unverified_context()
            websiteData = request.urlopen(full_url, context=context).read().decode('UTF-8')
            jsonData = json.loads(websiteData)
        except Exception as err:
            print("Error:", err)

        gameURLS = [] # This list is going to contain the URLs pointing to games as strings.
        gameURLS[:] = []
        try:
            numberOfDates = len(jsonData['dates'])
            for dateIndex in range(0, numberOfDates):
                gameDay = jsonData['dates'][dateIndex]["date"]
                for i in jsonData['dates'][dateIndex]['games']:
                    gameURLS.append( (gameDataURLprefix + i["link"], gameDay) )
        except IndexError as err:
            print("Error:", err)
        return gameURLS

    def ProcessGame(self, game):
        '''
            This function will parse game URL's JSON Stream.

            Inputs:
                game - string - This is the URL of the game.
                date - The date of the game.

            Returns:
                gamePenaltyList - List of Penalty Objects - This is the list of penalties that occur during the game.
        '''
        gameURL = game[0]
        gameDate = game[1]

        #Establishing and clearing the list of Penalties
        gamePenaltyList = []
        gamePenaltyList[:] = []

        #Getting the JSON data from the NHL website
        context = ssl._create_unverified_context()
        response = request.urlopen(gameURL, context=context).read().decode('UTF-8')
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

            #Checking to see if it was a penalty shot. At this time, the NHL does not consider Penalty Shots to count towards the team totals.
            if "PS-" not in penaltyName and "PS - " not in penaltyName:
                newPenalty = Penalty(playerName, playerTeamName, penaltyName, location, opponentTeamName, gameDate, refs)
                gamePenaltyList.append(newPenalty)

        return gamePenaltyList

    def SubmitPenaltyToDatabase(self, penalty):
        try:
            if self.databaseManager is None:
                raise Exception("No Database Manager defined")
            self.databaseManager.insertData(penalty.formatForSQL())
        except Exception as err:
            print("Error:", err)
        
    def run(self):
        self.RunErrorChecking();
        gameURLS = self.GetGameURLS()
        for game in gameURLS:
            gamePenalties = self.ProcessGame(game)
            for penalty in gamePenalties:
                self.SubmitPenaltyToDatabase(penalty)

        
