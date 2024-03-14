from io import BytesIO
import os
from google.cloud import vision
from textblob import TextBlob
from PIL import Image

# Instanciar un cliente
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your_google_api_credentials.json'
client = vision.ImageAnnotatorClient()

def getLabels(image):
  # Procesamos la imagen
  image_pil = Image.open(image)
  with BytesIO() as output:
    image_pil.save(output, format='JPEG')
    bytes_content = output.getvalue()

  # Generar el objeto Image a analizar
  image = vision.Image(content=bytes_content)
  
  # Llamada al cliente de google vision
  response = client.label_detection(image=image)
  labels = []
  for label in response.label_annotations:
    labels.append(label.description)
  
  return labels

def translateList(list):
  delete_words = ['Edificio', 'Propiedad', 'Baño', 'Cocina', 'Sala de estar',
                  'Diseño de interiores', 'Marco', 'Sombra', 'Piso', 'Comodidad',
                  'Arquitectura', 'Púrpura', 'Arreglo de tubería', 'Marrón']
  change_words = {
    "Hundir": "Pila",
    "Gabinetes": "Armarios bajos",
    "Marco de la cama": "Cabecero",
    "Madera": "Suelos de madera",
    "Asiento del baño": "WC"
  }
  translated = []
  # Traduccion de las características
  for word in list:
    blob = TextBlob(word)
    translated.append(str(blob.translate(from_lang='en', to='es')))

  new_translated = [word for word in translated if word not in delete_words]
  # Cambio las palabras mal traducidas
  for i in range(len(new_translated)):
    if new_translated[i] in change_words:
      new_translated[i] = change_words[new_translated[i]]
  
  new_translated = [word.lower() for word in new_translated]

  return new_translated

# image_path = './images/salon.jpg'

# labels = getLabels(image_path)
# print("ETIQUETAS:")
# labels_esp, pos = translateList(labels)
# for label in labels_esp:
#   print(label)