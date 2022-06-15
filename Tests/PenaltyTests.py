import unittest
from Penalty import Penalty

class TestingPenaltyClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.event = Penalty("Roy Gero","Colorado Avalanche","Too Many Men",True,"Calgary Flames","July 8, 2015",["Don","Ron"])

    def testPlayerName(self):
        self.assertEqual(self.event.getPlayer(), "Roy Gero")

    def testPlayerTeam(self):
        self.assertEqual(self.event.getTeam(), "Colorado Avalanche")

    def testPenalty(self):
        self.assertEqual(self.event.getPenalty(), "Too Many Men")

    def testSide(self):
        self.assertEqual(self.event.getSide(), "Home")

    def testOpponent(self):
        self.assertEqual(self.event.getOpponent(), "Calgary Flames")

    def testDate(self):
        self.assertEqual(self.event.getDate(), "July 8, 2015")

    def testRef(self):
        self.assertEqual(self.event.getRefs(), ["Don","Ron"])

    def testPrint(self):
        self.assertEqual(self.event.getEventAsString(),"Roy Gero | Colorado Avalanche | Too Many Men | July 8, 2015 | Calgary Flames | Home | Don, Ron")