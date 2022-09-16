import json, requests
from time import strptime
from datetime import date


#Obtengo fecha del dia para comparar meses y anios
fecha_hoy = date.today()
mes = fecha_hoy.strftime("%m")
anio_actual = fecha_hoy.strftime("%y")


def convertir_json():
    #Abro el archivo json de vuelos y convierto caracteres Non-ASCII en espacios
    f = open('Vuelos.json')
    data = json.load(f)

    data = json.dumps(data)
    data = data.replace('\\u00c2\\u00a0', ' ')
    data = json.loads(data)

    return data


def procesar_lista(lista_fechas_procesar, lista_precios_procesar, origen, destino):
#Se crea una lista de fechas y precios para facilitar creacion de urls
    lista_procesado = []

    for fecha, precio in zip(lista_fechas_procesar, lista_precios_procesar):

        moneda = precio.split(' ')[0]
        precio = precio.split(' ')[1]

        fechas = fecha.split('-')
        ida = fechas[0].split(' ')
        ida[1] = strptime(ida[1],'%b').tm_mon

        vuelta = fechas[1].split(' ')
        vuelta[2] = strptime(vuelta[2],'%b').tm_mon

        anio_ida = 1
        anio_vuelta = 1
        if int(ida[1]) < int(mes):
            anio_ida += int(anio_actual)
        else:
                anio_ida = int(anio_actual)

        if int(vuelta[2]) < int(mes):
            anio_vuelta += int(anio_actual)
        else:
            anio_vuelta = int(anio_actual)

        ida = [ida[2], str(ida[1]), str(anio_ida)]
        vuelta = [vuelta[3], str(vuelta[2]), str(anio_vuelta)]

        url = 'https://www.google.com/travel/flights?q=Flights%20to%20'+destino+'%20from%20'+origen+'%20on%2020'+ida[2]+'-'+ida[1]+'-'+ida[0]+'%20through%2020'+vuelta[2]+'-'+vuelta[1]+'-'+vuelta[0]

        #Crea la lista final para procesar los datos
        #Elemento: dia, mes, anio ida, dia, mes, anio vuelta, precio, moneda
        precio = precio.replace(',', '')
        lista_procesado.append([ida[0], ida[1], ida[2], vuelta[0], vuelta[1], vuelta[2], int(precio), url, moneda])
        
    lista_procesado_precios = lista_procesado[:]
    lista_procesado_precios.sort(key=lambda vuelo: vuelo[6])
    return [lista_procesado_precios, lista_procesado]


def escribir_mensaje(lista_procesado):
    cuerpo_mensaje = '\n'

    for vuelo in lista_procesado:
        cuerpo_mensaje += '(' + vuelo[0] + '/' + vuelo[1] + '/' + vuelo[2] + ' a ' + vuelo[3] + '/' + vuelo[4] + '/' + vuelo[5] + '). Precio: ' + str(vuelo[6]) + ' ' + ' ARS' + '. URL del vuelo: ' + vuelo[7] + ' \n'

    return cuerpo_mensaje


data = convertir_json()

#Si algun elemento queda en blanco, es borrado
data = {k: v for k, v in data.items() if v}

#request_dollar = requests.get('https://api.bluelytics.com.ar/v2/latest')

#Tomo el json y creo listas de fechas y precios, eliminando el origen y el destino del archivo
#para ser usados en variables
lista_fechas_procesar = list(data.keys()) 
lista_precios_procesar = list(data.values())
origen = lista_fechas_procesar.pop(len(lista_fechas_procesar)-1)
destino = lista_precios_procesar.pop(len(lista_precios_procesar)-1)
listas = procesar_lista(lista_fechas_procesar, lista_precios_procesar, origen, destino)
lista_procesado_precios = listas[0]
lista_procesado = listas[1]

def obtener_mensaje():
    return escribir_mensaje(lista_procesado)

def obtener_mensaje_precios():
    return escribir_mensaje(lista_procesado_precios)

def crear_txt_listas_vuelos():
    with open('Vuelos ordenados por precio.txt', 'w') as f:
        f.write(escribir_mensaje(lista_procesado_precios))
    f.close()

    with open('Vuelos ordenados por fecha.txt', 'w') as f:
        f.write(escribir_mensaje(lista_procesado))
    f.close()

def obtener_lista_ciudades():
    with open('ciudades.txt', 'r') as ciudades:
        ciudades = ciudades.read().split(',')
        return ciudades

#Los nombres del origen y destino no estan separados,
#compara los nombres con una lista de ciudades y los separa
def obtener_nombres_reales_origen_destino():
    lista_ciudades = obtener_lista_ciudades()

    origen_real = origen.lower()
    destino_real = destino.lower()

    for i in lista_ciudades:
        i = i.split('-')

        if i[0] == origen_real:
            origen_real = i[1]
        if i[0] == destino_real:
            destino_real = i[1]
    
    origen_real = origen_real.title()
    destino_real = destino_real.title()
    return [origen_real, destino_real]


crear_txt_listas_vuelos()