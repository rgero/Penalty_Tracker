import sqlite3, os

class DatabaseManager:
  cursor = None
  conn = None
  location = None
  tableName = None

  def __init__(self, location, tableName):
    self.location = location
    self.tableName = tableName
    if not os.path.isfile(self.location): #If the file doesn't exist we need to create the table
      self.openConnection()
      self.createTable(tableName)
    else:
      self.openConnection()
      if not self.checkTable(self.tableName):
          self.createTable(self.tableName)

  def openConnection(self):
    self.conn = sqlite3.connect(self.location)
    self.cursor = self.conn.cursor()


  def checkTable(self, tableName):
    '''Checks the Database for the existence of a table. It will return True if the table exists'''
    value = self.cursor.execute("select count(type) from sqlite_master where type = 'table' and name = '" + tableName + "'").fetchone()[0]
    if value == 1:
        return True
    else:
        return False

  def getHighestID(self):
    value = self.cursor.execute("SELECT MAX(id) FROM " + self.tableName).fetchone()[0]
    if (value == None):
      value = 0
    return value

  def createTable(self, tableName):
    self.cursor.execute('''create table if not exists ''' + tableName + ''' (
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
    inputCommand = "INSERT INTO " + self.tableName + " VALUES (" + str(id) + "," + inputString + ");"
    self.executeCommand(inputCommand)
