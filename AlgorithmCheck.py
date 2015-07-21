import glob, time, os
from Penalty import *
from scanning_games import *
from TeamsCounter import *

MasterMasterList=[]
teamCheck = []

#Three teams ended up being as +1
# Nashville, Edmonton and Ottawa
nashville = []
edmonton = []
ottawa = []

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
		if "Nashville" in i.getTeam():
			nashville.append(i.printEvent())
		if "Ottawa" in i.getTeam():
			ottawa.append(i.printEvent())
		if "Edmonton" in i.getTeam():
			edmonton.append(i.printEvent())
		
print time.time()-startTime

print len(MasterMasterList)



'''Takes in the dictionaries, creates arrays and sorts them based on the number of infractions, most at the top.'''
unsorted_data = []
for l in TeamCounter:
	unsorted_data.append([l,TeamCounter[l]])
sorted_data = sorted(unsorted_data, key=lambda x: x[1], reverse=True)
for i in sorted_data:
	print i
	
#Printing Data on the three teams to figure out what is wrong
fileName = "Edmonton_Counted.txt"
file = open(fileName, 'w')
for j in edmonton:
	file.write(j + "\n")
file.close()