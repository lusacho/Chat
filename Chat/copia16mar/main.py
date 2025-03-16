# main.py
from interfaz import InterfazLaberinto
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Proyecto Laberinto")
    app = InterfazLaberinto(root)
    root.mainloop()
