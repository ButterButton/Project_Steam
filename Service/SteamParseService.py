from bs4 import BeautifulSoup
import requests

class SteamRankPageParseService:

    RankPageSoup = set()
    AppQuantity = 0
    AppUrlList = []
    AppIDList = []
    AppTypeList = []
    SmallPictureList = []
    AppNameList = []
    EvaluationList = []
    DiscountList = []
    OriginalPriceList = []
    DiscountPriceList = []


    def __init__(self , RankPageUrl):
        Result = requests.get(RankPageUrl)
        self.RankPageSoup = BeautifulSoup(Result.text, "html.parser")
        self.__SetAll()

    def __SetBaseInformation(self):
        # URL/ID/Type
        UrlResult = self.RankPageSoup.find_all("a", class_="search_result_row")

        for Url in UrlResult:
            self.AppUrlList.append(Url["href"])
            self.AppIDList.append(Url["href"].split("/")[4])
            self.AppTypeList.append(Url["href"].split("/")[3])


    def __SetAppSmallPicture(self):
        SmallPictureResult = self.RankPageSoup.find_all("div", class_="search_capsule")

        for Pic in SmallPictureResult:
            self.SmallPictureList.append(Pic.img["src"])

    def __SetAppName(self):
        AppNameResult = self.RankPageSoup.find_all("span", class_="title")

        for Name in AppNameResult:
            self.AppNameList.append(Name.get_text())

    def __SetAppEvaluation(self):
        AppEvaluationResult = self.RankPageSoup.select(".search_reviewscore")

        for Evaluation in AppEvaluationResult:
            if(Evaluation.find("span") == None):
                self.EvaluationList.append("尚無評價")
            else:
                self.EvaluationList.append(Evaluation.span["data-tooltip-html"])

    def __SetAppDiscount(self):
        AppDiscountResult = self.RankPageSoup.select(".search_discount")

        for AppDiscount in AppDiscountResult:
            if(AppDiscount.find("span") == None):
                self.DiscountList.append("No Disocunt")
            else:
                self.DiscountList.append(AppDiscount.find("span").get_text())

    def __SetAppOriginalAndDiscountPirce(self):
        AppPriceResult = self.RankPageSoup.find_all("div", class_ = "search_price")

        for AppPrice in AppPriceResult:
            if(AppPrice.find("span") == None):
                self.OriginalPriceList.append(AppPrice.get_text().strip())
                self.DiscountPriceList.append("")
            else:
                Length = len(AppPrice.get_text().split("NT$"))
                self.OriginalPriceList.append(AppPrice.find("strike").get_text())
                self.DiscountPriceList.append("NT$" + AppPrice.get_text().strip().split("NT$")[Length-1])

    def __SetAll(self):
        self.__SetBaseInformation()
        self.__SetAppSmallPicture()
        self.__SetAppName()
        self.__SetAppEvaluation()
        self.__SetAppDiscount()
        self.__SetAppOriginalAndDiscountPirce()
        self.AppQuantity = len(self.AppUrlList)

    def IsAllDataSetReady(self):

        Length = self.AppQuantity
        print("AppUrlList :" + str(Length))
        if(Length != len(self.SmallPictureList)):
            print("SmallPictureList :" + str(len(self.SmallPictureList)))
            return False
        if(Length != len(self.AppNameList)):
            print("AppNameList :" + str(len(self.AppNameList)))
            return False
        if(Length != len(self.EvaluationList)):
            print("EvaluationList :" + str(len(self.EvaluationList)))
            return False
        if(Length != len(self.DiscountList)):
            print("DiscountList :" + str(len(self.DiscountList)))
            return False
        if(Length != len(self.OriginalPriceList)):
            print("OriginalPriceList :" + str(len(self.OriginalPriceList)))
            return False
        if(Length != len(self.DiscountPriceList)):
            print("DiscountPriceList :" + str(len(self.DiscountPriceList)))
            return False
        
        
        return True

class SteamApplicationPageParseService:
    
    ApplicationPageSoup = set()
    ApplicationPageUrl = ""

    def __init__(self, ApplicationPageUrl):
        ApplicationPageResult = requests.get(ApplicationPageUrl)
        self.ApplicationPageUrl = ApplicationPageUrl
        self.ApplicationPageSoup = BeautifulSoup(ApplicationPageResult.text, "html.parser")

    def GetHeaderPicture(self, SmallPictureUrl):
        HeaderPictureUrl = ""
        ApplicationPageUrlSplit = self.ApplicationPageUrl.split("/")
        SmallPictureUrlSplit = SmallPictureUrl.split("/")

        if(SmallPictureUrl[4] == "bundles"):
            HeaderPictureUrl = "https://steamcdn-a.akamaihd.net/steam/" + SmallPictureUrlSplit[4] + "/"  + ApplicationPageUrlSplit[4] + "/" + SmallPictureUrlSplit[6] + "/header.jpg"
        else:
            HeaderPictureUrl = "https://steamcdn-a.akamaihd.net/steam/" + SmallPictureUrlSplit[4] + "/" + ApplicationPageUrlSplit[4] + "/header.jpg"
        
        return HeaderPictureUrl

    def GetScreenshot(self):
        ScreenshotUrl = ""
        ScreenshotResult = self.ApplicationPageSoup.find_all("a", class_ = "highlight_screenshot_link")

        # https://steamcdn-a.akamaihd.net/steam/apps/271590/ss_eb0a041f0699ad4c98c6ef2b8222c264e0435864.1920x1080.jpg?t=1544815097
        
        if(self.ApplicationPageUrl.split("/")[3] == "app"):
            for Screenshot in ScreenshotResult:
                ScreenshotUrl = ScreenshotUrl + Screenshot["href"].split("/")[6] + "/"
        
        return ScreenshotUrl

# test = SteamRankPageParseService("https://store.steampowered.com/search/?ignore_preferences=1&filter=topsellers&os=win&cc=TW&page=1")
# print(test.AppTypeList)
# test = SteamApplicationPageParseService("https://store.steampowered.com/app/271590/Grand_Theft_Auto_V/?snr=1_7_7_topsellers_150_1")
# shot = test.GetScreenshot()
# print(shot)

