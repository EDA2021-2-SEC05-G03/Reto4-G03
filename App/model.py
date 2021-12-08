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
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import bfs

import folium

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
                'cities2':None,
                'withroutes': None,
                }

    catalog['IATAS'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIATA)

    catalog['AN-ID'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIATA)

    catalog['routes'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareIATA)
    catalog['connected'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareIATA)
    catalog["cities"] = lt.newList(datastructure="ARRAYLIST")
    catalog["path"] = mp.newMap(numelements=100000,maptype="LINEAR_PROBING",loadfactor=0.95)
    catalog["salida"] = lt.newList()
    catalog['repeat'] = lt.newList()
    catalog['cities2'] = mp.newMap(maptype="PROBING", numelements= 41002)
    catalog['withroutes'] = lt.newList(datastructure="SINGLE_LINKED")

    return catalog


def addAirport(catalog,airport): 
    lt.addLast(catalog['salida'],airport["IATA"])
    map = catalog['IATAS']
    mp.put(map,airport["IATA"],airport)       
    mp.put(catalog["AN-ID"],airport["Name"],airport["IATA"]) 
    entry = mp.get(map, airport["IATA"])
    if entry is None:    
        mp.put(map,airport["IATA"],airport["Name"])
        
    if not gr.containsVertex(catalog['routes'], airport["IATA"]):
        gr.insertVertex(catalog['routes'], airport["IATA"])

    gr.insertVertex(catalog['connected'], airport["IATA"])

def addRoute(catalog, route):
    origen = route["Departure"]
    destino = route["Destination"]
    dist = route["distance_km"]
    presente = lt.isPresent(catalog['withroutes'],origen)
    presente2 = lt.isPresent(catalog["withroutes"], destino)
    if not presente:
        lt.addLast(catalog['withroutes'], origen)
    if not presente2:
        lt.addLast(catalog["withroutes"], destino)

    edge = gr.getEdge(catalog['routes'], origen, destino)
    if edge is None:
        gr.addEdge(catalog['routes'], origen, destino, float(dist))
        
    #se revisa si en el digrafo hay un arco de vuelta
    edge1 = gr.getEdge(catalog['routes'], destino, origen)    
    if edge1 != None:       
        #si hay un arco de vuelta significa que hay ruta de ida y vuelta y se agrega al grafo no dirigido   
        edge2 = gr.getEdge(catalog['connected'], destino, origen)      
        if edge2 == None:
            gr.addEdge(catalog['connected'], origen, destino, float(dist))
        
    

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

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datoss

# Funciones de consulta

def req1 (catalog):
    listIATAS = catalog['withroutes']
    best5 = om.newMap(omaptype = "RBT", comparefunction= compareroutes)
    for airport in lt.iterator(listIATAS):
        airportinfo = mp.get(catalog["IATAS"],airport)['value']
        indegree =  gr.indegree(catalog['routes'],airport)
        outdegree = gr.outdegree(catalog['routes'],airport)
        airportinfo["indegree"] = indegree
        airportinfo["outdegree"] = outdegree
        airportinfo["degree"] = indegree + outdegree
        om.put(best5,airportinfo,airportinfo)
    connected = lt.size(listIATAS)
    listasalida = lt.newList(datastructure="ARRAY_LIST")
    for x in range(5):
        key = om.maxKey(best5)
        lt.addLast(listasalida,key)
        om.deleteMax(best5)
    return (connected,listasalida)

def requerimiento2(catalog, IATA1, IATA2):

    g = catalog["routes"]

    catalog["scc"] = scc.KosarajuSCC(g)
    componentes = scc.connectedComponents(catalog["scc"])
    mismo = scc.stronglyConnected(catalog["scc"], IATA1, IATA2)

    return mismo,componentes

def req4(catalog, origen, millas):
    #Para obtener las rutas de ida y vuelta se toma el grafo no dirigido
    mst = prim.PrimMST(catalog["connected"])
    arbol = mst["mst"]
    weight = prim.weightMST(catalog["routes"],mst)  
    grafo = prim.prim(catalog["connected"], mst, origen)
    
    print(grafo)

    bf = bfs.BreadhtFisrtSearch(catalog["connected"], origen)

    for i in lt.iterator(arbol):
        print(i)
    
    pos_air = int(arbol["size"])
    km = float(millas) * 1.60
    print()
    print("El numero de nodos conectados a la red de expansión minima es de: "+ str(pos_air))
    print("El costo total de la red en Km es de : "+ str(weight))
    
    print("El total de millas en kilometros del usuario es de: "+ str(km) + " km" )


def req5(catalog,air):
    afectados = gr.degree(catalog["routes"],air)
    arcos = gr.adjacents(catalog["routes"], air)
    print("El total de aeropuertos afectados es de -"+str(afectados)+ "- si el aeropuerto "+ air +" se encuentra cerrado " )
    print("Los primeros y ultimos 3 aeropuertos afectados son:")

    prin2 = lt.newList(datastructure="ARRAY_LIST")

    s = lt.size(arcos)
    f = s-3
    while s > f:
        elm = lt.lastElement(arcos)
        p = lt.isPresent(prin2,elm)
        if p == 0:
            lt.addFirst(prin2,elm )      
            lt.removeLast(arcos)  
            s = lt.size(arcos)
        else:
            lt.removeLast(prin2)  

    prin1 = lt.newList(datastructure="ARRAY_LIST")
    c = 0  
    for i in lt.iterator(arcos):
        p = lt.isPresent(prin1,i)
        if c < 3 and p == 0:
            lt.addLast(prin1,i)         
            c+=1          
        elif p != 0:
            None
        else:
            break
    
    return prin1,prin2

def v_req1(catalog,info):
    m = folium.Map(location=[33.39, -1.52], zoom_start=2)
    points = []
    for i in lt.iterator(info):    
        airp = i["Name"]
        iata = mp.get(catalog["AN-ID"],airp)["value"]
        lat1 = mp.get(catalog["IATAS"],iata)["value"]["Latitude"]
        lon1 = mp.get(catalog["IATAS"],iata)["value"]["Longitude"]
        folium.Marker(
                location=[lat1, lon1],
                popup=iata,
                icon=folium.Icon(icon="plane"),).add_to(m)
        edges = gr.adjacentEdges(catalog["routes"],iata)
        for g in lt.iterator(edges):
            b = g["vertexB"]           
            lat2 = mp.get(catalog["IATAS"],b)["value"]["Latitude"]
            lon2 = mp.get(catalog["IATAS"],b)["value"]["Longitude"]
            points.append([float(lat1),float(lon1)])
            points.append([float(lat2),float(lon2)])
    
    folium.PolyLine(locations=points,color="red",weight=.5).add_to(m)
            
    m.save("C:\\Users\\maril\\Desktop\\mapG03-R1.html")    
    m

def v_req2(catalog,mismo,a,b):
    m = folium.Map(location=[33.39, -1.52], zoom_start=2) 
    lat1 = mp.get(catalog["IATAS"],a)["value"]["Latitude"]
    lon1 = mp.get(catalog["IATAS"],a)["value"]["Longitude"]
    lat2 = mp.get(catalog["IATAS"],b)["value"]["Latitude"]
    lon2 = mp.get(catalog["IATAS"],b)["value"]["Longitude"]
    if mismo[0]:
        folium.Marker(
                location=[lat1, lon1],
                popup=a,
                icon=folium.Icon(color="green",icon="plane"),).add_to(m)
        folium.Marker(
                location=[lat2, lon2],
                popup=b,
                icon=folium.Icon(color="green",icon="plane"),).add_to(m)
    else:
        folium.Marker(
                location=[lat1, lon1],
                popup=a,
                icon=folium.Icon(color="purple",icon="plane"),).add_to(m)
        folium.Marker(
                location=[lat2, lon2],
                popup=b,
                icon=folium.Icon(color="orange",icon="plane"),).add_to(m)

    m.save("C:\\Users\\maril\\Desktop\\mapG03-R2.html")    
    m


def v_req5(catalog,info,closed):
    m = folium.Map(location=[33.39, -1.52], zoom_start=2)
    points=[]
    lat1 = mp.get(catalog["IATAS"],closed)["value"]["Latitude"]    
    lon1 = mp.get(catalog["IATAS"],closed)["value"]["Longitude"]    
    folium.Marker( 
                location=[lat1, lon1],
                popup=closed,
                icon=folium.Icon(color="red",icon="plane"),
                ).add_to(m)
    
    for i in lt.iterator(info[0]):    
        if i != closed:
            lat2 = mp.get(catalog["IATAS"],i)["value"]["Latitude"]
            lon2 = mp.get(catalog["IATAS"],i)["value"]["Longitude"]
            
            points.append([float(lat1),float(lon1)])
            points.append([float(lat2),float(lon2)])
            folium.Marker(
                location=[lat2, lon2],
                popup=i,
                icon=folium.Icon(icon="plane"),).add_to(m)      
    
    for i in lt.iterator(info[1]):    
        if i != closed:
            lat2 = mp.get(catalog["IATAS"],i)["value"]["Latitude"]
            lon2 = mp.get(catalog["IATAS"],i)["value"]["Longitude"]
            
            points.append([float(lat1),float(lon1)])
            points.append([float(lat2),float(lon2)])
            folium.Marker(
                location=[lat2, lon2],
                popup=i,
                icon=folium.Icon(icon="plane"),).add_to(m)

    folium.PolyLine(locations=points, color="red",weight=.5).add_to(m)  
    
    m.save("C:\\Users\\maril\\Desktop\\mapG03-R5.html")    
    m
    

# Funciones utilizadas para comparar elementos dentro de una lista

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

def compareroutes(airport1,airport2):
    """
    Función de comparación requerimiento 1
    """
    airport1 = airport1['degree']
    airport2 = airport2['degree']
    if airport1 == airport2:
        return 0
    elif airport1 > airport2:
        return 1
    else:
        return -1




