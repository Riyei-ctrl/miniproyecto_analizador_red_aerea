"""
benchmarking.py
Módulo para el análisis empírico de complejidad algorítmica.
Utiliza datos reales de OpenFlights extraídos mediante datos.py.
"""

import time
from tda_rutas import ListaRutas
from datos import cargar_rutas_region

def medir_tiempo_lista_enlazada(datos_prueba):
    """Mide los tiempos de ejecucion de la Lista Doblemente Enlazada"""
    lista = ListaRutas("BenchmarkingListaEnlazada")
    tiempos = {}

    # Medir insercion ordenada
    inicio = time.perf_counter()
    for ruta in datos_prueba:
        # Se extraen los datos real4es del diccionario generado en datos.py
        lista.insertar(ruta["origen"], ruta["destino"], ruta["distancia"], ruta["escalas"])
    tiempos["insercion"] = time.perf_counter() - inicio
    
    # Medir recorrido
    inicio = time.perf_counter()
    actual = lista.cabeza
    while actual is not None:
        _ = actual
        actual = actual.siguiente
    tiempos["recorrido"] = time.perf_counter() - inicio

    # Medir eliminacion (Se eliminaran el 10% de las rutas)
    # max(1, ...) asegura que si hay pocos datos, al menos elimine 1
    rutas_a_eliminar = datos_prueba[:max(1, len(datos_prueba) // 10)]
    inicio = time.perf_counter()
    for ruta_del in rutas_a_eliminar:
        # Se extraen los datos real4es del diccionario generado en datos.py
        lista.eliminar(ruta_del["origen"], ruta_del["destino"])
    tiempos["eliminacion"] = time.perf_counter() - inicio

    return tiempos

def medir_arreglo_continuo(datos_prueba):
    """Mide los tiempos de ejecucion del arreglo continuo nativo (list de Python)"""
    arreglo_continuo = []
    tiempos = {}

    # Medir insercion ordenada
    inicio = time.perf_counter()
    for ruta_nueva in datos_prueba:
        insertado = False
        for i, ruta_existente in enumerate(arreglo_continuo):
            if ruta_nueva["origen"] < ruta_existente["origen"]:
                arreglo_continuo.insert(i, ruta_nueva)
                insertado = True
                break
        if not insertado:
            arreglo_continuo.append(ruta_nueva)
    tiempos["insercion"] = time.perf_counter() - inicio

    # Medir recorrido
    inicio = time.perf_counter()
    for ruta in arreglo_continuo:
        _ = ruta["origen"]
    tiempos["recorrido"] = time.perf_counter() - inicio

    # Medir eliminacion
    rutas_a_eliminar = datos_prueba[:max(1, len(datos_prueba) // 10)]
    inicio = time.perf_counter()
    for ruta_del in rutas_a_eliminar:
        for ruta in arreglo_continuo:
            if ruta["origen"] == ruta_del["origen"] and ruta["destino"] == ruta_del["destino"]:
                arreglo_continuo.remove(ruta) # Operacion con coste O(n)
                break
    tiempos["eliminacion"] = time.perf_counter() - inicio

    return tiempos