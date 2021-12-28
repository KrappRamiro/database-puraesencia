from database_functions import *
from frontend_functions import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
root = tk.Tk()
root.attributes('-type', 'dialog')  # abrir en floating mode

def exit_program():
	valor = messagebox.askquestion("Salir", "¿Deseas salir de la aplicacion?")
	if valor == "yes":
		root.destroy()

mi_frame = tk.Frame(root)
mi_frame.config(width=300, height=400)
mi_frame.pack()

button_agregar_clienta = tk.Button(mi_frame, text="Agregar clienta", command=lambda: client_entry_window())
button_agregar_clienta.grid(row=0, column=0)

button_agregar_producto = tk.Button(mi_frame, text="Agregar Producto", command=lambda: product_entry_window())
button_agregar_producto.grid(row=0, column=1)

button_agregar_categorias = tk.Button(mi_frame, text="Agregar categorias", command= lambda: category_entry_window())
button_agregar_categorias.grid(row=0, column=2)

button_agregar_order = tk.Button(mi_frame, text="Agregar order", command= lambda: order_entry_window())
button_agregar_order.grid(row=0, column=3)
connect_to_database()
root.mainloop()
