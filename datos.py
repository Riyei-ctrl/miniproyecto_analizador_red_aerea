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

    #2.Cargar datos tratando el string "\N" de OpenFlights como valor nulo(NaN)
    try:
        df_airports=pd.read_csv(ruta_airports_csv,names=cols_airports,na_values="\\N")
        df_routes= pd.read_csv(ruta_routes_csv,names=cols_routes,na_values="\\N")
    except FileNotFoundError:
        print("Error:No se encontraron los archivos CSV.Verifica las rutas.")
        return[]
    #3.Limpieza:Eliminar aeropuertos sin codigo IATA
    df_airports=df_airports.dropna(subset=["IATA"])

    #4. Filtrar aeropuertos por el subconjunto de trabajo(ejemplo: un pais o continente)
    df_region=df_airports[df_airports["Country"]== pais_asignado]
    iata_region = set(df_region["IATA"].tolist())

    #5.Filtrar rutas donde el aeropuerto de origen pertenezca a la region asignada
    df_rutas_region = df_routes[df_routes["Source"].isin(iata_region)].copy()
    df_rutas_region=df_rutas_region.dropna(subset=["Source","Dest"])

    #6. Mapear coordenadas para calcular distancias
    dicc_coords=df_airports.set_index("IATA")[["Lat","Lon"]].to_dict("index")

    rutas_procesadas=[]

