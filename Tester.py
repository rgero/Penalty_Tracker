from Penalty import *
from scanning_games import *
import unittest
import os,sys

class TestingPenaltyClass(unittest.TestCase):
	def testPlayerName(self):
		self.assertEqual(event.getPlayer(), "Roy Gero")
		
	def testPlayerTeam(self):
		self.assertEqual(event.getTeam(), "Colorado Avalanche")
		
	def testPenalty(self):
		self.assertEqual(event.getPenalty(), "Too Much Man")
	
	def testSide(self):
		self.assertEqual(event.getSide(), "Home")
		
	def testOpponent(self):
		self.assertEqual(event.getOpponent(), "Calgary Flames")
		
	def testDate(self):
		self.assertEqual(event.getDate(), "July 8, 2015")
	
	def testRef(self):
		self.assertEqual(event.getRefs(), ["Don","Ron"])
		
	def testPrint(self):
		self.assertEqual(event.printEvent(),"Roy Gero | Colorado Avalanche | Too Much Man | July 8, 2015 | Calgary Flames | Home | Don, Ron")
	

		
class TestingSGMethods(unittest.TestCase):
	def testTeamsPlaying(self):
		self.assertEqual(teamsPlaying(scan),["Montreal Canadiens", "Toronto Maple Leafs"])
	
	def testRefsInGame(self):
		self.assertEqual(refsInGame(scan),["Paul Devorski", "Tom Kowal"])
	
	def testDate(self):
		self.assertEqual(getDateFromFile(scan),"10/08/2014")
		
	def testProcessFile(self):
		self.assertEqual(len(processData(scan)),4)
		
	def testingProcessingFromFile(self):
		procedurallyGenerated = processData(scan)
		testingFile = open("TestingDocs\ProcessingFromFileTest.txt","r")
		readingFromFile = processFromFile(testingFile)
		self.assertEqual(len(procedurallyGenerated), len(readingFromFile))
		for i in range(0,len(procedurallyGenerated)):
			pG = procedurallyGenerated[i]
			fF = readingFromFile[i]
			self.assertTrue(pG.getPlayer()==fF.getPlayer(), pG.getPlayer() + " : " + fF.getPlayer() + " in entry " + str(i))
			self.assertTrue(pG.getTeam()==fF.getTeam(), pG.getTeam() + " : " + fF.getTeam() + " in entry " + str(i))
			self.assertTrue(pG.getPenalty()==fF.getPenalty(), pG.getPenalty() + " : " + fF.getPenalty() + " in entry " + str(i))
			self.assertTrue(pG.getSide()==fF.getSide(), pG.getSide() + " : " + 
				fF.getSide() + " in entry " + str(i))
			self.assertTrue(pG.getOpponent()==fF.getOpponent(), pG.getOpponent() + " : " + 
				fF.getOpponent() + " in entry " + str(i))
			self.assertTrue(pG.getDate()==fF.getDate(), pG.getDate() + " : " + 
				fF.getDate() + " in entry " + str(i))
			self.assertTrue(pG.getRefsAsString()==fF.getRefsAsString(), pG.getRefsAsString() + " : " + fF.getRefsAsString() + " in entry " + str(i))
	

		
'''
// Setting up Data
'''	
os.system("cls")		
event = Penalty("Roy Gero","Colorado Avalanche","Too Much Man",True,"Calgary Flames","July 8, 2015",["Don","Ron"])

#Setting up a dummy file
file_name = "TestingDocs\\Testing.htm"
file = open(file_name,'r')
scan = file.read()

	  
print "Testing the class constructor and get functions. (8 Tests)"
print "--------------------------------------------------------"
penaltyClassSuite = unittest.TestLoader().loadTestsFromTestCase(TestingPenaltyClass)
unittest.TextTestRunner(verbosity=2).run(penaltyClassSuite)

print "\nTesting the functions in scanning_games using \"" + file_name + "\""
print "--------------------------------------------------------"
sgFileSuite = unittest.TestLoader().loadTestsFromTestCase(TestingSGMethods)
unittest.TextTestRunner(verbosity=2).run(sgFileSuite)