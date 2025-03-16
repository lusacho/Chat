# interfaz.py
import tkinter as tk
from laberinto import Laberinto

class InterfazLaberinto:
    def __init__(self, master):
        self.master = master
        self.zoom = 20  # píxeles por celda
        self.mostrar_info = tk.BooleanVar(value=True)
        self.entrada = (0, 0)
        self.salida = (9, 9)
        self.filas = 10
        self.columnas = 10
        self.laberinto = Laberinto(self.columnas, self.filas)
        self.crear_widgets()
        self.dibujar_laberinto()

    def crear_widgets(self):
        # Se crean dos marcos: uno para el canvas y otro para los controles (a la derecha)
        self.frame_canvas = tk.Frame(self.master)
        self.frame_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.frame_control = tk.Frame(self.master)
        self.frame_control.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas para dibujar el laberinto
        self.canvas = tk.Canvas(self.frame_canvas, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Controles: Filas y Columnas
        tk.Label(self.frame_control, text="Filas:").pack(pady=2)
        self.entry_filas = tk.Entry(self.frame_control, width=5)
        self.entry_filas.pack(pady=2)
        self.entry_filas.insert(0, str(self.filas))
        
        tk.Label(self.frame_control, text="Columnas:").pack(pady=2)
        self.entry_columnas = tk.Entry(self.frame_control, width=5)
        self.entry_columnas.pack(pady=2)
        self.entry_columnas.insert(0, str(self.columnas))
        
        # Botón "Situar E/S"
        self.btn_situar_es = tk.Button(self.frame_control, text="Situar E/S", command=self.situar_es)
        self.btn_situar_es.pack(pady=5)
        
        # Botón "Generar Grid"
        self.btn_generar_grid = tk.Button(self.frame_control, text="Generar Grid", command=self.generar_grid)
        self.btn_generar_grid.pack(pady=5)
        
        # Botones para modificar paredes
        tk.Label(self.frame_control, text="Paredes:").pack(pady=5)
        self.btn_agregar_pared = tk.Button(self.frame_control, text="+Pared", command=self.agregar_pared)
        self.btn_agregar_pared.pack(pady=2)
        self.btn_quitar_pared = tk.Button(self.frame_control, text="-Pared", command=self.quitar_pared)
        self.btn_quitar_pared.pack(pady=2)
        
        # Botones para modificar el camino (Way)
        tk.Label(self.frame_control, text="Way:").pack(pady=5)
        self.btn_agregar_way = tk.Button(self.frame_control, text="+Way", command=self.agregar_way)
        self.btn_agregar_way.pack(pady=2)
        self.btn_quitar_way = tk.Button(self.frame_control, text="-Way", command=self.quitar_way)
        self.btn_quitar_way.pack(pady=2)
        
        # Controles de Zoom
        tk.Label(self.frame_control, text="Zoom:").pack(pady=5)
        self.btn_zoom_in = tk.Button(self.frame_control, text="Zoom +", command=self.zoom_in)
        self.btn_zoom_in.pack(pady=2)
        self.btn_zoom_out = tk.Button(self.frame_control, text="Zoom -", command=self.zoom_out)
        self.btn_zoom_out.pack(pady=2)
        
        # Opción para mostrar/ocultar información
        self.chk_mostrar_info = tk.Checkbutton(self.frame_control, text="Mostrar Info", variable=self.mostrar_info, command=self.dibujar_laberinto)
        self.chk_mostrar_info.pack(pady=5)
        
        # Nuevos botones para "Completar Laberinto" y "Generar"
        self.btn_completar = tk.Button(self.frame_control, text="Completar Laberinto", command=self.completar_laberinto)
        self.btn_completar.pack(pady=5)
        self.btn_generar = tk.Button(self.frame_control, text="Generar", command=self.generar_laberinto)
        self.btn_generar.pack(pady=5)

    def situar_es(self):
        # Se sitúan la entrada en (0,0) y la salida en (filas-1, columnas-1)
        try:
            self.filas = int(self.entry_filas.get())
            self.columnas = int(self.entry_columnas.get())
        except:
            print("Error: Filas y Columnas deben ser números.")
            return
        self.entrada = (0, 0)
        self.salida = (self.filas - 1, self.columnas - 1)
        print(f"Entrada: {self.entrada}, Salida: {self.salida}")
        self.dibujar_laberinto()
        
    def generar_grid(self):
        try:
            self.filas = int(self.entry_filas.get())
            self.columnas = int(self.entry_columnas.get())
        except:
            print("Error: Filas y Columnas deben ser números.")
            return
        self.laberinto = Laberinto(self.columnas, self.filas)
        self.situar_es()  # Actualiza entrada y salida
        self.dibujar_laberinto()
        print("Grid generado.")
        
    def agregar_pared(self):
        # Funcionalidad para agregar pared manualmente (placeholder)
        print("Agregar pared (funcionalidad pendiente).")
        
    def quitar_pared(self):
        # Funcionalidad para quitar pared manualmente (placeholder)
        print("Quitar pared (funcionalidad pendiente).")
        
    def agregar_way(self):
        # Funcionalidad para agregar parte del camino (placeholder)
        print("Agregar Way (funcionalidad pendiente).")
        
    def quitar_way(self):
        # Funcionalidad para quitar parte del camino (placeholder)
        print("Quitar Way (funcionalidad pendiente).")
        
    def zoom_in(self):
        self.zoom += 5
        self.dibujar_laberinto()
        
    def zoom_out(self):
        if self.zoom > 5:
            self.zoom -= 5
        self.dibujar_laberinto()
        
    def completar_laberinto(self):
        # Invoca la función del objeto Laberinto y redibuja el canvas
        self.laberinto.completar_laberinto(self.entrada, self.salida, self.obtener_recorrido_manual())
        self.dibujar_laberinto()
        
    def generar_laberinto(self):
        # Invoca la función generar del objeto Laberinto y redibuja el canvas
        self.laberinto.generar(self.entrada, self.salida, self.obtener_recorrido_manual())
        self.dibujar_laberinto()
        
    def obtener_recorrido_manual(self):
        # Por defecto se usa una diagonal como recorrido manual de ejemplo.
        recorrido = [(i, i) for i in range(min(self.filas, self.columnas))]
        print("Recorrido manual:", recorrido)
        return recorrido
        
    def dibujar_laberinto(self):
        self.canvas.delete("all")
        if not self.laberinto:
            return
        # Dibuja el grid basándose en la información de self.laberinto.grid
        for i in range(self.filas):
            for j in range(self.columnas):
                x = j * self.zoom
                y = i * self.zoom
                cell = self.laberinto.grid[i][j]
                if cell['N']:
                    self.canvas.create_line(x, y, x + self.zoom, y)
                if cell['S']:
                    self.canvas.create_line(x, y + self.zoom, x + self.zoom, y + self.zoom)
                if cell['E']:
                    self.canvas.create_line(x + self.zoom, y, x + self.zoom, y + self.zoom)
                if cell['O']:
                    self.canvas.create_line(x, y, x, y + self.zoom)
                # Si la opción está activada, muestra la información de la celda
                if self.mostrar_info.get():
                    self.canvas.create_text(x + self.zoom/2, y + self.zoom/2, text=f"{i},{j}", font=("Arial", 8))
        # Dibuja la entrada (verde) y la salida (roja)
        ex, ey = self.entrada[1] * self.zoom, self.entrada[0] * self.zoom
        self.canvas.create_rectangle(ex, ey, ex+self.zoom, ey+self.zoom, fill="green")
        sx, sy = self.salida[1] * self.zoom, self.salida[0] * self.zoom
        self.canvas.create_rectangle(sx, sy, sx+self.zoom, sy+self.zoom, fill="red")
