import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def abrir_archivo():
    with open('Vuelos ordenados por fecha.txt', 'r') as archivo:
        return archivo.readlines()


def crear_lista_fechas_precios():

    archivo = abrir_archivo()    
    archivo.remove('\n')

    lista_fechas_precios = []
    lista_fechas = []
    lista_precios = []

    for vuelo in archivo:
        
        vuelo = vuelo.split('.')
        del vuelo[-1]
        del vuelo[-1]
        del vuelo[-1]
        vuelo[0] = vuelo[0].split(' ')[0].replace('(', '')
        vuelo[1] = vuelo[1].replace(' Precio: ', '').replace(' ARS', '').replace(' ', '')

        lista_fechas_precios.append(vuelo)
        #lista_fechas.append(vuelo[0])
        #lista_precios.append(vuelo[1])
    
    for vuelo in lista_fechas_precios:
        vuelo[0] = pd.to_datetime(vuelo[0], format="%d/%m/%y")

    lista_fechas_precios.sort(key=lambda x: x[1])
    
    for vuelo in lista_fechas_precios:
        lista_fechas.append(vuelo[0])
        lista_precios.append(vuelo[1])

    return [lista_fechas, lista_precios]


def armar_grafico():

    lista = crear_lista_fechas_precios()

    x = lista[0]
    y = lista[1]
    plt.yticks([int(lista[1][0]), int(lista[1][int(len(lista[1])/2)]), int(lista[1][len(lista[1])-1])])

    plt.bar(x, y)

    #plt.grid()
    #plt.bar(xpoints, ypoints)
    #plt.tick_params(labelleft=False, left=False)
    plt.show()


armar_grafico()