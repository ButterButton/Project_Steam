from flask import Flask
from flask import Response
from flask_cors import CORS
from Service.DataBaseService import DataBaseService
import pytz
import datetime
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Welcome To Mono SteamRankAPI"

def GetTimeNow_Taipei():
    TimeNow = datetime.datetime.now()
    TimeNowTaipei = TimeNow.astimezone(pytz.timezone('Asia/Taipei'))

    return TimeNowTaipei
    
@app.route("/Time", methods=["GET"])
def GetTimeNow():
    return GetTimeNow_Taipei().strftime("%Y-%m-%d %H:%M:%S")


def GetAppList():
    DateTimeToday = GetTimeNow_Taipei().strftime("%Y-%m-%d")
    SteamRank = GetQueryTimeAppList(DateTimeToday)
    
    return SteamRank


@app.route("/Apps/Today", methods=["GET"])
def TodayData():   
    return Response(json.dumps(GetAppList(), ensure_ascii=False), mimetype='text/json')

@app.route("/Test/TodayFormated", methods=["GET"])
def GetTodayAppList():  
    return Response(json.dumps(GetAppList(), ensure_ascii=False, indent=4), mimetype='text/json')

def GetQueryTimeAppList(DateTimeToday):
    DBService = DataBaseService()
    QueryData = DBService.QueryDateSelectAll(DateTimeToday)
    QueryDiscountAppQuantity = DBService.QueryDiscountCount(DateTimeToday)

    IsHaveData = False
    ApplicationList = []
    SteamRank = {
        "IsSuccess": False,
        "type": "",
        "datetime": DateTimeToday,
        "total_app": 0,
        "discount_app_quantity": 0,
        "applications": []
    }

    if(QueryData == []):
        return SteamRank

    for App in QueryData:
        ScreenshotList = []
        ScreenshotUrlList = App[14].split("/")
        ScreenshotUrlList.remove("")

        for Url in ScreenshotUrlList:
            ScreenshotList.append("https://steamcdn-a.akamaihd.net/steam/" + App[4] + "s/" + str(App[2]) + "/" + Url)

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
            "screenshot_list": ScreenshotList,
        }

        ApplicationList.append(Application)

    TotalQuantity = len(ApplicationList)

    if(TotalQuantity > 0 and TotalQuantity == len(QueryData)):
        IsHaveData = True

    SteamRank["IsSuccess"] = IsHaveData
    SteamRank["Type"] = QueryData[0][1]
    SteamRank["datetime"] = DateTimeToday
    SteamRank["total_app"] = TotalQuantity
    SteamRank["applications"] = ApplicationList
    SteamRank["discount_app_quantity"] = QueryDiscountAppQuantity[0]

    return SteamRank
 
if __name__ == "__main__":
    app.run(debug=True)

