# Подключаем библиотеки
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
from datetime import datetime
from configs import *

class SheetEditor():
    def _init_(self):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http()) # Авторизуемся в системе
        self.service = apiclient.discovery.build('sheets', 'v4', http = self.httpAuth) # Выбираем работу с таблицами и 4 версию API 
        self.sheetService = self.service.spreadsheets()
    def SendReviews(self, idUser, nameUser, rev):
        return self.SendDataOther(idSheet=idReviews, idUser=idUser, nameUser=nameUser, textData=rev)
    def SendOffer(self, idUser, nameUser, offer):
        return self.SendDataOther(idSheet=idOffer, idUser=idUser, nameUser=nameUser, textData=offer)
    def SendQuestion(self, idUser, nameUser, quest):
        return self.SendDataOther(idSheet=idQuestion, idUser=idUser, nameUser=nameUser, textData=quest)
    def SendDataOther(self, idSheet, idUser, nameUser, textData):
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