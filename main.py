from PenaltyTracker import PenaltyTracker

test = PenaltyTracker()
test.setDatabaseLocation("test.db")
test.setSeason("Playoffs")
test.setTargetDate("2022-06-11")
testValue = test.run()