import json, requests
from time import strptime
from datetime import date
import pandas as pd


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

def obtener_lista_precios():
    return lista_procesado_precios
    
def obtener_mensaje():
    return escribir_mensaje(lista_procesado)

def obtener_mensaje_precios():
    return escribir_mensaje(lista_procesado_precios)

def obtener_lista_ciudades():
    with open('ciudades.txt', 'r') as ciudades:
        ciudades = ciudades.read().split(',')
        return ciudades

#Crea una lista de listas con los meses y sus precios promedio
def obtener_lista_meses_mas_baratos():

    lista_meses_precios = []
    meses = []

    for mes, precio in zip(data.keys(), data.values()):
        if len(mes.split(' ')) == 7:
            mes = mes.split(' ')[1]
            precio = float(precio.split(' ')[1].replace(',', ''))

            lista_meses_precios.append({mes : precio})

            if [mes] not in meses:
                meses.append([mes])

    lista = []
    for i in meses:
        lista = []
        lista = list(d.get(i[0], 0) for d in lista_meses_precios)

        while 0 in lista:
            lista.remove(0)
                
        promedio = int(sum(lista)/len(lista))
        i[0] = mes_corto_a_largo(i[0])
        i.append(promedio)
    
    meses.sort(key=lambda meses: meses[1])

    while len(meses) < 11:
        meses.append(['', ''])
    
    return meses


def obtener_fecha_mas_barata_por_mes():
    precio_mas_barato_mes = []
    mes_actual = ''
    data.popitem()

    for i,j in zip(data.keys(), data.values()):
        i = i.split(' ')[1] + ' ' + i.split(' ')[2]

        mes_actual = i.split(' ')[0]

        j = int(j.split(' ')[1].replace(',', ''))
        if len(precio_mas_barato_mes) == 0:
            precio_mas_barato_mes.append([i,j])
        else:
            size = len(precio_mas_barato_mes)-1
            if j < precio_mas_barato_mes[size][1] and precio_mas_barato_mes[size][0].split(' ')[0] == mes_actual:
                precio_mas_barato_mes.pop()
                precio_mas_barato_mes.append([i,j])
            elif j < precio_mas_barato_mes[size][1] or precio_mas_barato_mes[size][0].split(' ')[0] != mes_actual:
                precio_mas_barato_mes.append([i,j])
    
    return precio_mas_barato_mes


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


def crear_excel_por_precio():

    lista_fechas_ida = []
    lista_fechas_vuelta = []
    lista_precios = []
    lista_urls = []
    for i in lista_procesado_precios:
        fecha_ida = '('+i[0]+'/'+i[1]+'/'+i[2]+')'
        fecha_vuelta = '('+i[3]+'/'+i[4]+'/'+i[5]+')'
        precio = str(i[6]) + ' ' + i[8]
        url = i[7]

        lista_fechas_ida.append(fecha_ida)
        lista_fechas_vuelta.append(fecha_vuelta)
        lista_precios.append(precio)
        lista_urls.append(url)

    # dataframe Name and Age columns
    df = pd.DataFrame({'Fecha ida': lista_fechas_ida,
                    'Fecha vuelta': lista_fechas_vuelta,
                    'Precio': lista_precios,
                    'URL': lista_urls
                    })

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('Vuelos ordenados por precio.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add some cell formats.
    format1 = workbook.add_format({'num_format': '#,##0.00'})

    # Set the column width and format.
    worksheet.set_column(0, 2, 15, format1)
    worksheet.set_column(3, 3, 120, format1)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()



def crear_excel_por_fecha():

    lista_fechas_ida = []
    lista_fechas_vuelta = []
    lista_precios = []
    lista_urls = []
    for i in lista_procesado:
        fecha_ida = '('+i[0]+'/'+i[1]+'/'+i[2]+')'
        fecha_vuelta = '('+i[3]+'/'+i[4]+'/'+i[5]+')'
        precio = str(i[6]) + ' ' + i[8]
        url = i[7]

        lista_fechas_ida.append(fecha_ida)
        lista_fechas_vuelta.append(fecha_vuelta)
        lista_precios.append(precio)
        lista_urls.append(url)

    # dataframe Name and Age columns
    df = pd.DataFrame({'Fecha ida': lista_fechas_ida,
                    'Fecha vuelta': lista_fechas_vuelta,
                    'Precio': lista_precios,
                    'URL': lista_urls
                    })

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('Vuelos ordenados por fecha.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add some cell formats.
    format1 = workbook.add_format({'num_format': '#,##0.00'})

    # Set the column width and format.
    worksheet.set_column(0, 2, 15, format1)
    worksheet.set_column(3, 3, 120, format1)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

#Pasa mes abreviado a mes entero
def mes_corto_a_largo(mes_corto):
    return {
            'Jan': 'Enero',
            'Feb': 'Febrero',
            'Mar': 'Marzo',
            'Apr': 'Abril',
            'May': 'Mayo',
            'Jun': 'Junio',
            'Jul': 'Julio',
            'Aug': 'Agosto',
            'Sep': 'Septiembre', 
            'Oct': 'Octubre',
            'Nov': 'November',
            'Dec': 'Diciembre'
    }[mes_corto]