'''
  This program was written by Roy W. Gero.
  If you have questions, comments or concerns please contact him on GitHub
'''

from Penalty import *
from PenaltyTracker import *
import unittest,os,sys,shutil, filecmp

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

class TestingPenaltyTracker(unittest.TestCase):
  def testGameUrls(self):
    numberOfGames = len( getData("2016-02-26") )
    self.assertEqual( numberOfGames, 5 )

  def testPenaltyProcessing(self):
    if os.path.exists( os.path.join( os.getcwd(), "test_penalty.db") ):
        os.remove( os.path.join( os.getcwd(), "test_penalty.db") )
    run(dbLoc="test_penalty.db", date="2016-10-24")
    # Compares the data. Need to investigate this. Right now the test will just pass if this code executes.
    os.remove( os.path.join( os.getcwd(), "test_penalty.db") )

'''
// Setting up Data
'''
os.system("cls")
event = Penalty("Roy Gero","Colorado Avalanche","Too Many Men",True,"Calgary Flames","July 8, 2015",["Don","Ron"])



print("Testing the class constructor and get functions.")
print("--------------------------------------------------------")
penaltyClassSuite = unittest.TestLoader().loadTestsFromTestCase(TestingPenaltyClass)
unittest.TextTestRunner(verbosity=2).run(penaltyClassSuite)

print("")
print("Testing the Penalty Tracker")
print("--------------------------------------------------------")
penaltyTrackerSuite = unittest.TestLoader().loadTestsFromTestCase(TestingPenaltyTracker)
unittest.TextTestRunner(verbosity=2).run(penaltyTrackerSuite)
