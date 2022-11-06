import requests, json, os

#Se obtiene el json con los datos de las personas
response = requests.get('http://127.0.0.1:8000/personas/').json()

#Se crea un archivo con esos datos
with open('personas.json', 'w') as archivo:
    json.dump(response, archivo)

archivo_personas = response

longitud = len(archivo_personas)

#Se ejecuta el proceso de
#Automatizacion, procesamiento de datos y envio de mail
#Una vez por persona
for i in range(longitud):

    with open('personas.json', 'w') as archivo:
        json.dump(archivo_personas, archivo)

    os.system('npx playwright test --debug')

    

    archivo_personas.pop(0)

print(archivo_personas)