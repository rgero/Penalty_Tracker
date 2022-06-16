from PenaltyTracker import PenaltyTracker

test = PenaltyTracker()
test.setDatabaseLocation("test.db")
test.setSeason("Playoffs")
test.setDateRange("2022-02-01", "2022-02-28")
testValue = test.run()