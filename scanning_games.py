from HTMLParser import HTMLParser
from Teams import *
from Penalty import *


class MyHTMLParser(HTMLParser):
	'''This generates an Array with all the HTML elements so I can quickly sort through it.'''	
	#def handle_data(self, data):
	
	
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

def processFile(file):
	data = open(file,"r")
	scan = data.read()
	
	teams = teamsPlaying(scan)
	referees = refsInGame(scan)
	
	
	
	
	
	
	#parser = MyHTMLParser()
	#parser.feed(scan)
	
	
file = "Testing.htm"
processFile(file)