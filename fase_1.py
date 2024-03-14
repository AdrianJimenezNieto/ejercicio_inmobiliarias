import random

templates = {
    'formal': {
        'intro': "Estimado cliente, esta propiedad de {area} metros cuadrados y {nRooms} habitaciones, situada en {address} está disponible por {price} euros.\n\n",
        'outro': "Para más información, no dude en contactarnos. Atentamente, la agencia inmobiliaria."
    },
    'informal': {
        'intro': "¡Hola! Este pedazo de casa que está en {address} tiene {area} metros y {nRooms} habitaciones, ¡y solo cuesta {price} euros!\n\n",
        'outro': "Si te interesa, házmelo saber. ¡Nos vemos!"
    },
    'jerga': {
        'intro': "Ey, mira este piso en {address} de {area} metros y {nRooms} habitaciones, está a la venta por {price} pavos.\n\n",
        'outro': "Si te mola, ya sabes, ¡avísanos!"
    },
    'default': {
        'intro': "Este inmueble situado en {address} de {area} metros y {nRooms} habitaciones tiene un precio de {price} euros.\n\n",
        'outro': "Si estás interesado, contáctanos para más información."
    }
}

def generate_text(features = None, type = 'default', equipment = None, places = None):
  keywords = {
    'adj': ["Fantástica", "Maravillosa", "Fenomenal"],
    'space': ["Espaciosa", "Amplia"],
    'ppl': ["familias", "parejas"]
  }

  text = templates[type]['intro'].format(**features)

  text += 'Descripción de la propiedad:\n\n'

  if features["extras"]:
    format_extras = ', '.join(features['extras'])
    text += f"{random.choice(keywords['adj'])} vivienda con lujos como {format_extras}.\n\n"

  # Descripcion segun metros cuadrados
  if features["area"] >= 80:
    text += f"{random.choice(keywords['space'])} inmueble de más de {features['area']} metros cuadrados "
  elif features["area"] >= 50 and features["area"] <= 79:
    text += f"Oportunidad de inmueble de más de {features['area']} metros cuadrados "
  else:
    text += f"Acogedor inmueble de más de {features['area']} metros cuadrados "

  text += " distribuidos en:\n\n"

  # Descripcion segun número de habitaciones
  if features["nRooms"]:
    text += f"\t- {features['nRooms']} {'habitaciones' if features['nRooms']!=1 else 'habitación'}."
    if equipment['rooms']:
      text += f"{' Equipados' if features['nRooms']!=1 else 'Equipado'} con {', '.join(equipment['rooms'][0])}."
    text += "\n\n"

  # Descripcion segun salones/comedores
  if features["nLiving"]:
    text += f"\t- {features['nLiving']} {'salones/comedores' if features['nLiving']!=1 else 'salon/comedor'}."
    if equipment['living']:
      text += f"{' Equipados' if features['nLiving']!=1 else 'Equipado'} con {', '.join(equipment['living'][0])}."
    text += "\n\n"
        
  # Descripcion segun baños
  if features["nBathrooms"]:
    text += f"\t- {features['nBathrooms']} {'baños' if features['nBathrooms']!=1 else 'baño'}."
    if equipment['bath']:
      text += f"{' Equipados' if features['nBathrooms']!=1 else 'Equipado'} con {', '.join(equipment['bath'][0])}."
    text += "\n\n"

  # Descripcion segun cocinas
  if features["nKitchens"]:
    text += f"\t- {features['nKitchens']} {'cocinas' if features['nKitchens']!=1 else 'cocina'}."
    if equipment['kitchen']:
      text += f"{' Equipados' if features['nKitchens']!=1 else 'Equipado'} con {', '.join(equipment['kitchen'][0])}."
    text += "\n\n"

  # Descripcion segun estancias exteriores
  if features["nBalconies"] and features["nTerraces"]:
    sum = features['nBalconies'] + features['nTerraces']
    text += f"  - {sum} {'estancias exteriores, que se reparten en' if sum!=1 else 'estancia exterior, que se reparte en'} {features['nBalconies']} {'balcones' if features['nBalconies']!=1 else 'balcón'} y {features['nTerraces']}{' terrazas.' if features['nTerraces']!=1 else' terraza.'}"
    if equipment['terrace']:
      text += f"{' Equipados' if features['nTerraces']!=1 else 'Equipado'} con {', '.join(equipment['terrace'][0])}."
    text += "\n\n"
  else:
    text += f"\t- {features['nBalconies']} {'balcones' if features['nBalconies']!=1 else 'balcón'}." if features["nBalconies"] != 0 else f"\t- {features['nTerraces']} {'terrazas' if features['nTerraces']!=1 else 'terraza'}."
    if equipment['terrace']:
      text += f"{' Equipados' if features['nTerraces']!=1 else 'Equipado'} con {', '.join(equipment['terrace'][0])}."
    text += "\n\n"

  # Descripcion segun condiciones climatizacion
  if features["climat"]:
    formated_climat = ", ".join(features["climat"])
    text += f"En cuanto a la climatización de la vivienda ésta está dotada de {formated_climat}.\n\n"

  # Descripcion segun altura y piso
  if features["height"] and features["floor"]:
    text += f"Apartamento ideal para {keywords['ppl'][0] if features['nRooms']>2 else keywords['ppl'][1]} situado a {features['height']} metros de altura en la {features['floor']}º planta. "
  elif features["height"] == 0 and features["floor"]:
    text+= f"Apartamento ideal para {keywords['ppl'][0] if features['nRooms']>2 else keywords['ppl'][1]} situado en la {features['floor']}º planta. "

  if features["buildingYear"]:
    text += f"Construido en el año {features['buildingYear']} {'tiene un coste de ' + str(features['taxes']) + '€ al año en cuanto a impuestos.' if features['taxes'] else '.'}\n\n"

  if features["garage"]:
    text += "Amplia plaza de garaje incluida en el precio.\n\n"

  # Imprimo informacion sobre los lugares de interes
  if places:
    text += "El inmueble tiene una localización genial, contando con estas localizaciones a menos de 500m:\n\n"
    
    for place in places.keys():
      text += f"\t-{place}, cuenta con {'+20' if places[place]['count']>=20 else places[place]['count']} cercanos, entre los que se encuentran:\n"
      for aux in places[place]['places']:
        text += f"\t\t+ {aux}\n"
      text += "\n"

  text += "\n"
  text += templates[type]['outro'].format(**features)

  return text
