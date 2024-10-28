
from functools import partial
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="TEsstt")

geocode = partial(geolocator.geocode, language="ru")
location = geocode("Москва Нарвская 2")

print(location.address)
print((location.latitude, location.longitude))