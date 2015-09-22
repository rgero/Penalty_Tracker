'''
	This program was written by Roy W. Gero.
	If you have questions, comments or concerns please contact him on GitHub
'''

class Penalty:
	def __init__(self, player, team, penalty, side, opponent, date, referees):
		self.name = player
		self.team = team
		self.penalty = penalty
		
		if (type(side) == bool):
			self.side = side
		else:
			raise TypeError("Location unable to be determined")
			
		self.opponent = opponent
		self.date = date
		
		if type(referees) is list:
			self.refs = referees
		else:
			raise TypeError("Referees are not passed in as list")
		
	def getPlayer(self):
		return self.name
	
	def getTeam(self):
		return self.team
	
	def getPenalty(self):
		return self.penalty
	
	def getSide(self):
		if (self.side):
			return "Home"
		else:
			return "Away"
	
	def getOpponent(self):
		return self.opponent
	
	def getDate(self):
		return self.date
	
	def getRefs(self):
		return self.refs
		
	def getRefsAsString(self):
		refereeString = ""
		for i in self.refs:
			refereeString += i + ", "
		refereeString = refereeString[0:len(refereeString)-2]
		return refereeString
	
	def printEvent(self):
		entry = self.name + " | " + self.team + " | " + self.penalty + " | " + self.date + " | " + self.opponent + " | " + self.getSide() + " | " + self.getRefsAsString()
		return entry
	
	#Adding a new function to print as a table.
	def printTable(self):
		entry = "<tr><td>" + self.name + "<//td><td>" + self.team + "<//td><td>" + self.penalty + "<//td><td>" + self.date + "<//td><td>" + self.opponent + "<//td><td>" + self.getSide() + "<//td><td>" + self.getRefsAsString() + "<//td><//tr>"
		return entry