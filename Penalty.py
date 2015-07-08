class Penalty:
    def __init__(self, player, team, penalty, side, opponent, date, ref1, ref2):
        self.playerName = player
        self.playerTeam = team
        self.penalty = penalty
        self.side = side
        self.opponent = opponent
        self.date = date
        self.ref1 = ref1
        self.ref2 = ref2
        
    def getPlayer(self):
        return self.playerName
    
    def getTeam(self):
        return self.playerTeam
    
    def getPenalty(self):
        return self.penalty
    
    def getSide(self):
        return self.side
    
    def getOpponent(self):
        return self.opponent
    
    def getDate(self):
        return self.date
    
    def getRefs(self):
        return [self.ref1,self.ref2]
    