import mysql.connector
import configparser

class DataBaseService:
    
    def GetDataBase(self):
        ConfigFile = configparser.ConfigParser()
        ConfigFile.read("Service/config.py")
        DB = mysql.connector.connect(
            host = ConfigFile["DBProject_Steam"]["Host"],
            port =ConfigFile["DBProject_Steam"]["Port"],
            user = ConfigFile["DBProject_Steam"]["User"],
            passwd = ConfigFile["DBProject_Steam"]["Passwd"],
            database = ConfigFile["DBProject_Steam"]["Name"]
        )

        return DB

    def QueryDateSelectAll(self, QueryDate):
        DBService = self.GetDataBase()
        DBCursor = DBService.cursor()
        SelectQuery = "SELECT * FROM Application WHERE UpdateDateTime = '%s'"

        DBCursor.execute(SelectQuery % QueryDate)
        Result = DBCursor.fetchall()

        return Result
    
    def QueryDateSelectOne(self, QueryDate):
        DBService = self.GetDataBase()
        DBCursor = DBService.cursor()
        SelectQuery = "SELECT * FROM Application WHERE UpdateDateTime = '%s' LIMIT 1"

        DBCursor.execute(SelectQuery % QueryDate)
        Result = DBCursor.fetchall()

        return Result

# test = DataBaseService()
# for t in test.QuerySelect("2019-05-28"):
#     print(t)