import requests

# https://developers.amadeus.com/self-service/category/air/api-doc/airport-nearest-relevant/api-reference

def queryAPI(token, city ,lat, lon):
  access_token = token #TODO
  headers = {"Authorization": "Bearer " + access_token}
  params = {
    "latitude": lat,
    "longitude": lon,
    "radius": 500
  }

  r = requests.get('https://test.api.amadeus.com/v1/reference-data/locations/airports', headers=headers, params=params)
  data = r.json()
  #print(r.text)     #Solo para imprimir

  if data["meta"]["count"]== 0:
    print("No se encontró ningun aeropuerto cercano")
  else:
    cercano = data["data"][0]
    print("El aeropuerto más cercano a "+city+" es el "+ cercano["name"] + " - " +  cercano["iataCode"])
  
  return cercano["iataCode"]
