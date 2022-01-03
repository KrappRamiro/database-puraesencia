from database_functions import *
from frontend_functions import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import logging
root = tk.Tk()
root.attributes('-type', 'dialog')  # abrir en floating mode
root.title("Base de datos Pura Esencia")
logging.basicConfig(encoding='utf-8',format='%(levelname)s: %(message)s', level=logging.DEBUG)

db_connection = sqlite3.connect("database.sqlite3")
db_cursor = db_connection.cursor()

def exit_program():
	'''Abre un messagebox preguntando si se desea salir de la aplicacion'''	
	valor = messagebox.askquestion("Salir", "¿Deseas salir de la aplicacion?")
	if valor == "yes":
		logging.info("Saliendo de la aplicación")
		root.destroy()

#Creacion del frame del menu principal
mi_frame = tk.Frame(root)
mi_frame.config(width=300, height=400)
mi_frame.pack()

# Boton para agregar clienta
button_agregar_clienta = tk.Button(mi_frame, text="Agregar clienta", command=lambda: client_entry_window())
button_agregar_clienta.grid(row=0, column=0, padx=5, pady=5)

# Boton para agregar producto
button_agregar_producto = tk.Button(mi_frame, text="Agregar Producto", command=lambda: product_entry_window())
button_agregar_producto.grid(row=0, column=1, padx=5, pady=5)

# Boton para agregar categoria
button_agregar_categorias = tk.Button(mi_frame, text="Agregar categorias", command= lambda: category_entry_window())
button_agregar_categorias.grid(row=0, column=2, padx=5, pady=5)

# Boton para agregar una orden de compra
button_agregar_order = tk.Button(mi_frame, text="Agregar order", command= lambda: order_entry_window())
button_agregar_order.grid(row=0, column=3, padx=5, pady=5)

#Boton para agregar medios de pago
button_agregar_medios_pago = tk.Button(mi_frame, text="Agregar medio de pago", command= lambda: medio_de_pago_entry_window())
button_agregar_medios_pago.grid(row=0, column=4, padx=5, pady=5)

# Crea la base de datos si no existe
connect_to_database()
root.mainloop()
