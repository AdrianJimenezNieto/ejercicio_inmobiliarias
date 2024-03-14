import pandas as pd

# Cargamos dataset
# dataset obtenido de kaggle: https://www.kaggle.com/datasets/datamarket/inmuebles-en-alquiler
data = pd.read_csv('./datasets/inmuebles-en-alquiler-sample.csv')

# Limpiamos los datos
data.drop(['website', 'province', 'town', 'location', 'name',
          'is_outer', 'description', 'publication','dealer', 'is_professional',
          'insert_date', 'floor', 'elevator'], axis = 'columns', inplace=True)

# Calculamos parametros de interes
area_q30 = data['area'].quantile(0.30)
area_q80 = data['area'].quantile(0.80)
nRooms_q30 = data['rooms'].quantile(0.30)
nRooms_q80 = data['rooms'].quantile(0.80)
price_q30 = data['price'].quantile(0.30)
price_q80 = data['price'].quantile(0.80)

# Clasificamos el piso según los parámetros obtenidos
def getTypeOfText(home):
  threshold = []

  if home['price'] >= price_q80:
    threshold.append(3)
  elif home['price'] >= price_q30:
    threshold.append(1)
  else:
    threshold.append(2)

  if home['nRooms'] >= nRooms_q80:
    threshold.append(3)
  elif home['nRooms'] >= nRooms_q30:
    threshold.append(1)
  else:
    threshold.append(2)

  if home['area'] >= area_q80:
    threshold.append(3)
  elif home['area'] >= area_q30:
    threshold.append(1)
  else:
    threshold.append(2)

  # Clasificamos el inmueble según los resultados
  if sum(threshold) > 7:
    return 'formal'
  elif sum(threshold) < 4:
    return 'jerga'
  else:
    return 'informal'