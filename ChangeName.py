from DatabaseManager import *
import sys

# Lifting this from the PenaltyTracker
if __name__=="__main__":
    if len(sys.argv) == 2:
        dbLoc = sys.argv[1]
        dbManager = DatabaseManager(dbLoc)
        dbManager.executeCommand("ALTER TABLE PenaltyTracker RENAME TO Regular_16_17")
        dbManager.executeCommand("ALTER TABLE Playoffs RENAME TO Playoffs_16_17")
