from PenaltyTracker import PenaltyTracker
from DatabaseManager import DatabaseManager
import unittest,os,sys,shutil, filecmp

class TestingPenaltyTracker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testPTDatabase = os.path.join( os.getcwd(), "Tests", "test_penalty.db")
        cls.testPenaltyTracker = PenaltyTracker()
        cls.testPenaltyTracker.setDatabaseLocation(cls.testPTDatabase)
        cls.testPenaltyTracker.setSeason("PenaltyTracker")
        cls.testPenaltyTracker.createAndSetDatabaseManager()

        controlPath = os.path.join(os.getcwd(), "Tests", "season_test_10-24-16.db")
        cls.controlDatabase = DatabaseManager(controlPath, "PenaltyTracker")

    @classmethod
    def tearDownClass(cls):
        cls.testPenaltyTracker = None
        cls.controlDatabase = None
        os.remove( os.path.join( os.getcwd(), "Tests", "test_penalty.db") )

    def testGameUrls(self):
        self.testPenaltyTracker.setTargetDate("2016-02-26")
        numberOfGames = len( self.testPenaltyTracker.GetGameURLS() )
        self.assertEqual( numberOfGames, 5 )

    def testSetDBLocation(self):
        self.assertNotEqual(self.testPenaltyTracker.databaseManager, None )

    def testPenaltyProcessing(self):
        # generate the test data
        self.testPenaltyTracker.setTargetDate("2016-10-24") 
        self.testPenaltyTracker.run();

        self.assertEqual( self.controlDatabase.getHighestID(), self.testPenaltyTracker.databaseManager.getHighestID() )
        
        getAllCommand = "SELECT * FROM PenaltyTracker"
        controlRows = self.controlDatabase.getData(getAllCommand)
        testRows = self.testPenaltyTracker.databaseManager.getData(getAllCommand)
        self.assertEqual(controlRows, testRows)


