import mysql.connector
import configparser

class DataBaseService:
    
    def GetDataBase(self):
        ConfigFile = configparser.ConfigParser()
        ConfigFile.read("Service\config.py")
        DB = mysql.connector.connect(
            host = ConfigFile["DBProject_Steam"]["Host"],
            port =ConfigFile["DBProject_Steam"]["Port"],
            user = ConfigFile["DBProject_Steam"]["User"],
            passwd = ConfigFile["DBProject_Steam"]["Passwd"],
            database = ConfigFile["DBProject_Steam"]["Name"]
        )

        return DB


# test = DataBaseService()
# DB = test.GetDataBase()
# print(type(DB))