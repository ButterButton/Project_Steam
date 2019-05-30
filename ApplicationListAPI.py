from flask import Flask
from flask import Response
from flask_cors import CORS
from Service.DataBaseService import DataBaseService
import datetime
import json

app = Flask(__name__)
CORS(app)

@app.route("/GetApps/Today")
def TodayData():
    DateTimeToday = datetime.datetime.now().strftime("%Y-%m-%d")
    DBService = DataBaseService()
    QueryApplicationsList = DBService.QueryDateSelectAll("2019-05-30")
    IsHaveData = False
    TotalQuantity = len(QueryApplicationsList)
    ApplicationList = []

    if(TotalQuantity > 0):
        IsHaveData = True


    SteamRank = {
        "IsSuccess": IsHaveData,
        "Type": QueryApplicationsList[0][1],
        "datetime": (QueryApplicationsList[0][0]).strftime("%Y-%m-%d"),
        "total_app": TotalQuantity,
        "applications":[]
    }

    for App in QueryApplicationsList:
        Application = {
            "steam_link": App[9],
            "app_id": App[2],
            "app_typ": App[4],
            "small_pic": App[10],
            "header_pic": App[11],
            "app_name": App[3],
            "evaluation": App[5],
            "discount": App[8],
            "original_price": App[6],
            "discount_price": App[7],
            "page": App[12],
            "rank": App[13],
            "screenshot_list": [],
        }
        ApplicationList.append(Application)

    print(ApplicationList[0])
    
    return "Success"

 
if __name__ == "__main__":
    app.run(debug=True)