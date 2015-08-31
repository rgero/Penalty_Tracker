import glob, time, os
from Penalty import *
from scanning_games import *
from TeamsCounter import *

MasterMasterList=[]
teamCheck = []

startTime = time.time()
for filename in glob.iglob('C:\\TestingData\\GameLogs\*\*.htm'): #This will iterate through every folder and file
	pathway = os.path.dirname(os.path.realpath(filename))
	index_path = pathway.find("GameLogs\\") + len("GameLogs\\") #Figures out the date based on the file structure
	date = pathway[index_path::]
	file = open(filename,"r")
	scan = file.read()
	temporaryStorage = processData(scan)
	for i in temporaryStorage:
		MasterMasterList.append(i)
		TeamCounter[i.getTeam()] += 1

		
print time.time()-startTime

print len(MasterMasterList)



'''Takes in the dictionaries, creates arrays and sorts them based on the number of infractions, most at the top.'''
unsorted_data = []
for l in TeamCounter:
	unsorted_data.append([l,TeamCounter[l]])
sorted_data = sorted(unsorted_data, key=lambda x: x[1], reverse=True)
for i in sorted_data:
	print i

	
#HEALTH CHECK
testingFile = open("TestingDocs\Tested.txt","r")
PenaltyList = processFromFile(testingFile)
for i in PenaltyList:
	print i.printEvent()