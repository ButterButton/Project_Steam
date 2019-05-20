
from Service.SteamParseService import *
from Service.DataBaseService import DataBaseService
import datetime
import time

DateTimeNow = datetime.datetime.now().strftime("%Y-%m-%d")
TimeStart = datetime.datetime.now()
PageNumber = 1
SteamRank = 1
TotalAppQuantity = 0
InsertDataList = []
DBService = DataBaseService().GetDataBase()
DBCursor = DBService.cursor()

SelectSQL = "SELECT COUNT(*) FROM Application WHERE UpdateDateTime = '%s'"
DBCursor.execute(SelectSQL % DateTimeNow)
Result = DBCursor.fetchone()
DBCursor.close()
DBService.close()

if(Result[0] == 0):
    print("開始執行排程")

    while(True):
        StrPageNumber = str(PageNumber)
        RankPageUrl = "https://store.steampowered.com/search/?ignore_preferences=1&filter=topsellers&os=win&cc=TW&page=" + StrPageNumber
        RankPage = SteamRankPageParseService(RankPageUrl)

        print("開始解析第" + StrPageNumber + "頁")
        print("解析中...")

        if(RankPage.IsAllDataSetReady() == True):            
            for AppCount in range(RankPage.AppQuantity):
                print("正在解析排行榜第" + StrPageNumber + "頁中第" + str(AppCount + 1) + "個App")

                AppUrl = RankPage.AppUrlList[AppCount]
                SmallUrl = RankPage.SmallPictureList[AppCount]
                ApplicationPage = SteamApplicationPageParseService(AppUrl)

                InsertDataList.append(
                    (
                        DateTimeNow, "TopSeller", RankPage.AppIDList[AppCount], 
                        RankPage.AppNameList[AppCount], RankPage.AppIDList[AppCount], RankPage.EvaluationList[AppCount], 
                        RankPage.OriginalPriceList[AppCount], RankPage.DiscountPriceList[AppCount], RankPage.DiscountList[AppCount],
                        RankPage.AppUrlList[AppCount], SmallUrl, ApplicationPage.GetHeaderPicture(SmallUrl),
                        PageNumber, SteamRank, ApplicationPage.GetScreenshot(), "", ""
                    )
                )

                AppCount = AppCount + 1
                SteamRank = AppCount

            TotalAppQuantity = TotalAppQuantity + RankPage.AppQuantity
        else:
            break

        print("第" + str(PageNumber) + "頁解析花費時間 :" + str(datetime.datetime.now() - TimeStart))

        if(RankPage.IsLastPage()):
            break

        PageNumber = PageNumber + 1
        print(len(InsertDataList))

    print("共" + str(TotalAppQuantity) + "個App解析完成")
    print("解析共花費時間 :" + str(datetime.datetime.now() - TimeStart))
    print("開始新增資料進Table")

    InsertManySQL = """INSERT INTO Application(UpdateDateTime, RankType, ApplicationID, ApplicationName, ApplicationType, Evaluation, 
    OriginalPrice, DiscountPrice, Discount, SteamLink, SmallPicture, HeaderPicture, SteamPageNumber, SteamRank, Screenshot, 
    BestComment, WorstComment) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    TempInsertDataList = []
    ListLength = len(InsertDataList)
    N = 0

    for InsertData in InsertDataList:
        TempInsertDataList.append(InsertData)
        N = N + 1
        if(N == ListLength or N == 300):
            DBCursor.executemany(InsertManySQL, TempInsertDataList)
            TempInsertDataList = []
            N = 0
            DBCursor.close()
            DBService.commit()
            DBService.close()

    print("共插入完成" + str(TotalAppQuantity) + "個Apps")
    print("總共花費時間 :" + str(datetime.datetime.now() - TimeStart))
    
else:
    print("已經有" + DateTimeNow + "的資料，共" + str(Result[0]) + "筆")