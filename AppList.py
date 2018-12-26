from flask import Flask
import requests
from bs4 import BeautifulSoup
import datetime
import json

app = Flask(__name__)

@app.route("/")
def index():
    res = requests.get("https://store.steampowered.com/search/?filter=topsellers&os=win&ignore_preferences=1")
    soup = BeautifulSoup(res.text, 'html.parser')
    GameList = {
        "type" : "topseller",
	    "datetime" : datetime.datetime.now().date().strftime("%Y-%m-%d"),
	    "total_app" : 0,
	    "startrank" : 0,
        "endtrank" : 0,
        "applications" : []
    }
    HTMLAppInfo = soup.find_all("a", class_="search_result_row")
    HTMLAppPic = soup.find_all("div", class_="search_capsule")
    HTMLAppName = soup.find_all("span", class_="title")
    HTMLAppEval = soup.find_all("span", class_="search_review_summary")
    HTMLAppDis = soup.select(".search_discount")
    HTMLAppPrice = soup.find_all("div", class_="search_price")

    i = 0
    tempapplist = []
    
    for item in HTMLAppInfo:
        application = {}
        # 網址
        link = item["href"]
        applink = link.split("/")
        application["steam_link"] = link
        application["app_id"] = applink[4]
        application["small_pic"] = GetAppSmPic(HTMLAppPic)[i]
        application["app_name"] = GetAppName(HTMLAppName)[i]
        application["evaluation"] = GetAppEval(HTMLAppEval)[i]
        application["discount"] = GetAppDis(HTMLAppDis)[i]
        application["original_price"] = GetAppOrgPrice(HTMLAppPrice)[i]
        application["discount_price"] = GetAppDisPrice(HTMLAppPrice)[i]
        i = i + 1
        application["rank"] = i
        tempapplist.append(application)

    GameList["applications"] = tempapplist
    print(json.dumps(GameList, indent=4, sort_keys=True))
    return "Success"

def GetAppSmPic(HtmlAppPic):
    PicList = []

    for Pic in HtmlAppPic:
        PicList.append(Pic.img["src"])
    
    return PicList

def GetAppName(HtmlAppName):
    NameList = []

    for Name in HtmlAppName:
        NameList.append(Name.get_text())

    return NameList

def GetAppEval(HtmlAppEval):
    EvalList = []

    for Eval in HtmlAppEval:
        EvalList.append(Eval["data-tooltip-html"])
    
    return EvalList

def GetAppDis(HtmlAppDis):
    DisList = []

    for Dis in HtmlAppDis:
        if(Dis.find("span") == None):
            DisList.append("No Discount")
        else:
            DisList.append(Dis.find("span").get_text())
           
    return DisList

def GetAppOrgPrice(HtmlAppPrice):
    OrgPriceList = []

    for Price in HtmlAppPrice:
        if(Price.find("span") == None):        
            OrgPriceList.append(Price.get_text().strip())
        else:
            OrgPriceList.append("NT$" + Price.get_text().split("NT$")[1])

    return OrgPriceList

def GetAppDisPrice(HtmlAppPrice):
    DisPriceList = []

    for Price in HtmlAppPrice:
        if(Price.find("span") == None):        
            DisPriceList.append("")
        else:
            DisPriceList.append("NT$" + Price.get_text().strip().split("NT$")[2])

    return DisPriceList



if __name__ == "__main__":
    app.run(debug=True)