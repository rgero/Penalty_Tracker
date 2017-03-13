''' Data Checker
'''

import sys

def organizeDataDump(file):
    teamDump = {}
    with open(file,'r') as F:
        for line in F:
            data = line.split(',')[1].replace('"','')
            if data.lower() != "team name":
                data = data.split(" ")
                data = data[len(data)-1]
                if data in teamDump:
                    teamDump[data]+=1
                else:
                    teamDump[data]=1
    return teamDump
        
def processNHLData(file):
    nhlData = {}
    teamColumn = -1
    penaltyColumn = -1
    with open(file,'r') as F:
        for line in F:
            if (teamColumn == -1) or (penaltyColumn == -1):
                data = line.split(',')
                for col in range(0,len(data)):
                    if data[col].lower().find("team") != -1:
                        teamColumn = col
                    if data[col].lower().find("pen") != -1:
                        penaltyColumn = col                    
            else:
                data = line.split(',')
                team = data[teamColumn].split(' ')
                team = team[len(team)-1]
                penaltyTotal = data[penaltyColumn]
                nhlData[team] = penaltyTotal
    return nhlData

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("You need two additional arguments")
        print("The first one is the CSV Spreadsheet saved from the NHL Website")
        print("The second one is the CSV Data Dump from Roymond.net")
        sys.exit(-1)
    else:
        issueTeams = {}
        nhlFile = sys.argv[1]
        rFile = sys.argv[2]
        rData = organizeDataDump(rFile)
        nhlData = processNHLData(nhlFile)
        for i in nhlData:
            if int(nhlData[i]) != int(rData[i]):
                issueTeams[i] = int(nhlData[i])-int(rData[i])
        if len(issueTeams) != 0:
            print("Error! There is a difference between the NHL Data and Roymond Data")
            print("Team\t:\tDifference")
            for i in issueTeams:
                print(i + "\t: \t" + str(issueTeams[i]))
        else:
            print("Everything is Fine")