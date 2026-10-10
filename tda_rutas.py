"""
tda_rutas.py
Implementacion del tipo de dato abstracto
Estructura: lista doblemente enlazada
"""

class NodoRuta:
    """
    Representa una ruta de vuelo individual
    """
    def __init__(self, origen, destino, distancia, escalas = 0):
        self.origen = origen
        self.destino = destino
        self.distancia = distancia
        self.escalas = escalas

        self.siguiente = None
        self.anterior = None

    def __str__(self):
        return f"({self.origen} -> {self.destino} | {self.distancia}km)"

class ListaRutas:
    """
    TDA que gestiona las rutas de una aerolinea
    Mantiene las rutas ordenadas alfabeticamente por aeropuerto de origen
    """
    def __init__(self, aerolinea):
        self.aerolinea = aerolinea
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    def vacia(self):
        """
        Complejidad: O(1)
        """
        return self.cabeza is None

    def insertar(self, origen, destino, distancia, escalas = 0):
        """
        Inserta una nueva ruta manteniendo el orden alfabetico por el aeropuerto de origen
        Precondicion: Los datos de origen y destino deben ser cadenas de texto
        Poscondicion: El tamaño de la lista aumenta en 1 y la ruta queda en su posicion alfabetica
        Complejidad: O(n) en el peor de los casos, O(1) en el mejor (insercion de inicio)
        """
        nuevo_nodo = NodoRuta(origen, destino, distancia, escalas)

        if self.vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
            self.tamano += 1
            return

        if origen < self.cabeza.origen:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
            self.tamano += 1
            return

        actual = self.cabeza
        while actual.siguiente is not None and actual.siguiente.origen <= origen:
            actual = actual.siguiente

        if actual.siguiente is None:
            actual.siguiente = nuevo_nodo
            nuevo_nodo.anterior = actual
            self.cola = nuevo_nodo
        else:
            actual.siguiente.anterior = nuevo_nodo
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.anterior = actual

        self.tamano += 1

    def eliminar(self, origen, destino):
        """
        Busca y Elimina una ruta especifica basada en su origen y destino.
        Precondicion: La lista no debe estar vacia.
        Poscondicion: Si la ruta existe, se elimina, se reasignan los punteros y el tamaño disminuye
        Complejidad: O(n) en el peor de los casos.
        """
        if self.vacia():
            return False

        actual = self.cabeza

        while actual is not None:
            if actual.origen == origen and actual.destino == destino:
                if actual == self.cabeza:
                    self.cabeza = actual.siguiente
                    if self.cabeza:
                        self.cabeza.anterior = None
                else:
                    self.cola = None # La lista quedó vacia

            elif actual == self.cola:
                self.cola = actual.anterior
                self.cola.siguiente = None

            else:
                actual.anterior.siguiente = actual.siguiente
                actual.siguiente.anterior = actual.anterior

            self.tamano -= 1
            return True

            actual = actual.siguiente

        return False