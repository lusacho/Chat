# interfaz.py
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from laberinto import Laberinto  # Asegúrate de que laberinto.py esté en el mismo directorio o en el PYTHONPATH
import numpy as np

# Variables globales de visualización (pueden usarse o trasladarse a variables de instancia)
tam_celda = 40  # Tamaño base de cada celda (se ajusta con zoom)
zoom_factor = 1.0

# Definiciones de colores para Matplotlib (valores entre 0 y 1)
COLOR_FONDO = (1, 1, 1)         # blanco
COLOR_GRID = (0.9, 0.9, 0.9)      # gris claro
COLOR_PARED = (0, 0, 0)           # negro
COLOR_INICIO = (0, 1, 0)          # verde
COLOR_FIN = (1, 0, 0)             # rojo
COLOR_SOLUCION = (1, 0, 0)        # rojo para el recorrido manual
COLOR_WAYPOINT = (0.5, 0, 0.5)    # morado para waypoints

# Variable para el modo de interacción; se usará para determinar la acción en el clic
# Los posibles modos son: "grid", "situar_es", "recorrido_manual", "agregar_way", "eliminar_way", "anadir_pared", "quitar_pared", "generar_paredes"
modo = "grid"

class InterfazLaberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Laberintos Manuales")
        # Configurar la ventana para que se ajuste al tamaño de pantalla (se usa un tamaño grande de ejemplo)
        self.root.geometry("1200x800")
        
        # Inicializar variables del laberinto
        self.laberinto = None
        
        # Crear la figura de Matplotlib y el canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Panel de control a la derecha
        self.frame_control = ttk.Frame(self.root, padding="10")
        self.frame_control.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Campos de entrada para filas y columnas
        ttk.Label(self.frame_control, text="Filas:").pack(pady=5)
        self.entry_filas = ttk.Entry(self.frame_control, width=10)
        self.entry_filas.insert(0, "10")
        self.entry_filas.pack(pady=5)
        
        ttk.Label(self.frame_control, text="Columnas:").pack(pady=5)
        self.entry_columnas = ttk.Entry(self.frame_control, width=10)
        self.entry_columnas.insert(0, "10")
        self.entry_columnas.pack(pady=5)
        
        # Botones de control
        ttk.Button(self.frame_control, text="Generar Grid", command=self.btn_generar_grid).pack(pady=5)
        ttk.Button(self.frame_control, text="Situar E/S", command=self.btn_situar_es).pack(pady=5)
        ttk.Button(self.frame_control, text="Recorrido Manual", command=self.btn_recorrido_manual).pack(pady=5)
        
        # Botones para waypoints (divididos en dos)
        frame_way = ttk.Frame(self.frame_control)
        frame_way.pack(pady=5)
        ttk.Button(frame_way, text="+ Way", command=self.btn_agregar_way).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_way, text="- Way", command=self.btn_eliminar_way).pack(side=tk.LEFT, padx=5)
        
        # Botones para edición de paredes (divididos en dos)
        frame_pared = ttk.Frame(self.frame_control)
        frame_pared.pack(pady=5)
        ttk.Button(frame_pared, text="+ Pared", command=self.btn_agregar_pared).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_pared, text="- Pared", command=self.btn_quitar_pared).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.frame_control, text="Generar Paredes", command=self.btn_generar_paredes).pack(pady=5)
        
        # Botones de zoom
        frame_zoom = ttk.Frame(self.frame_control)
        frame_zoom.pack(pady=5)
        ttk.Button(frame_zoom, text="Zoom In", command=self.zoom_in).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_zoom, text="Zoom Out", command=self.zoom_out).pack(side=tk.LEFT, padx=5)
        
        # Opciones de visualización
        self.var_mostrar_es = tk.BooleanVar(value=True)
        self.var_mostrar_sol = tk.BooleanVar(value=True)
        self.var_mostrar_way = tk.BooleanVar(value=True)
        self.var_mostrar_pared = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.frame_control, text="Mostrar E/S", variable=self.var_mostrar_es, command=self.actualizar_canvas).pack(pady=5)
        ttk.Checkbutton(self.frame_control, text="Mostrar Solución", variable=self.var_mostrar_sol, command=self.actualizar_canvas).pack(pady=5)
        ttk.Checkbutton(self.frame_control, text="Mostrar Waypoints", variable=self.var_mostrar_way, command=self.actualizar_canvas).pack(pady=5)
        ttk.Checkbutton(self.frame_control, text="Mostrar Paredes", variable=self.var_mostrar_pared, command=self.actualizar_canvas).pack(pady=5)
        
        self.bind_eventos()
    
    def bind_eventos(self):
        # Vincular eventos de clic en el canvas y de teclado en la ventana principal
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.root.bind("<Key>", self.on_key)
    
    def btn_generar_grid(self):
        global tam_celda, zoom_factor, modo
        try:
            filas = int(self.entry_filas.get())
            columnas = int(self.entry_columnas.get())
        except:
            messagebox.showerror("Error", "Valores inválidos para filas/columnas.")
            return
        self.laberinto = Laberinto(filas, columnas)
        self.laberinto.generar_grid()
        modo = "grid"
        zoom_factor = 1.0
        tam_celda = 40
        self.actualizar_canvas()
    
    def btn_situar_es(self):
        global modo
        modo = "situar_es"
    
    def btn_recorrido_manual(self):
        global modo
        modo = "recorrido_manual"
    
    def btn_agregar_way(self):
        global modo
        modo = "agregar_way"
    
    def btn_eliminar_way(self):
        global modo
        modo = "eliminar_way"
    
    def btn_agregar_pared(self):
        global modo
        modo = "anadir_pared"
    
    def btn_quitar_pared(self):
        global modo
        modo = "quitar_pared"
    
    def btn_generar_paredes(self):
        global modo
        modo = "generar_paredes"
        if self.laberinto:
            self.laberinto.generar_paredes_completas()
        self.actualizar_canvas()
    
    def zoom_in(self):
        global zoom_factor
        zoom_factor *= 1.1
        self.actualizar_canvas()
    
    def zoom_out(self):
        global zoom_factor
        zoom_factor /= 1.1
        self.actualizar_canvas()
    
    def on_click(self, event):
        global tam_celda, zoom_factor, modo
        if not self.laberinto or event.inaxes is None:
            return
        col = int(event.xdata // (tam_celda * zoom_factor))
        fila = int(event.ydata // (tam_celda * zoom_factor))
        celda = (fila, col)
        if modo == "situar_es":
            # Permitir que el usuario sitúe E/S manualmente
            if self.laberinto.inicio is None:
                self.laberinto.inicio = celda
            elif self.laberinto.fin is None:
                self.laberinto.fin = celda
            self.actualizar_canvas()
        elif modo == "recorrido_manual":
            if self.laberinto.recorrido:
                if celda in self.laberinto.recorrido:
                    indice = self.laberinto.recorrido.index(celda)
                    self.laberinto.recorrido = self.laberinto.recorrido[:indice+1]
                else:
                    self.laberinto.actualizar_recorrido(celda)
            else:
                self.laberinto.recorrido.append(celda)
            self.actualizar_canvas()
        elif modo == "agregar_way":
            self.laberinto.agregar_waypoint(celda)
            self.actualizar_canvas()
        elif modo == "eliminar_way":
            self.laberinto.eliminar_waypoint(celda)
            self.actualizar_canvas()
        elif modo == "anadir_pared":
            self.laberinto.agregar_pared(celda)
            self.actualizar_canvas()
        elif modo == "quitar_pared":
            self.laberinto.quitar_pared(celda)
            self.actualizar_canvas()
    
    def on_key(self, event):
        global modo
        if modo == "recorrido_manual" and self.laberinto and self.laberinto.recorrido:
            ultima = self.laberinto.recorrido[-1]
            fila, col = ultima
            if event.keysym == 'Up' and fila > 0:
                nueva = (fila - 1, col)
            elif event.keysym == 'Down' and fila < self.laberinto.filas - 1:
                nueva = (fila + 1, col)
            elif event.keysym == 'Left' and col > 0:
                nueva = (fila, col - 1)
            elif event.keysym == 'Right' and col < self.laberinto.columnas - 1:
                nueva = (fila, col + 1)
            else:
                return
            if nueva in self.laberinto.recorrido:
                indice = self.laberinto.recorrido.index(nueva)
                self.laberinto.recorrido = self.laberinto.recorrido[:indice+1]
            else:
                self.laberinto.recorrido.append(nueva)
            self.actualizar_canvas()
    
    def actualizar_canvas(self):
        self.ax.clear()
        if self.laberinto:
            filas = self.laberinto.filas
            columnas = self.laberinto.columnas
            # Dibujar la cuadrícula
            for fila in range(filas):
                for col in range(columnas):
                    x = col * tam_celda * zoom_factor
                    y = fila * tam_celda * zoom_factor
                    rect = plt.Rectangle((x, y), tam_celda * zoom_factor, tam_celda * zoom_factor, 
                                           facecolor=COLOR_GRID, edgecolor=COLOR_PARED, lw=0.5)
                    self.ax.add_patch(rect)
            # Dibujar entrada y salida
            if self.laberinto.inicio:
                f, c = self.laberinto.inicio
                x = c * tam_celda * zoom_factor + (tam_celda * zoom_factor)/2
                y = f * tam_celda * zoom_factor + (tam_celda * zoom_factor)/2
                self.ax.plot(x, y, 'o', color=COLOR_INICIO, markersize=(tam_celda*zoom_factor)/2)
            if self.laberinto.fin:
                f, c = self.laberinto.fin
                x = c * tam_celda * zoom_factor + (tam_celda * zoom_factor)/2
                y = f * tam_celda * zoom_factor + (tam_celda * zoom_factor)/2
                self.ax.plot(x, y, 'o', color=COLOR_FIN, markersize=(tam_celda*zoom_factor)/2)
            # Dibujar recorrido
            if self.laberinto.recorrido:
                pts_x = [c * tam_celda * zoom_factor + (tam_celda*zoom_factor)/2 for (f, c) in self.laberinto.recorrido]
                pts_y = [f * tam_celda * zoom_factor + (tam_celda*zoom_factor)/2 for (f, c) in self.laberinto.recorrido]
                self.ax.plot(pts_x, pts_y, color=COLOR_SOLUCION, lw=2)
            # Dibujar waypoints
            for (f, c) in self.laberinto.waypoints:
                x = c * tam_celda * zoom_factor + (tam_celda*zoom_factor)/2
                y = f * tam_celda * zoom_factor + (tam_celda*zoom_factor)/2
                self.ax.plot(x, y, 's', color=COLOR_WAYPOINT, markersize=(tam_celda*zoom_factor)/2)
            # Dibujar paredes añadidas
            for celda, lista in self.laberinto.paredes.items():
                f, c = celda
                x = c * tam_celda * zoom_factor
                y = f * tam_celda * zoom_factor
                for p in lista:
                    if p == 'N':
                        self.ax.plot([x, x+tam_celda*zoom_factor], [y, y], color=COLOR_PARED, lw=2)
                    elif p == 'S':
                        self.ax.plot([x, x+tam_celda*zoom_factor], [y+tam_celda*zoom_factor, y+tam_celda*zoom_factor], color=COLOR_PARED, lw=2)
                    elif p == 'E':
                        self.ax.plot([x+tam_celda*zoom_factor, x+tam_celda*zoom_factor], [y, y+tam_celda*zoom_factor], color=COLOR_PARED, lw=2)
                    elif p == 'O':
                        self.ax.plot([x, x], [y, y+tam_celda*zoom_factor], color=COLOR_PARED, lw=2)
        self.ax.set_xlim(0, self.laberinto.columnas * tam_celda * zoom_factor)
        self.ax.set_ylim(self.laberinto.filas * tam_celda * zoom_factor, 0)
        self.ax.axis('off')
        self.canvas.draw()
