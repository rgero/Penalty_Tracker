'''
	This program was written by Roy W. Gero.
	If you have questions, comments or concerns please contact him on GitHub
'''

from HTMLParser import HTMLParser
from Teams import *
from Penalty import *

GameData = []
GamePenaltyList = [] #So I can return this to the test framework

class MyHTMLParser(HTMLParser):
	'''This generates an Array with all the HTML elements so I can quickly sort through it.'''	
	def handle_data(self, data):
		GameData.append(data)
		
def clearLists():
	'''This is going to make sure that the both lists are cleared so that way I can guarentee to get all the correct data.'''
	GameData[:] = []
	GamePenaltyList[:] = []
	return GameData, GamePenaltyList
	
	
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
	'''	This is necessary because of the fact that the NHL website uses &nbsp spaces, which gets parsed differently when processing the file.
		So I added this to make sure that I get the penalties correctly formatted.
	'''
	penalty = penalty.decode('unicode_escape').encode('ascii','ignore').split("\n")
	return penalty[1] #Returning the second index because that is where the actual penalty is stored.
	
def processFromFile(scan):
	'''	This might need to be moved to a different file.
		This would be because of the fact that this should be processing the text file
		and working for ALL games in the text file. This section of the code is for every
		instance of a game.
	'''
	GamePenaltyList = []
	for i in scan:
		i = i.rstrip("\n")
		event = i.split(" | ")
		event[6] = event[6].split(", ")
		newPenalty = Penalty(event[0],event[1],event[2],"Home" in event[5],event[4],event[3],event[6])
		GamePenaltyList.append(newPenalty)
	return GamePenaltyList

def processData(scan):
	'''Processes the file which has been opened and read into a variable.
	scan is the file data
	returns: List of Penalty objects.
	'''
	GamePenaltyList = []
	
	GameData,GamePenaltyList = clearLists()
	
	teams = teamsPlaying(scan)
	referees = refsInGame(scan)
	date = getDateFromFile(scan)
			
	parser= MyHTMLParser() #Creates an instance of the HTML Parser class
	parser.feed(scan)
	
	#Establishing two boolean variables. inSection means that we're in the penalty section. startedProcessing makes it so that way we don't find any false positives for "Stats"
	inSection = False
	startedProcessing = False
	
	for i in range(0,len(GameData)):
		if(GameData[i] == "Penalty Summary" or inSection):
			startedProcessing = True
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
				GamePenaltyList.append(newPenalty)
			
		if("Stats" in GameData[i] and startedProcessing):
			inSection = False
			break #Once we find the end of the penalty section, we can ignore the rest of the file
	return GamePenaltyList
	