#carga de datos, instanciación del TDA y la resolución de problemas (iterativos y recursivos).

import sys
from tda_rutas import ListaDobleRutas
from datos import cargar_rutas_region

#ayuda a que no colapse el programa
sys.setrecursionlimit(2000) 

def localizar_rutas_origen(tda_rutas, aeropuerto_origen):
    # Localiza todas las rutas que parten de un aeropuerto dado.
    print(f"\n--- Rutas partiendo desde {aeropuerto_origen} ---")
    actual = tda_rutas.cabeza
    encontradas = 0

    while actual is not None:
        if actual.origen == aeropuerto_origen:
            print(f" -> Destino: {actual.destino} | Distancia: {actual.distancia} km | Escalas: {actual.escalas}")
            encontradas += 1
        # Optimización algorítmica: 
        # Como el TDA está ordenado, si el origen actual es alfabéticamente mayor, 
        # ya no habrá más coincidencias. Rompemos el ciclo temprano.
        elif actual.origen > aeropuerto_origen:
            break
        actual = actual.siguiente
        
    if encontradas == 0:
        print("No se encontraron rutas directas para este aeropuerto en la región.")
    return encontradas

def calcular_itinerario_recursivo(tda_rutas, secuencia_iata, indice=0):
    #Calcula la distancia total y escalas de un itinerario mediante recursividad. 
    #base:el índice alcanza el último aeropuerto de la secuencia
    #recursivivdad: se busca la distancia entre el nodo actual y el siguiente y se suma al resto de la secuencia

    if indice >= len(secuencia_iata) -1:
        return 0, 0

    origen_actual = secuencia_iata[indice]
    destino_siguiente = secuencia_iata[indice + 1]

    #buscar lista enlazada
    actual = tda_rutas.cabeza
    tramo_encontrado = None
    while actual is not None and actual.origen <= origen_actual:
        if actual.origen == origen_actual and actual.destino == destino_siguiente:
            tramo_encontrado = actual
            break
        actual = actual.siguiente

    if tramo_encontrado is None:
        print(f"ERROR: No existe una ruta entre {origen_actual} y {destino_siguiente}.   ")  
        return -1, -1 #detiene el calculo

    #se llama recursiva para el resto
    distancia_restante, escalas_restantes = calcular_itinerario_recursivo(tda_rutas, secuencia_iata, indice + 1)

    if distancia_restante == -1:
        return -1, -1

    distancia_total = tramo_encontrado.distancia + distancia_restante

    #se suman las escalas
    conexion = 1 if indice + 1 < len(secuencia_iata) -1 else 0
    escalas_total = tramo_encontrado.escalas +  escalas_restantes +  conexion

    return distancia_total, escalas_total

def main():
    print("Iniciando analizador de la red aérea mundial... ")

    #cargar datos
    print("Extrayendo datos de OpenFlights y calculando distancias.")
    datos_procesados = cargar_rutas_region("data/airports.dat", "data/routes.dat", "México")

    if not datos_procesados:
        print("Deteniendo ejecución:Faltan datos en 'data/'.")
        return

    #instanciar dato abstracto
    red_aerea = ListaDobleRutas("Región asignada")

    #TDA
    print(f"Insertando  {len(datos_procesados)} rutas en la lista doblemente enlazada.")
    for ruta in datos_procesados:
        red_aerea.insertar_ordenado(ruta['origen'], ruta['destino'], ruta['distancia'], ruta['escalas'])

    print("Estructura de datos enlazada, lista para colsultas.")

    #pruebas
    while True:
        print("\n" + "=" *45)
        print("MENÚ DE ANÁLISIS DE LA RED AÉREA")
        print("=" *45)
        print(" 1. Localizar rutas desde un aeropuerto.")
        print(" 2. Calcular itinerario de viaje.")
        print(" 3. Salir.")
        opcion = input("Selecciona una opción (1-3): ")

        if opcion == "1":
            origen = input("Ingresa el código IATA del aeropuerto de origen (Ej. MEX, MTY, CUN): ").upper()
            localizar_rutas_origen(red_aerea, origen)

        elif opcion == "2":
            entrada = input("Ingresa la secuencia del viaje separados por guion (Ej. MEX-CUN-MTY): ").upper()
            secuencia = entrada.split(" - ")

            if len(secuencia) < 2:
                print("Un itinerario debe tener al menos un punto de origen y un destino.")
                continue

            distancia, escalas = calcular_itinerario_recursivo(red_aerea, secuencia)
            if distancia != -1:
                print(f"\n --- Resumen del itinerario {' -> '.join(secuencia)} --- ")
                print(f"Distancia total a recorrer: {distancia:.2f} km")
                print(f"Número de escalas de la ruta: {escalas}")

        elif opcion == "3":
            print("Cerrando...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()                