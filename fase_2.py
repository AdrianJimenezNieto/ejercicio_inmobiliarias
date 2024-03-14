import googlemaps

# Definir mi API key
API_KEY = "yourapikey"

# Definir mi cliente
gmaps = googlemaps.Client(key = API_KEY)

# Definir las coordenadas de la búsqueda
# coordinates = {
#   "latitud": 41.63294274993376,
#   "longitud": -0.8797277
# }

# Definimos los lugares de interés
interest_types = ["school", "transit_station", "store", 
                  "gym", "pharmacy", "park", "electric_vehicle_charging_station",
                  "hospital"]

interest_trans = ["Escuelas", "Transporte público", "Tiendas",
                  "Gimnasios", "Farmacias", "Parques", "Cargadores de coche",
                  "Hospitales y clínicas"]

def getPlaces(address, radius):
  geocode_result = gmaps.geocode(address)

  location = (geocode_result[0]['geometry']['location']['lat'],
              geocode_result[0]['geometry']['location']['lng'])
  
  # Búsqueda de los tipos de interes cercanos
  places = {}
  for i in range(len(interest_types)):
    type = interest_trans[i]
    place = gmaps.places_nearby(location=location, radius=radius, type=interest_types[i])
    aux = place.get('results', [])

    places[type] = {}
    places[type]['places'] = []
    places[type]['count'] = len(aux)
    for place in aux[:3]:
      places[type]['places'].append(f"{place['name']}({place['vicinity']})")

  return places

# places = getPlaces(coordinates, 1000)

# print(places)
# # Mostrar información de los lugares encontrados
# # for place in places:
# #   print(f"Nombre: {place['name']}")
# #   print(f"Tipo: {place['types']}")
# #   print(f"Direccion: {place['vicinity']}")
# #   print("-----------------------------------------------------")


