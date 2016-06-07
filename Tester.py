'''
	This program was written by Roy W. Gero.
	If you have questions, comments or concerns please contact him on GitHub
'''

from Penalty import *
from PenaltyTracker import *
import unittest,os,sys,shutil

class TestingPenaltyClass(unittest.TestCase):
	def testPlayerName(self):
		self.assertEqual(event.getPlayer(), "Roy Gero")
		
	def testPlayerTeam(self):
		self.assertEqual(event.getTeam(), "Colorado Avalanche")
		
	def testPenalty(self):
		self.assertEqual(event.getPenalty(), "Too Many Men")
	
	def testSide(self):
		self.assertEqual(event.getSide(), "Home")
		
	def testOpponent(self):
		self.assertEqual(event.getOpponent(), "Calgary Flames")
		
	def testDate(self):
		self.assertEqual(event.getDate(), "July 8, 2015")
	
	def testRef(self):
		self.assertEqual(event.getRefs(), ["Don","Ron"])
		
	def testPrint(self):
		self.assertEqual(event.printEvent(),"Roy Gero | Colorado Avalanche | Too Many Men | July 8, 2015 | Calgary Flames | Home | Don, Ron")
		
	def testTablePrint(self):
		self.assertEqual(event.printTable(),"<tr><td>Roy Gero<//td><td>Colorado Avalanche<//td><td>Too Many Men<//td><td>July 8, 2015<//td><td>Calgary Flames<//td><td>Home<//td><td>Don, Ron<//td><//tr>")
        
class TestingPenaltyTracker(unittest.TestCase):
    def testGameUrls(self):
        numberOfGames = len( getData("2016-02-26") )
        self.assertEqual( numberOfGames, 5 )
        
    def testPenaltyProcessing(self):
        testGameList = getData("2016-02-26")
        penaltyString = ""
        for game in testGameList:
            penaltyList = processGame(game, "2016-02-26")
            penaltyString += getPenaltyListAsString(penaltyList)
        file = open('.\TestingDocs\TestList.txt','r')
        testedData = file.read()
        self.assertEqual(testedData, penaltyString)
        
	

		

'''
// Setting up Data
'''	
os.system("cls")		
event = Penalty("Roy Gero","Colorado Avalanche","Too Many Men",True,"Calgary Flames","July 8, 2015",["Don","Ron"])


	  
print "Testing the class constructor and get functions."
print "--------------------------------------------------------"
penaltyClassSuite = unittest.TestLoader().loadTestsFromTestCase(TestingPenaltyClass)
unittest.TextTestRunner(verbosity=2).run(penaltyClassSuite)

print ""
print "Testing the Penalty Tracker"
print "--------------------------------------------------------"
penaltyTrackerSuite = unittest.TestLoader().loadTestsFromTestCase(TestingPenaltyTracker)
unittest.TextTestRunner(verbosity=2).run(penaltyTrackerSuite)