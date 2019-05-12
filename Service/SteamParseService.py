from bs4 import BeautifulSoup
import requests

class SteamRankPageParseService:

    RankPageSoup = set()
    AppUrlList = []
    SmallPictureList = []
    HeaderPictureList = []
    AppNameList = []
    EvaluationList = []
    DiscountList = []
    OriginalPriceList = []
    DiscountPriceList = []


    def __init__(self , RankPageUrl):
        Result = requests.get(RankPageUrl)
        self.RankPageSoup = BeautifulSoup(Result.text, "html.parser")

    def SetAppUrl(self):
        UrlResult = self.RankPageSoup.find_all("a", class_="search_result_row")

        for Url in UrlResult:
            print(Url["href"])
            self.AppUrlList.append(Url["href"])

    def SetAppSmallPicture(self):
        SmallPictureResult = self.RankPageSoup.find_all("div", class_="search_capsule")

        for Pic in SmallPictureResult:
            print(Pic.img["src"])
            self.SmallPictureList.append(Pic.img["src"])

    def SetAppName(self):
        AppNameResult = self.RankPageSoup.find_all("span", class_="title")

        for Name in AppNameResult:
            print(Name.get_text())
            self.AppNameList.append(Name.get_text())

    def SetAppEvaluation(self):
        AppEvaluationResult = self.RankPageSoup.select(".search_reviewscore")

        for Evaluation in AppEvaluationResult:
            if(Evaluation.find("span") == None):
                self.EvaluationList.append("尚無評價")
            else:
                self.EvaluationList.append(Evaluation.span["data-tooltip-html"])

        print(self.EvaluationList)

    def SetAppDiscount(self):
        AppDiscountResult = self.RankPageSoup.select(".search_discount")

        for AppDiscount in AppDiscountResult:
            if(AppDiscount.find("span") == None):
                self.DiscountList.append("No Disocunt")
            else:
                self.DiscountList.append(AppDiscount.find("span").get_text())
        
        print(self.DiscountList)

    def SetAppOriginalAndDiscountPirce(self):
        AppPriceResult = self.RankPageSoup.find_all("div", class_ = "search_price")

        for AppPrice in AppPriceResult:
            if(AppPrice.find("span") == None):
                self.OriginalPriceList.append(AppPrice.get_text().strip())
                self.DiscountPriceList.append("")
            else:
                Length = len(AppPrice.get_text().split("NT$"))
                self.OriginalPriceList.append(AppPrice.find("strike").get_text())
                self.DiscountPriceList.append("NT$" + AppPrice.get_text().strip().split("NT$")[Length-1])
        
        print(len(self.OriginalPriceList))
        print(len(self.DiscountPriceList))

    def SetAll(self):
        self.SetAppUrl()
        self.SetAppSmallPicture()
        self.SetAppName()
        self.SetAppEvaluation()
        self.SetAppDiscount()
        self.SetAppOriginalAndDiscountPirce()

class SteamApplicationPageParseService:
    
    ApplicationPageUrl = ""

    def __init__(self, ApplicationPageUrl):
        self.ApplicationPageUrl = ApplicationPageUrl

    def GetHeaderPicture(self, SmallPictureUrl):
        HeaderPictureUrl = ""
        ApplicationPageUrlSplit = self.ApplicationPageUrl.split("/")
        SmallPictureUrlSplit = SmallPictureUrl.split("/")

        if(SmallPictureUrl[4] == "bundles"):
            HeaderPictureUrl = "https://steamcdn-a.akamaihd.net/steam/" + SmallPictureUrlSplit[4] + "/"  + ApplicationPageUrlSplit[4] + "/" + SmallPictureUrlSplit[6] + "/header.jpg"
        else:
            HeaderPictureUrl = "https://steamcdn-a.akamaihd.net/steam/" + SmallPictureUrlSplit[4] + "/" + ApplicationPageUrlSplit[4] + "/header.jpg"
        
        return HeaderPictureUrl






TEST = SteamApplicationPageParseService("https://store.steampowered.com/app/271590/Grand_Theft_Auto_V/?snr=1_7_7_topsellers_150_1")
print(TEST.GetHeaderPicture("https://steamcdn-a.akamaihd.net/steam/apps/271590/capsule_sm_120.jpg?t=1544815097"))
