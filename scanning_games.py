from HTMLParser import HTMLParser
from Teams import *
from Penalty import *

GameData = []


class MyHTMLParser(HTMLParser):
	'''This generates an Array with all the HTML elements so I can quickly sort through it.'''	
	def handle_data(self, data):
		GameData.append(data)
	
	
def teamsPlaying(scan):
	'''	This section is going to scan the file for the game_string attribute and return the two playing teams.
		The first team will be the AWAY team, the second team will be the HOME team
		I have to do it this way because there is no tag for the teams.
	'''
	game_string = scan.find("game_string: \"") + len("game_string: \"")
	teams = scan[game_string: game_string + scan[game_string::].find("\"")].split(" @ ")
	away_team = Teams[teams[0]]
	home_team = Teams[teams[1]]
	return [away_team,home_team]
	
def refsInGame(scan):
	'''Referees are in only one place in the entire file.'''
	location_of_Referees = scan.lower().find("referees")+len("referees: ")
	end_Of_Refs = scan[location_of_Referees::].lower().find("<")
	return  scan[location_of_Referees:location_of_Referees+end_Of_Refs].split(", ")
	
def getDateFromFile(scan):
	'''This is going to be very costly time wise but it's a way to implement it.'''
	tailOfDate = scan.find("</title>")
	frontOfDate = scan[tailOfDate:0:-1].find(" - ")-1
	return scan[tailOfDate-frontOfDate:tailOfDate]
	
def processPenalty(penalty):
	penalty = penalty.decode('unicode_escape').encode('ascii','ignore').split("\n")
	return penalty[1] #Returning the second index because that is where the actual penalty is stored.

def processData(scan):
	MasterPenaltyList = [] #So I can return this to the test framework
	
	teams = teamsPlaying(scan)
	referees = refsInGame(scan)
	date = getDateFromFile(scan)
	
			
	parser= MyHTMLParser() #Creates an instance of the HTML Parser class
	parser.feed(scan)
	
	inSection = False

	for i in range(0,len(GameData)):
		if(GameData[i] == "Penalty Summary" or inSection):
			inSection = True

			if(GameData[i] in Teams):
				playersTeam = Teams[GameData[i]]
				playersName = GameData[i+1]
				playersPenalty = processPenalty(GameData[i+2])
				
				if (playersTeam == teams[0]):
					location = False
					opponent = teams[1]
				else:
					location = True
					opponent = teams[0]
					
				newPenalty = Penalty(playersName, playersTeam, playersPenalty, location, opponent, date, referees)
				MasterPenaltyList.append(newPenalty)
			
		if("Stats" in GameData[i]):
			inSection = False
			
	return MasterPenaltyList	