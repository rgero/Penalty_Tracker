import sqlite3, os

class DatabaseManager:
  cursor = None
  conn = None
  location = None

  def __init__(self, location):
    self.location = location  
    if not os.path.isfile(self.location): #If the file doesn't exist we need to create the table
      self.openConnection()
      self.createTable()
    else:
      self.openConnection()
   
    
    
  def openConnection(self):
    self.conn = sqlite3.connect(self.location)
    self.cursor = self.conn.cursor()
    
  def getHighestID(self):
    value = self.cursor.execute("SELECT MAX(id) FROM PenaltyTracker").fetchone()[0]
    if (value == None):
      value = 0  
    return value
  
  def createTable(self):
    self.cursor.execute('''create table if not exists PenaltyTracker ( 
                    id integer not null primary key autoincrement,
                    playerName varchar(150),
                    teamName varchar(100),
                    penalty varchar(100),
                    gameDate date,
                    opponentTeam varchar(100),
                    homeAway bit,  /* 0 is home, 1 is away. */
                    refs varchar(250)
                  );
              '''
    )
    
  def executeCommand(self, inputString):
    self.cursor.execute(inputString)
    self.conn.commit()
  
  def insertData(self, inputString):
    id = self.getHighestID() + 1
    inputCommand = "INSERT INTO PenaltyTracker VALUES (" + str(id) + "," + inputString + ");"
    self.executeCommand(inputCommand)