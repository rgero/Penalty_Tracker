'''
  This program was written by Roy W. Gero.
  If you have questions, comments or concerns please contact him on GitHub
'''
import unittest

from Tests.PenaltyTests import TestingPenaltyClass
from Tests.PenaltyTrackerTests import TestingPenaltyTracker

print("Testing the class constructor and get functions.")
print("--------------------------------------------------------")
penaltyClassSuite = unittest.TestLoader().loadTestsFromTestCase(TestingPenaltyClass)
unittest.TextTestRunner(verbosity=2).run(penaltyClassSuite)

print("Testing the Penalty Tracker")
print("--------------------------------------------------------")
penaltyTrackerSuite = unittest.TestLoader().loadTestsFromTestCase(TestingPenaltyTracker)
unittest.TextTestRunner(verbosity=2).run(penaltyTrackerSuite)
