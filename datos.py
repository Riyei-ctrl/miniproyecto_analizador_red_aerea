import pandas as pd
import math

def calcular_distancia(lat1,lon1,lat2,lon2):
    """
    Calcula la distancia en kilometros entre dos coordenadas usando la formula de Haversine.
    Calcula la distancia más corta sobre la superficie de una esfera (como la Tierra) entre dos puntos definidos por su latitud y longitud.
    """
    R=6371.0 #Radio de la tierra en km
    lat1_rad,lon1_rad=math.radians(lat1), math.radians(lon1)
    lat2_rad,lon2_rad=math.radians(lat2), math.radians(lon2)

    dlat=lat2_rad - lat1_rad
    dlon=lon2_rad - lon1_rad

    a=math.sin(dlat/2)**2+ math.cos(lat1_rad)*math.cos(lat2_rad)*math.sin(dlon/2)**2
    c=2* math.atan2(math.sqrt(a),math.sqrt(1-a))

    return round(R*c,2)

def cargar_rutas_region(ruta_airports_csv, ruta_routes_csv, pais_asignado="Mexico"):
    """
    Lee los datasets de OpenFlights, limpia los nulos y filtra por la region asignada.
    Retorna una lista de diccionarios lista para inyectarse en el TDA.
    """
    #1. Definir columnas segun la documentacion de OpenFlights
    cols_airports=["AirportID","Name","City","Country","IATA", "ICAO","Lat","Lon","Alt","Timezone","DST","Tz","Type","Source"]
    cols_routes=["Airline","AirlineID", "Source","SourceID","Dest","DestID","Codeshare","Stops","Equipment"]
    