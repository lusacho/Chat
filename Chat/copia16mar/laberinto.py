# laberinto.py

class Laberinto:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        # Cada celda es un diccionario que indica la presencia (True) o ausencia (False) de una pared en cada dirección.
        self.grid = [[{'N': False, 'S': False, 'E': False, 'O': False} for _ in range(ancho)] for _ in range(alto)]
    
    def agregar_pared(self, fila, columna, direccion):
        """Agrega una pared en la dirección indicada para la celda (fila, columna)."""
        self.grid[fila][columna][direccion] = True

    def eliminar_pared(self, fila, columna, direccion):
        """Elimina la pared en la dirección indicada para la celda (fila, columna)."""
        self.grid[fila][columna][direccion] = False

    def remove_wall_between(self, cell1, cell2):
        """
        Elimina la pared entre dos celdas adyacentes.
        cell1 y cell2 son tuplas (fila, columna).
        """
        i1, j1 = cell1
        i2, j2 = cell2
        if i1 == i2:
            if j2 == j1 + 1:
                # cell2 está al Este de cell1
                self.eliminar_pared(i1, j1, 'E')
                self.eliminar_pared(i2, j2, 'O')
            elif j2 == j1 - 1:
                self.eliminar_pared(i1, j1, 'O')
                self.eliminar_pared(i2, j2, 'E')
        elif j1 == j2:
            if i2 == i1 + 1:
                self.eliminar_pared(i1, j1, 'S')
                self.eliminar_pared(i2, j2, 'N')
            elif i2 == i1 - 1:
                self.eliminar_pared(i1, j1, 'N')
                self.eliminar_pared(i2, j2, 'S')

    def get_neighbors(self, cell):
        """
        Retorna una lista de celdas vecinas a 'cell' (fila, columna) a las que se puede acceder
        (es decir, sin pared intermedia).
        """
        i, j = cell
        neighbors = []
        # Norte
        if i > 0 and not self.grid[i][j]['N'] and not self.grid[i-1][j]['S']:
            neighbors.append((i-1, j))
        # Sur
        if i < self.alto - 1 and not self.grid[i][j]['S'] and not self.grid[i+1][j]['N']:
            neighbors.append((i+1, j))
        # Este
        if j < self.ancho - 1 and not self.grid[i][j]['E'] and not self.grid[i][j+1]['O']:
            neighbors.append((i, j+1))
        # Oeste
        if j > 0 and not self.grid[i][j]['O'] and not self.grid[i][j-1]['E']:
            neighbors.append((i, j-1))
        return neighbors

    def dfs_path(self, start, end):
        """
        Realiza una búsqueda en profundidad (DFS) para encontrar el camino único entre start y end.
        Retorna la lista de celdas que forman el camino o None si no se encuentra.
        """
        stack = [(start, [start])]
        visited = set()
        while stack:
            (current, path) = stack.pop()
            if current == end:
                return path
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
        return None

    def _flood_fill(self, start, accesibles):
        """
        Algoritmo de flood fill para marcar las celdas accesibles a partir de 'start'.
        """
        stack = [start]
        while stack:
            cell = stack.pop()
            if cell in accesibles:
                continue
            accesibles.add(cell)
            for neighbor in self.get_neighbors(cell):
                if neighbor not in accesibles:
                    stack.append(neighbor)

    def completar_laberinto(self, entrada, salida, recorrido_manual):
        """
        Completa el laberinto conectando las celdas inaccesibles.
        Se asume que:
          - La función situar_es() ya ha definido la entrada y salida.
          - El usuario ha dibujado un recorrido manual válido.
        Utiliza flood fill para detectar celdas aisladas y conecta cada una con un vecino accesible.
        """
        print("Ejecutando completar_laberinto...")
        accesibles = set()
        self._flood_fill(entrada, accesibles)
        # Conectar las celdas que no fueron alcanzadas
        for i in range(self.alto):
            for j in range(self.ancho):
                if (i, j) not in accesibles:
                    for neighbor in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if 0 <= neighbor[0] < self.alto and 0 <= neighbor[1] < self.ancho:
                            if neighbor in accesibles:
                                self.remove_wall_between((i, j), neighbor)
                                self._flood_fill(entrada, accesibles)
                                break
        print("Laberinto completado.")

    def generar(self, entrada, salida, recorrido_manual):
        """
        Genera el laberinto partiendo de un grid en blanco a partir de:
          - Puntos de entrada y salida.
          - Un recorrido manual dibujado que conecta la entrada y salida.
        
        Procedimiento:
          1. Reinicia el grid eliminando todas las paredes.
          2. Agrega paredes en todas las celdas que no pertenecen al recorrido manual,
             de modo que el recorrido marcado sea la única vía sin paredes.
          3. Verifica que el recorrido manual sea la única solución entre entrada y salida.
          4. Conecta todas las celdas aisladas sin crear ciclos.
        """
        print("Inicializando grid sin paredes...")
        # Paso 1: Reiniciar el grid
        for fila in range(self.alto):
            for columna in range(self.ancho):
                self.grid[fila][columna] = {'N': False, 'S': False, 'E': False, 'O': False}
        # Asegurar la conectividad del recorrido manual: remover las paredes entre celdas consecutivas.
        for index in range(len(recorrido_manual) - 1):
            cell1 = recorrido_manual[index]
            cell2 = recorrido_manual[index + 1]
            self.remove_wall_between(cell1, cell2)
        # Paso 2: Agregar paredes en todas las celdas que NO pertenecen al recorrido manual.
        for fila in range(self.alto):
            for columna in range(self.ancho):
                if (fila, columna) not in recorrido_manual:
                    if fila > 0:
                        self.agregar_pared(fila, columna, 'N')
                    if fila < self.alto - 1:
                        self.agregar_pared(fila, columna, 'S')
                    if columna > 0:
                        self.agregar_pared(fila, columna, 'O')
                    if columna < self.ancho - 1:
                        self.agregar_pared(fila, columna, 'E')
        # Paso 3: Verificar que el recorrido manual sea la única solución.
        path = self.dfs_path(entrada, salida)
        if path != recorrido_manual:
            print("Advertencia: El recorrido manual no es la única solución. Reforzando el recorrido manual...")
            for index in range(len(recorrido_manual) - 1):
                cell1 = recorrido_manual[index]
                cell2 = recorrido_manual[index + 1]
                self.remove_wall_between(cell1, cell2)
            path = self.dfs_path(entrada, salida)
            if path != recorrido_manual:
                print("Error: No se pudo forzar la unicidad del recorrido manual.")
        # Paso 4: Conectar todas las celdas aisladas sin crear ciclos.
        print("Conectando celdas aisladas...")
        accessible = set(recorrido_manual)  # Se parte del recorrido manual como columna vertebral
        progress = True
        while progress:
            progress = False
            for i in range(self.alto):
                for j in range(self.ancho):
                    if (i, j) not in accessible:
                        vecinos = []
                        if i > 0 and ((i - 1, j) in accessible):
                            vecinos.append((i - 1, j))
                        if i < self.alto - 1 and ((i + 1, j) in accessible):
                            vecinos.append((i + 1, j))
                        if j > 0 and ((i, j - 1) in accessible):
                            vecinos.append((i, j - 1))
                        if j < self.ancho - 1 and ((i, j + 1) in accessible):
                            vecinos.append((i, j + 1))
                        if len(vecinos) >= 1:
                            self.remove_wall_between((i, j), vecinos[0])
                            accessible.add((i, j))
                            progress = True
        final_path = self.dfs_path(entrada, salida)
        if final_path != recorrido_manual:
            print("Advertencia: La conexión de celdas aisladas ha modificado la solución.")
        else:
            print("Generación del laberinto completada exitosamente.")
