# Подключаем библиотеки
import httplib2 
import apiclient.discovery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials	
from datetime import datetime

from functools import partial
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="TEsstt")

geocode = partial(geolocator.geocode, language="ru")
location = geocode("Москва Нарвская 2")

print(location.address)
print((location.latitude, location.longitude))

CREDENTIALS_FILE = 'terekradio-8ef8fb71a56c.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Список диллеров
idTableDillers = "1kPl4VfYkJHQRKg7CO-We8zlzTK__iwCdQEUwpTdnAGY"

SAMPLE_RANGE_NAME = "List1!A:A"
SAMPLE_RANGE_NAME_1 = "List1!A5"

# Вопросы в сервисный центр
idTableSevise = "1jL3SLdING4TOOKA4kyCk_Cnph4PjDkMuWRFTXRFfTdc"


# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе

service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

sheetService = service.spreadsheets()
result = (
    sheetService.values()
    .get(spreadsheetId=idTableSevise, range=SAMPLE_RANGE_NAME)
    .execute()
)
values = result.get("values", [])

if not values:
    print("No data found.")
else:
    # Getting the current date and time
    dt = datetime.now()

    sheetService.values().update(spreadsheetId=idTableSevise, range=f"List1!A{len(values) + 1}", valueInputOption="USER_ENTERED", body={"values": [[str(dt)]]}).execute()
    sheetService.values().update(spreadsheetId=idTableSevise, range=f"List1!B{len(values) + 1}", valueInputOption="USER_ENTERED", body={"values": [[str(414231719)]]}).execute()
    sheetService.values().update(spreadsheetId=idTableSevise, range=f"List1!C{len(values) + 1}", valueInputOption="USER_ENTERED", body={"values": [["Need help!!!"]]}).execute()



