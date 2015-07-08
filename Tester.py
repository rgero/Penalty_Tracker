from Penalty import *
from scanning_games import *
import unittest

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

		
class TestingSGMethods(unittest.TestCase):
	def testTeamsPlaying(self):
		self.assertEqual(teamsPlaying(scan),["Montreal Canadiens", "Toronto Maple Leafs"])
	
	def testRefsInGame(self):
		self.assertEqual(refsInGame(scan),["Paul Devorski", "Tom Kowal"])


		
'''
// Setting up Data
'''	
		
event = Penalty("Roy Gero","Colorado Avalanche","Too Much Man","Home","Calgary Flames","July 8, 2015","Don","Ron")

#Setting up a dummy file
file_name = "Testing.htm"
file = open(file_name,'r')
scan = file.read()

	  
print "Testing the class constructor and get functions. (7 Tests)"
print "--------------------------------------------------------"
penaltyClassSuite = unittest.TestLoader().loadTestsFromTestCase(TestingPenaltyClass)
unittest.TextTestRunner(verbosity=2).run(penaltyClassSuite)

print "\nTesting the functions in scanning_games using \"" + file_name + "\""
print "--------------------------------------------------------"
sgFileSuite = unittest.TestLoader().loadTestsFromTestCase(TestingSGMethods)
unittest.TextTestRunner(verbosity=2).run(sgFileSuite)