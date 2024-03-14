from flask import Flask, render_template, request
import json
from fase_3_4 import getLabels, translateList
from fase_1 import generate_text
from fase_5 import getTypeOfText
from fase_2 import getPlaces

# Instanciamos la clase Flask
app = Flask(__name__)

# Función para procesar las imagenes del HTML
def processImage(file):
  labels = []
  for img in file:
    if img and img.filename != '':
      labels.append(translateList(getLabels(img)))
  return labels

# Página principal
@app.get('/')
def index():
  return render_template('form.html')

@app.post('/resultado')
def resultado():
    features = {}  # Diccionario para almacenar los datos

    # Recoger los datos del formulario y almacenarlos en el diccionario
    features['address'] = request.form.get('direccion')
    features['price'] = float(request.form.get('price'))
    features['area'] = int(request.form.get('area'))
    features['nRooms'] = int(request.form.get('nRooms'))
    features['nLiving'] = int(request.form.get('nLiving'))
    features['nKitchens'] = int(request.form.get('nKitchens'))
    features['nBathrooms'] = int(request.form.get('nBathrooms'))
    features['nBalconies'] = int(request.form.get('nBalconies'))
    features['nTerraces'] = int(request.form.get('nTerraces'))
    features['nElevators'] = int(request.form.get('nElevators'))
    features['climat'] = request.form.get('climat').split(',')
    features['height'] = float(request.form.get('height'))
    features['floor'] = int(request.form.get('floor'))
    features['buildingYear'] = int(request.form.get('buildingYear'))
    features['taxes'] = float(request.form.get('taxes'))
    features['state'] = request.form.get('state')
    features['extras'] = request.form.get('extras').split(',')
    features['garage'] = bool(request.form.get('garage'))

    # Recoger las imágenes subidas por estancia
    img_kitchen = request.files.getlist('img_kitchen[]')
    img_rooms = request.files.getlist('img_rooms[]')
    img_living = request.files.getlist('img_living[]')
    img_bath = request.files.getlist('img_bath[]')
    img_terrace = request.files.getlist('img_terrace[]')

    # Procesamos las imagenes
    kitchen_labels = processImage(img_kitchen)
    rooms_labels = processImage(img_rooms)
    living_labels = processImage(img_living)
    bath_labels = processImage(img_bath)
    terrace_labels = processImage(img_terrace)

    pictures_info = {
      'kitchen': kitchen_labels,
      'rooms': rooms_labels,
      'living': living_labels,
      'bath': bath_labels,
      'terrace': terrace_labels
    }

    radious = 500
    places_info = getPlaces(features['address'], radious)

    type_of_text = getTypeOfText(features)
    
    text = generate_text(features,
                        equipment=pictures_info,
                        places=places_info,
                        type=type_of_text)

    return render_template(
      'response.html',
      data=[text,
            json.dumps(pictures_info, indent=4, sort_keys=True),
            json.dumps(places_info, indent=4, sort_keys=True),
            type_of_text]
    )

if __name__ == '__main__':
  app.run(debug=True)