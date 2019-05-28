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
    ApplicationsList = DBService.QuerySelect(DateTimeToday)

    print(ApplicationsList)
    
    return "Success"

if __name__ == "__main__":
    app.run(debug=True)