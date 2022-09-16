import requests
import unidecode
import re


archivo = requests.get('https://countriesnow.space/api/v0.1/countries/population/cities')
archivo = archivo.json()


with open('ciudades.txt', 'w', encoding='utf8') as archivo_txt:
    for i in archivo['data']:
        ciudad = i['city'].lower()
        ciudad = ciudad.replace('-', ',')
        ciudad = ciudad.replace('/', ',')
        ciudad = unidecode.unidecode(ciudad)
        ciudad = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", ciudad)
        ciudad = ciudad.replace('()', '')
        ciudad = ciudad.strip()
        ciudad_separada = ciudad
        ciudad = ciudad.replace(' ', '')

        archivo_txt.write(ciudad + '-' + ciudad_separada + ',')