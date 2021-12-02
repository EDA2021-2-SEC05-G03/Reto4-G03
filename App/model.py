"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc 
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog = {
                'IATAS': None,
                'routes': None,
                'city': None,
                'connected': None,  
                'path': None,
                'salida' : None,
                'scc': None,
                'repeat': None,
                'cities2':None

                }

    catalog['IATAS'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIATA)

    catalog['routes'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareIATA)

    catalog["cities"] = lt.newList(datastructure="ARRAYLIST")

    catalog["path"] = mp.newMap(numelements=100000,maptype="LINEAR_PROBING",loadfactor=0.95)
    
    catalog['connected'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareIATA) 

    catalog["salida"] = lt.newList()
    catalog['repeat'] = lt.newList()
    catalog['cities2'] = mp.newMap(maptype="PROBING", numelements= 41002)

    return catalog

def addAirport(catalog,airport):
    
    map = catalog['IATAS']
    entry = mp.get(map, airport["IATA"])
    if entry is None:    
        mp.put(map,airport["IATA"],airport)
        
    if not gr.containsVertex(catalog['routes'], airport["IATA"]):
        gr.insertVertex(catalog['routes'], airport["IATA"])
    return catalog

def addRoute(catalog, route):
    origen = route["Departure"]
    destino = route["Destination"]
    dist = route["distance_km"]

    #se agregan los arcos sin repetir al digrafo
    edge = gr.getEdge(catalog['routes'], origen, destino)
    if edge is None:
        gr.addEdge(catalog['routes'], origen, destino, dist)

    #se revisa si en el digrafo hay un arco de vuelta
    edge1 = gr.getEdge(catalog['routes'], destino, origen)    

    if edge1 != None:       
        #si hay un arco de vuelta significa que hay ruta de ida y vuelta y se agrega al grafo no dirigido   
        lt.addLast(catalog["salida"], origen)    
        if not gr.containsVertex(catalog['connected'], origen):
            gr.insertVertex(catalog['connected'], origen)
        if not gr.containsVertex(catalog['connected'], destino):
            gr.insertVertex(catalog['connected'], destino)

        edge2 = gr.getEdge(catalog['connected'], origen, destino)
        
        if edge2 is None:
            gr.addEdge(catalog['connected'], origen, destino, dist)
    

def addCity(catalog, route):
    city = route
    cities = catalog["cities"]
    lt.addLast(cities,city)

    city = route["city_ascii"]
    cities = catalog["cities2"]
    present = mp.contains(cities,city)
    if not present:
        mp.put(cities,city,route)
    else:
        lt.addLast(catalog['repeat'], city)
        city = city +"-"+ route['country']
        present= mp.contains(cities,city)
        if not present:
            mp.put(cities,city,route)
        else:
            city = city + '-' + route["id"]
            mp.put(cities,city,route)
        


def requerimiento2(catalog, IATA1, IATA2):

    g = catalog["routes"]

    catalog["scc"] = scc.KosarajuSCC(g)

    componentes = scc.connectedComponents(catalog["scc"])

    mismo = scc.stronglyConnected(catalog["scc"], IATA1, IATA2)
    print(" ")
    print("El total de clústeres en la red de transporte aéreo es de:  "+ str(componentes))
    
    if mismo:
        print("Los aeropuertos ingresados -SI- corresponden al mismo clúster aéreo")
    else:
        print("Los aeropuertos ingresados -NO- corresponden al mismo clúster aéreo")
    print(" ")

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


def compareIATA(stop, keyvaluestop):
    """
    Compara IATAS
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
