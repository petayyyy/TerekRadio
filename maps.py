from functools import partial
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="testGet")
geocode = partial(geolocator.geocode, language="ru")

# return lat, lon
def CreateMapP(city: str, address: str):
    # location = geocode("Москва Нарвская 2")
    addressN = " ".join(address.split(",")[:2])
    #print(address, addressN, end=" :: ")
    addrStr = city + " " + addressN
    return GetMapP(addrStr)

def GetMapP(addrStr: str):
    addrStr = addrStr.replace("г.", "")
    addrStr = addrStr.replace(",", "")
    addrStr = addrStr.replace(".", ". ")
    if (len(addrStr) > 2): 
        location = geocode(addrStr)
        if (location != None): return float(location.latitude), float(location.longitude), addrStr
        else: return 0, 0, addrStr
    else: return 0, 0, ""
def DistaceBetwPoint(lat1: float, lon1: float, lat2: float, lon2: float):
    return ((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5
