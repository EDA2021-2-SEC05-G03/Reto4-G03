﻿"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadDataAir(catalog,airportsfile):
    servicesfile = cf.data_dir + airportsfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    iteration = 0
    airportdirigido = None
    for airport in input_file:
        model.addAirport(catalog,airport) 
        if iteration ==0:
            airportdirigido = airport
            iteration += 1
    return airportdirigido

def loadDataRoute(catalog,routesfile):
    servicesfile = cf.data_dir + routesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for route in input_file:      
        model.addRoute(catalog, route) 
       
def loadDataCities(catalog,cityfile):
    servicesfile = cf.data_dir + cityfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for city in input_file:      
        model.addCity(catalog,city)
       
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def req2(catalog, air1, air2):
    model.requerimiento2(catalog, air1, air2)
