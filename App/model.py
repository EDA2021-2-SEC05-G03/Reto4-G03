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
from DISClib.Algorithms.Graphs import dfs
from math import radians, cos, sin, asin, sqrt
from DISClib.Algorithms.Graphs import dijsktra as dj

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
                'rama': None,
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
    catalog["rama"] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareIATA)

    catalog["cities"] = lt.newList(datastructure="ARRAYLIST")
    catalog["path"] = mp.newMap(numelements=100000,maptype="LINEAR_PROBING",loadfactor=0.95)
    catalog["salida"] = lt.newList()
    catalog['repeat'] = lt.newList()
    catalog['cities2'] = mp.newMap(maptype="PROBING", numelements= 41002)
    catalog['withroutes'] = lt.newList(datastructure="SINGLE_LINKED")
    catalog['repeatmap'] = mp.newMap(maptype="PROBING", comparefunction=compareIATA)
    catalog['latitudeairports'] = om.newMap(omaptype="RBT")
    catalog["longitudeairports"] = om.newMap(omaptype="RBT")

    return catalog


def addAirport(catalog,airport): 
    lat = airport["Latitude"]
    lon = airport["Longitude"]
    om.put(catalog["latitudeairports"],lat,airport)
    om.put(catalog["longitudeairports"],lon,airport)

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
        lista = lt.newList(datastructure="ARRAYLIST")
        lt.addLast(lista,route)
        mp.put(cities,city,lista)
    else:
        lt.addLast(catalog["repeat"],city)
        x = mp.get(cities,city)['value']
        lt.addLast(x,route)
        mp.put(cities,city,x)

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

def req3(catalog,ciudadorigen,ciudaddestino):
    lat1 = ciudadorigen["lat"]
    lat2= ciudaddestino["lat"]
    lon1 = ciudadorigen['lng']
    lon2 = ciudaddestino["lng"]
    originairport = airportnear(catalog,lat1,lon1)
    destinyairport = airportnear(catalog,lat2,lon2)
    distanceoriginairport = originairport[0]
    distancedestinyairport = destinyairport[0]
    originairport = originairport[1]
    destinyairport = destinyairport[1]

    init =  dj.Dijkstra(catalog['routes'],originairport['IATA'])

    if dj.hasPathTo(init,destinyairport["IATA"]):
        distanciavuelo = dj.distTo(init,destinyairport["IATA"])
        pilavuelo = dj.pathTo(init,destinyairport["IATA"])
        return (originairport,distanceoriginairport,destinyairport,distancedestinyairport,distanciavuelo,pilavuelo)
    else:
        print("No existe una ruta entre los aeropuertos de las dos ciudades")
    
    return (distanceoriginairport,distancedestinyairport,originairport,destinyairport)

def airportnear(catalog,lat,long):
    key= om.ceiling(catalog['latitudeairports'],lat)
    airportup = om.get(catalog["latitudeairports"],key)['value']
    key = om.floor(catalog['latitudeairports'], lat)
    airportdown = om.get(catalog['latitudeairports'],key)["value"]

    key = om.floor(catalog['longitudeairports'], long)
    airportleft = om.get(catalog['longitudeairports'],key)["value"]
    key = om.ceiling(catalog['longitudeairports'], long)
    airportright = om.get(catalog['longitudeairports'],key)["value"]
    airportuplatitude = airportup["Latitude"]
    airportuplongitude = airportup['Longitude']
    distanceup = haversine(long,lat,airportuplongitude,airportuplatitude)
    airportdownlatitude = airportdown["Latitude"]
    airportdownlongitude = airportdown["Longitude"]
    distancedown = haversine(long,lat,airportdownlongitude,airportdownlatitude)
    airportleftlatitude = airportleft["Latitude"]
    airportleftlongitude = airportleft["Longitude"]
    distanceleft = haversine(long,lat,airportleftlongitude,airportleftlatitude)
    airportrightlatitude = airportright["Latitude"]
    airportrightlongitude = airportright["Longitude"]
    distanceright = haversine(long,lat,airportrightlongitude,airportrightlatitude)
    distanciaminima = min(distanceup,distancedown,distanceleft,distanceright)
    if distanciaminima == distanceright:
        return (distanciaminima,airportright)
    elif distanciaminima == distanceleft:
        return (distanciaminima, airportleft)
    elif distanciaminima == distanceup:
        return (distanciaminima,airportup)
    else:
        return (distanciaminima,airportdown)

def haversine(lon1, lat1, lon2, lat2):
    lon1 = float(lon1)
    lat1 = float(lat1)
    lon2 = float(lon2)
    lat2 = float(lat2)

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

def req4(catalog, origen, millas):
    #Para obtener las rutas de ida y vuelta se toma el grafo no dirigido   
    mst = prim.PrimMST(catalog["connected"])
    arbol = mst["mst"]
    weight = prim.weightMST(catalog["routes"],mst) 
    l = 0
    for i in lt.iterator(arbol):
        a = i["vertexA"]
        b = i["vertexB"]
        w = i["weight"]
        if not gr.containsVertex(catalog['rama'], a):
            gr.insertVertex(catalog['rama'], a)
        if not gr.containsVertex(catalog['rama'], b):
            gr.insertVertex(catalog["rama"],b)
        edge = gr.getEdge(catalog['rama'], a, b)
        if edge is None:
            gr.addEdge(catalog["rama"],a,b,w)
    
    x = gr.vertices(catalog["rama"])

    df = dfs.DepthFirstSearch(catalog["rama"], origen)
    ver = gr.vertices(catalog["rama"])
    l = 0
    for g in lt.iterator(ver):
        path = dfs.pathTo(df,g)
        
        if path != None:
            s = path["size"]
            if s > l:
                l = s 
                mayor = path

    km = float(millas) * 1.60
    total_dis = weight*2

    print("El numero de nodos conectados a la red de expansión minima es de: "+ str(x["size"]))

    print("La suma de la distancia entre los aeropuertos es de: " + str(weight))

    print("El total de millas en kilometros del usuario es de: "+ str(km) + " km" )

    print()

    if km < total_dis:
        falta = total_dis - km
        falta = falta/1.6
        print("El usuario necesita " + str(round(falta,2)) + " millas más para completar el viaje")
    else:
        sobra = km-weight
        print("A el usuario le sobran " + str(sobra) + " para completar el viaje")

    print()
    print("El costo total de la red de ida y vuelta en Km es de : "+ str(total_dis))
    
    
    return mayor,km

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

def req6(catalog,iatainicio, iatafin,lat1,lon1,lat2,lon2):
    grafo = catalog["routes"]
    air1 = mp.get(catalog["IATAS"],iatainicio)["value"]
    air2 = mp.get(catalog["IATAS"], iatafin)["value"]
    air1lat = air1["Latitude"]
    air1lon = air1["Longitude"]
    air2lat = air2["Latitude"]
    air2lon = air2["Longitude"]
    distance1 = haversine(lon1,lat1,air1lon,air1lat)
    distance2 = haversine(lon2,lat2,air2lon,air2lat)
    init = dj.Dijkstra(grafo,iatainicio)
    if dj.hasPathTo(init,iatafin):
        distanciavuelo = dj.distTo(init,iatafin)
        pilavuelo = dj.pathTo(init,iatafin)
        return (distance1,distance2,distanciavuelo,pilavuelo)
    else: 
        print("No hay una ruta directa entre los dos aeropuertos más cercanos a las ciudades")


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

def v_req3(catalog,ruta,o,d):
    m = folium.Map(location=[33.39, -1.52], zoom_start=3)
    points = []
    lat11 = o["lat"]
    lon11 = o["lng"]
    lat22 = d["lat"]
    lon22 = d["lng"]
               
    folium.Marker(
                location=[lat11, lon11],
                popup=o["city"],
                icon=folium.Icon(color="blue",icon="circle"),).add_to(m)
    folium.Marker(
                location=[lat22, lon22],
                popup=d["city"],
                icon=folium.Icon(color="blue",icon="circle"),).add_to(m)
    points = []
    for i in lt.iterator(ruta):
        a = i["vertexA"] 
        b = i["vertexB"] 
        
        lat1 = mp.get(catalog["IATAS"],a)["value"]["Latitude"]    
        lon1 = mp.get(catalog["IATAS"],a)["value"]["Longitude"] 
        lat2 = mp.get(catalog["IATAS"],b)["value"]["Latitude"]    
        lon2 = mp.get(catalog["IATAS"],b)["value"]["Longitude"] 
        folium.Marker(
                location=[lat1, lon1],
                popup=a,
                icon=folium.Icon(color="purple",icon="plane"),).add_to(m)
        folium.Marker(
                location=[lat2, lon2],
                popup=b,
                icon=folium.Icon(color="purple",icon="plane"),).add_to(m)
        points.append([float(lat1),float(lon1)])
        points.append([float(lat2),float(lon2)])
    
    folium.PolyLine(locations=points, color="red",weight=.5).add_to(m)
    
    m.save("C:\\Users\\maril\\Desktop\\mapG03-R3.html")    
    m

def v_req4(catalog,path):
    m = folium.Map(location=[33.39, -1.52], zoom_start=2)
    point = []
    for i in lt.iterator(path):
        lat1 = mp.get(catalog["IATAS"],i)["value"]["Latitude"]    
        lon1 = mp.get(catalog["IATAS"],i)["value"]["Longitude"] 
        folium.Marker( 
                location=[lat1, lon1],
                popup=i,
                icon=folium.Icon(color="red",icon="plane"),
                ).add_to(m)
        point.append([float(lat1),float(lon1)])
    folium.PolyLine(locations=point, color="blue",weight=.5).add_to(m)
    m.save("C:\\Users\\maril\\Desktop\\mapG03-R4.html")    
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




