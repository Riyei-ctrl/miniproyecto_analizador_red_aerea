"""
main.py
Punto de entrada principal para el Analizador de la red aérea mundial.
Orquesta la carga de datos, instanciación del TDA y la resolución de problemas (iterativos y recursivos).
"""
import sys
from tda_rutas import ListaDobleRutas
from datos import cargar_rutas_region

# Control de la profundidad de pila de Python (Documentado para la rúbrica U2)
# Limitamos o ampliamos explícitamente según la necesidad del hardware para evitar StackOverflow
sys.setrecursionlimit(2000) 

def localizar_rutas_origen(tda_rutas, aeropuerto_origen):
    """
    Problema 3: Localiza todas las rutas que parten de un aeropuerto dado.
    Aprovecha que la lista está ordenada alfabéticamente para detener la búsqueda anticipadamente.
    Complejidad: O(n) en el peor de los casos, pero optimizada empíricamente.
    """
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