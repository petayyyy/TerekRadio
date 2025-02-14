# Подключаем библиотеки
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
from datetime import datetime
from configs import *
import time
from maps import CreateMapP, DistaceBetwPoint

class SheetEditor():
    def __init__(self):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http()) # Авторизуемся в системе
        self.service = apiclient.discovery.build('sheets', 'v4', http = self.httpAuth) # Выбираем работу с таблицами и 4 версию API 
        self.sheetService = self.service.spreadsheets()
        self.listDiller = []
    def SendReviews(self, idUser, nameUser, rev):
        return self.SendDataOther(idSheet=idReviews, idUser=idUser, nameUser=nameUser, textData=rev)
    def SendOffer(self, idUser, nameUser, offer):
        return self.SendDataOther(idSheet=idOffer, idUser=idUser, nameUser=nameUser, textData=offer)
    def SendQuestion(self, idUser, nameUser, quest):
        return self.SendDataOther(idSheet=idQuestion, idUser=idUser, nameUser=nameUser, textData=quest)
    def SendDataOther(self, idSheet, idUser, nameUser, textData):
        # print(idSheet, idUser, nameUser, textData)
        result = (
            self.sheetService.values()
            .get(spreadsheetId=idSheet, range=SAMPLE_RANGE_Other)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            return False
        else:
            # Getting the current date and time
            dt = datetime.now()
            self.sheetService.values().update(spreadsheetId=idSheet, range=f"List1!A{len(values) + 1}", valueInputOption="USER_ENTERED", body={"values": [[str(dt)]]}).execute()
            self.sheetService.values().update(spreadsheetId=idSheet, range=f"List1!B{len(values) + 1}", valueInputOption="USER_ENTERED", body={"values": [[str(nameUser)]]}).execute()
            self.sheetService.values().update(spreadsheetId=idSheet, range=f"List1!C{len(values) + 1}", valueInputOption="USER_ENTERED", body={"values": [[str(idUser)]]}).execute()
            self.sheetService.values().update(spreadsheetId=idSheet, range=f"List1!D{len(values) + 1}", valueInputOption="USER_ENTERED", body={"values": [[str(textData)]]}).execute()
            return True
    def ReadDataDillers(self):
        result = (
            self.sheetService.values()
            .get(spreadsheetId=idDillers, range=SAMPLE_RANGE_Dillers)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            return False
        else:
            self.listDiller = values
            count = 0
            # print(self.listDiller)
            for dil in self.listDiller:
                if (len(dil) == 8):
                    lat, lon, addr = CreateMapP(dil[6], dil[7])    
                    if (lat == 0 or lon == 0): 
                        lat, lon, addr = CreateMapP(dil[6], "")
                        if (lat == 0 or lon == 0):     
                            self.SendMapC(-1, -1, countStr=count)    
                            lat, lon = -1, -1  
                        else:
                            self.SendMapC(lat, lon, countStr=count)                              
                    else:
                        self.SendMapC(lat, lon, countStr=count)  
                    self.listDiller[count].append(lat)   
                    self.listDiller[count].append(lon) 
                elif (len(dil) == 10 and (dil[8] == 0 or dil[9] == 0 or dil[8] == "0" or dil[9] == "0" or dil[8] == -1 or dil[9] == -1 or dil[8] == "-1" or dil[9] == "-1")):
                    lat, lon, addr = CreateMapP(dil[6], dil[7])    
                    if (lat == 0 or lon == 0): 
                        lat, lon, addr = CreateMapP(dil[6], "")
                        if (lat == 0 or lon == 0):     
                            self.SendMapC(-1, -1, countStr=count) 
                            lat, lon = -1, -1     
                        else:
                            self.SendMapC(lat, lon, countStr=count)                              
                    else:
                        self.SendMapC(lat, lon, countStr=count)  
                    self.listDiller[count][8] = lat   
                    self.listDiller[count][9] = lon   
                # else:
                #     # print(dil,  self.listDiller[count])
                #     if (len(dil) == 10):
                #         self.listDiller[count][8] = -1   
                #         self.listDiller[count][9] = -1
                #     else:
                #         self.listDiller[count].append(-1)   
                #         self.listDiller[count].append(-1)     
                count+=1
            for i in range(len(self.listDiller)):
                if (len(self.listDiller[i]) == 10 and type(self.listDiller[i][8]) == str): 
                    self.listDiller[i][8] = float(self.listDiller[i][8].replace(",", "."))
                if (len(self.listDiller[i]) == 10 and type(self.listDiller[i][9]) == str): 
                    self.listDiller[i][9] = float(self.listDiller[i][9].replace(",", "."))
            return values
    def CheckDillers(self, lat: float, lon: float):
        arrayDist = []
        for i in range(len(self.listDiller)):
            # print(lat, lon, self.listDiller[i][8], self.listDiller[i][9])
            distC = DistaceBetwPoint(lat1=float(lat), lon1=float(lon), lat2=self.listDiller[i][8], lon2=self.listDiller[i][9])
            arrayDist.append([i, distC])
        arrayDist.sort(key=lambda index : index[1])
        return self.listDiller[arrayDist[0][0]], self.listDiller[arrayDist[1][0]], self.listDiller[arrayDist[2][0]]
        
    def SendMapC(self, lat, lon, countStr, isSleep: bool = True):
        countStr += 2
        self.sheetService.values().update(spreadsheetId=idDillers, range=f"List1!I{countStr}", valueInputOption="USER_ENTERED", body={"values": [[lat]]}).execute()
        self.sheetService.values().update(spreadsheetId=idDillers, range=f"List1!J{countStr}", valueInputOption="USER_ENTERED", body={"values": [[lon]]}).execute()
        if (isSleep): time.sleep(1)