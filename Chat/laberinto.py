# laberinto.py

import numpy as np

class Laberinto:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.grid = np.zeros((filas, columnas))  # Representa el grid; se usa para visualización, si se desea.
        self.inicio = None    # Celda de entrada (fila, columna)
        self.fin = None       # Celda de salida (fila, columna)
        self.recorrido = []   # Lista de celdas del recorrido manual (solución)
        self.waypoints = []   # Lista de waypoints añadidos al recorrido
        self.paredes = {}     # Diccionario: clave = (fila, columna), valor = lista de paredes ('N','E','S','O')
    
    def generar_grid(self):
        """Reinicia el laberinto y sus variables."""
        self.grid = np.zeros((self.filas, self.columnas))
        self.inicio = None
        self.fin = None
        self.recorrido = []
        self.waypoints = []
        self.paredes = {}
    
    def situar_es(self, inicio, fin):
        """
        Establece la entrada y la salida.
        inicio y fin son tuplas (fila, columna).
        """
        self.inicio = inicio
        self.fin = fin
        self.recorrido = [inicio]
    
    def actualizar_recorrido(self, celda):
        """
        Actualiza el recorrido manual.
        Si la celda ya existe en el recorrido, retrocede hasta esa posición;
        de lo contrario, añade la celda al final del recorrido.
        """
        if celda in self.recorrido:
            indice = self.recorrido.index(celda)
            self.recorrido = self.recorrido[:indice+1]
        else:
            self.recorrido.append(celda)
    
    def agregar_waypoint(self, celda):
        """Agrega la celda como waypoint si no está ya en la lista."""
        if celda not in self.waypoints:
            self.waypoints.append(celda)
    
    def eliminar_waypoint(self, celda):
        """Elimina la celda de la lista de waypoints, si está presente."""
        if celda in self.waypoints:
            self.waypoints.remove(celda)
    
    def agregar_pared(self, celda):
        """
        Agrega una pared en la celda, siguiendo el orden: 'N', 'E', 'S', 'O'.
        Cada clic añade la siguiente pared que aún no esté presente.
        """
        if celda not in self.paredes:
            self.paredes[celda] = []
        orden = ['N', 'E', 'S', 'O']
        for p in orden:
            if p not in self.paredes[celda]:
                self.paredes[celda].append(p)
                break  # Agrega solo una pared por llamada
    
    def quitar_pared(self, celda):
        """
        Quita una pared de la celda siguiendo el mismo orden (quita la que esté primero).
        """
        if celda in self.paredes and self.paredes[celda]:
            self.paredes[celda].pop(0)
    
    def generar_paredes_completas(self):
        """
        Función placeholder para completar el laberinto:
        aquí se implementaría la lógica para, a partir del recorrido y las modificaciones,
        generar automáticamente las paredes necesarias para que todas las celdas sean accesibles.
        """
        pass
