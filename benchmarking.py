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

def medir_arreglo_contiguo(datos_prueba):
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

if __name__ == "__main__":
    print("Cargando datos reales de OpenFlights...")
    # Asegúrate de tener tus archivos en la carpeta data/
    datos_completos = cargar_rutas_region("data/airports.dat", "data/routes.dat", "Mexico")
    
    total_rutas = len(datos_completos)
    print(f"Total de rutas reales encontradas para la región: {total_rutas}\n")
    
    if total_rutas == 0:
        print("No se encontraron rutas. Revisa la ruta de los archivos o el país asignado.")
    else:
        # La rúbrica exige graficar 3 tamaños de entrada. 
        # Dividimos el total de datos reales en 3 proporciones.
        tamanos_n = [total_rutas // 4, total_rutas // 2, total_rutas]
        
        print(f"{'N (Tamaño)':<12} | {'Operación':<15} | {'TDA Enlazado (s)':<18} | {'Lista Nativa (s)':<18}")
        print("-" * 70)

        for n in tamanos_n:
            if n == 0: 
                continue
                
            # Tomamos una 'rebanada' (slice) del arreglo de datos reales
            datos_n = datos_completos[:n]
            
            tiempos_tda = medir_tiempo_lista_enlazada(datos_n)
            tiempos_nativa = medir_arreglo_contiguo(datos_n)
            
            print(f"{n:<12} | {'Inserción':<15} | {tiempos_tda['insercion']:<18.5f} | {tiempos_nativa['insercion']:<18.5f}")
            print(f"{'':<12} | {'Recorrido':<15} | {tiempos_tda['recorrido']:<18.5f} | {tiempos_nativa['recorrido']:<18.5f}")
            print(f"{'':<12} | {'Eliminación':<15} | {tiempos_tda['eliminacion']:<18.5f} | {tiempos_nativa['eliminacion']:<18.5f}")
            print("-" * 70)