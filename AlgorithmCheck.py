import glob, time, os
from Penalty import *
from scanning_games import *


startTime = time.time()
for filename in glob.iglob('GameLogs\*\*.htm'): #This will iterate through every folder and file
	pathway = os.path.dirname(os.path.realpath(filename))
	print filename
	index_path = pathway.find("GameLogs\\") + len("GameLogs\\") #Figures out the date based on the file structure
	date = pathway[index_path::]
	file = open(filename,"r")
	scan = file.read()
	dontCare = processData(scan)
print time.time()-startTime