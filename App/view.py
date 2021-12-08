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
import queryAPI
import getAccessToken
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
assert cf
from DISClib.ADT import map as mp
import threading
from DISClib.ADT import stack

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
routes = 'routes-utf8-small.csv'
airports = 'airports-utf8-small.csv'
cities = 'worldcities-utf8.csv'

"""
Menu principal
"""
def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            catalog = controller.init()       
            print("Cargando información de los archivos ....")

        elif int(inputs[0]) == 2:
            controller.loadDataAir(catalog,airports)
            controller.loadDataRoute(catalog,routes)
            controller.loadDataCities(catalog,cities)

            print("---GRAFO DIRIGIDO---")
            print("Nodes: El total de aeropuertos cargados es de: "+str(gr.numVertices(catalog["routes"])))
            print("Edges: El total de rutas aéreas es de: "+str(gr.numEdges(catalog["routes"])))
            llave = lt.firstElement(catalog["salida"])
            datos = mp.get(catalog["IATAS"], llave)["value"]
            print("El primer aeropuerto cargado fue: " + datos["Name"])
            print("Su ciudad es: " + datos["City"])
            print("Su país es: " + datos["Country"])
            print("Latitud: " + datos["Latitude"] + ", Longitud: " + datos["Longitude"])
            llave = lt.lastElement(catalog["salida"])
            datos = mp.get(catalog["IATAS"], llave)["value"]
            print("El último aeropuerto cargado fue: " + datos["Name"])
            print("Su ciudad es: " + datos["City"])
            print("Su país es: " + datos["Country"])
            print("Latitud: " + datos["Latitude"] + ", Longitud: " + datos["Longitude"])
            print(" ")      

            print("---GRAFO NO DIRIGIDO---")
            print("Nodes: El total de aeropuertos cargados es de: "+str(gr.numVertices(catalog["connected"])))
            print("Edges: El total de rutas aéreas que tienen ida y vuelta es de: " + str(gr.numEdges(catalog["connected"])))
            llave = lt.firstElement(catalog["salida"])
            datos = mp.get(catalog["IATAS"], llave)["value"]
            print("El primer aeropuerto cargado fue: " + datos["Name"])
            print("Su ciudad es: " + datos["City"])
            print("Su país es: " + datos["Country"])
            print("Latitud: " + datos["Latitude"] + ", Longitud: " + datos["Longitude"])
            llave = lt.lastElement(catalog["salida"])
            datos = mp.get(catalog["IATAS"], llave)["value"]
            print("El último aeropuerto cargado fue: " + datos["Name"])
            print("Su ciudad es: " + datos["City"])
            print("Su país es: " + datos["Country"])
            print("Latitud: " + datos["Latitude"] + ", Longitud: " + datos["Longitude"])
            print(" ")        

            print('--- Ciudades ---')
            print("El total de ciudades es de: "+ str(lt.size(catalog["cities"])))
            ciudadprimero = lt.firstElement(catalog["cities"])
            print("La primera ciudad cargada fue " + ciudadprimero["city_ascii"])
            print("Latitud " + str(ciudadprimero["lat"]) + ", Longitud " + str(ciudadprimero["lng"]))
            print("Población: " + ciudadprimero["population"])
            ciudadprimero = lt.lastElement(catalog["cities"])
            print("La ultima ciudad cargada fue " + ciudadprimero["city_ascii"])
            print("Latitud " + str(ciudadprimero["lat"]) + ", Longitud " + str(ciudadprimero["lng"]))
            print("Población: " + ciudadprimero["population"])
            
        elif int(inputs[0]) == 4:  
            air1 = input("Ingrese el IATA del primer aeropuerto: ")
            air2 = input("Ingrese el IATA del segundo aeropuerto: ")
            mismo = controller.req2(catalog, air1, air2)

            print(" ")
            print("El total de clústeres en la red de transporte aéreo es de:  "+ str(mismo[1]))
            if mismo[0]:
                print("Los aeropuertos ingresados -SI- corresponden al mismo clúster aéreo")
            else:
                print("Los aeropuertos ingresados -NO- corresponden al mismo clúster aéreo")
            print(" ")

            MAPA = controller.v_req2(catalog, mismo, air1, air2)
            

        elif int(inputs[0]) == 3:
            print('=============== Req. 1 Inputs ===============')
            print('most connected airports in network (TOP 5)')
            print("Numbers of airports in network: " + str(mp.size(catalog['IATAS'])))
            info = controller.req1(catalog)
            print('=============== Req. 1 Outputs ===============')
            print('Connected airports inside network: ' + str(info[0]))
            print("Top 5 most connected airports..")
            for x in lt.iterator(info[1]):
                print(x["Name"])
                print(x["degree"])
                print(x["indegree"])
                print(x["outdegree"])
            
            MAPA = controller.v_req1(catalog,info[1])

        elif int(inputs[0]) == 5:

            origin = "Saint Petersburg" #input("Por favor digite la ciudad de origen: ")
            if lt.isPresent(catalog['repeat'],origin):
                print("La ciudad que usted busca tiene mas de un posible resultado.")
                ciudades = mp.get(catalog['cities2'], origin)['value']
                print("Estos son los posibles países que usted puede estar buscando")
                contador = 1
                for x in lt.iterator(ciudades):
                    print('=== Posición ' + str(contador) + ' ===')
                    contador += 1
                    print(x['city_ascii'])
                    print(x["country"])
                    print(x['admin_name'])
                choice = int(input('Digite la opción deseada: '))
                ciudadorigen = lt.getElement(ciudades,choice)
            else:
                ciudad = mp.get(catalog['cities2'],origin)["value"]
                ciudadorigen = lt.getElement(ciudad,1)
            
            destiny ="Lisbon" #input("Por favor digite la ciudad de destino: ")
            if lt.isPresent(catalog['repeat'],destiny):
                print("La ciudad que usted busca tiene mas de un posible resultado.")
                ciudades = mp.get(catalog['cities2'], destiny)['value']
                print("Estos son los posibles países que usted puede estar buscando")
                contador2=1
                for x in lt.iterator(ciudades):
                    print('=== Posición ' + str(contador2) + ' ===')
                    contador2 += 1
                    print(x['city_ascii'])
                    print(x["country"])
                    print(x['admin_name'])
                choice = int(input('Digite la opción deseada: '))
                ciudaddestino = lt.getElement(ciudades,choice)
            else:
                ciudad = mp.get(catalog['cities2'],destiny)["value"]
                ciudaddestino = lt.getElement(ciudad,1)
            info = controller.req3(catalog,ciudadorigen,ciudaddestino)
            if info != None:
                print('=' * 15 + " Req No. 3 Inputs " + '=' * 15)
                print("Departure city: " + origin)
                print("Arrival city: " + destiny)
                print('=' * 15 + " Req No. 3 Answer " + '=' *15)
                print(" +++ The departure airport in " + origin + " is +++")
                print("IATA: " + info[0]["IATA"])
                print("Name: " + info[0]["Name"])
                print("City: " + info[0]["City"])
                print("Country: " + info[0]["Country"])
                print("The distance from the city to the airport is: " + str(info[1]) + " km")

                print(" +++ The arrival airport in " + destiny + " is +++")
                print("IATA: " + info[2]["IATA"])
                print("Name: " + info[2]["Name"])
                print("City: " + info[2]["City"])
                print("Country: " + info[2]["Country"])
                print("The distance from the airport to the city is: " + str(info[3]) + " km") 

                print (" +++ Dijkstra's trip details +++")
                print (" - Total distance: " + str(info[4]) + " (km)")     
                print (" - Trip Path: ")
                for route in lt.iterator(info[5]):
                    print("Origin : " + route["vertexA"] + " | Destiny: " + route["vertexB"] + " | Distance: "  + str(route["weight"]) + " (km)"  )
                total = info[4] + info[1] + info[3]
                print("The total distance of the trip is " + str(total) +  " (km)")


        elif int(inputs[0]) == 6:  
            city = "LIS" #input("Ingrese la ciudad de origen: ")
            millas = "1985.00" #input("Ingrese las millas de viajero disponibles: ")
            controller.req4(catalog,city,millas)

        elif int(inputs[0]) == 7:  
            iata = input("Ingrese el IATA del aeropuerto fuera de funcionamiento: ")
            tab = controller.req5(catalog,iata)
            MAP = controller.v_req5(catalog,tab,iata)
            city = catalog["IATAS"]
            print("+"+("-"*91)+"+")
            print("|"+"IATA".center(6)+"|"+"Name".center(50)+" | "+ "City".center(30)+" | ")
            print("+"+("-"*91)+"+")
            for i in lt.iterator(tab[0]):
                d = mp.get(city,i)["value"]
                print("|"+str(i).center(6)+"|"+str(d["Name"]).center(50)+" | "+ d["City"].center(30)+" | ")
                print("+"+("-"*91)+"+")

            for i in lt.iterator(tab[1]):
                d = mp.get(city,i)["value"]
                print("|"+str(i).center(6)+"|"+str(d["Name"]).center(50)+" | "+ d["City"].center(30)+" | ")
                print("+"+("-"*91)+"+")

        elif int(inputs[0]) == 8:  
            client_id = input("Ingrese su API Key: ")
            secret = input("Ingrese su API secret: ")
            getAccessToken.getToken(client_id,secret)
            token = input("Ingrese su Access Token: ")
            origen = input("Ingrese la ciudad de origen: ")
            destino = input("Ingrese la ciudad de destino: ")

            queryAPI.queryAPI(token)

            if lt.isPresent(catalog['repeat'],origen):
                print("La ciudad que usted busca tiene mas de un posible resultado.")
                ciudades = mp.get(catalog['cities2'], origin)['value']
                print("Estos son los posibles países que usted puede estar buscando")
                contador = 1
                for x in lt.iterator(ciudades):
                    print('=== Posición ' + str(contador) + ' ===')
                    contador += 1
                    print(x['city_ascii'])
                    print(x["country"])
                    print(x['admin_name'])
                choice = int(input('Digite la opción deseada: '))
                ciudadorigen = lt.getElement(ciudades,choice)
            else:
                ciudad = mp.get(catalog['cities2'],origin)["value"]
                ciudadorigen = lt.getElement(ciudad,1)

        elif int(inputs[0]) == 9:
            req = input("Ingrese el Requerimiento que desea visualizar: ")
            
            
        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()