"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
assert cf
from DISClib.ADT import map as mp

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Iniciar catálogo")
    print("2- Cargar información de las rutas aéreas.")
    print("3- Requerimiento 1 (Grupal): Encontrar puntos de interconexión aérea")
    print("4- Requerimiento 2 (Grupal): Encontrar clústeres de tráfico aéreo")
    print("5- Requerimiento 3 (Grupal): Encontrar la ruta más corta entre ciudades")
    print("6- Requerimiento 4 (Grupal): Utilizar las millas de viajero")
    print("7- Requerimiento 5 (Grupal): Cuantificar el efecto de un aeropuerto cerrado")
    print("8- Requerimiento 6 (BONO Grupal): Comparar con servicio WEB externo")


catalog = None
routes = 'routes_full.csv'
airports = 'airports_full.csv'
cities = 'worldcities.csv'

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = controller.init()
        
        print("Cargando información de los archivos ....")

    elif int(inputs[0]) == 2:
        dirigido = controller.loadDataAir(catalog,airports)
        controller.loadDataRoute(catalog,routes)
        controller.loadDataCities(catalog,cities)

        print("--GRAFO DIRIGIDO--")
        print("El total de aeropuertos es de: "+str(gr.numVertices(catalog["routes"])))
        print("El total de rutas aéreas es de: "+str(gr.numEdges(catalog["routes"])))
        print("El primer aeropuerto cargado fue: " + dirigido["Name"])
        print("Su ciudad es: " + dirigido["City"])
        print("Su país es: " + dirigido["Country"])
        print("Latitud: " + dirigido["Latitude"] + ", Longitud: " + dirigido["Longitude"])
        print(" ")

        print("--GRAFO NO DIRIGIDO--")
        print("El total de aeropuertos es de: "+str(gr.numVertices(catalog["connected"])))
        print("El total de rutas aéreas que tienen ida y vuelta es de:" + str(gr.numEdges(catalog["connected"])))
        llave = lt.firstElement(catalog["salida"])
        datos = mp.get(catalog["IATAS"], llave)["value"]
        print("El primer aeropuerto cargado fue: " + datos["Name"])
        print("Su ciudad es: " + datos["City"])
        print("Su país es: " + datos["Country"])
        print("Latitud: " + datos["Latitude"] + ", Longitud: " + datos["Longitude"])
        print(" ")        

        print("El total de ciudades es de: "+ str(lt.size(catalog["cities"])))
        ciudadprimero = lt.firstElement(catalog["cities"])
        print("La primera ciudad cargada fue " + ciudadprimero["city_ascii"])
        print("Latitud " + str(ciudadprimero["lat"]) + ", Longitud " + str(ciudadprimero["lng"]))
        print("Población: " + ciudadprimero["population"])
        
        

    else:
        sys.exit(0)
sys.exit(0)
