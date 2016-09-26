from DatabaseManager import *
from Penalty import *
import os

if os.path.isfile("test.db"):
  os.remove("test.db")

databaseManager = DatabaseManager("test.db")


for i in range(0,10):
  databaseManager.insertData("'Roy Gero','Boston','Hooking','09-26-2016','Montreal',0,'Steve'")

print databaseManager.getHighestID()

event = Penalty("Claude McSlash","Boston Bruins","Slashing",True,"Calgary Flames","July 10, 2015",["Don","Ron"])

databaseManager.insertData(event.formatForSQL())