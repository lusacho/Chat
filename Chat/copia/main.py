# main.py
import tkinter as tk
from interfaz import InterfazLaberinto

def main():
    root = tk.Tk()
    app = InterfazLaberinto(root)
    root.mainloop()

if __name__ == "__main__":
    main()
