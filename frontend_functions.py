from database_functions import *
import tkinter as tk
from tkinter import messagebox, ttk
import logging


def show_info():
	messagebox.showinfo("Interfaz grafica base de datos",
						"Krapp Ramiro, version 1.0 2021")

def show_license():
	messagebox.showwarning("Licencia", "Producto bajo licencia GNU GPL v2.0")

def client_entry_window():
	''' Esta funcion crea una ventana para que se ingrese informacion sobre los clientes,
	se piden: - Nombre - Apellido - email - genero'''
	def create(firstname, lastname, email, gender):
		''' Esta funcion ingresa nombre, apellido, email y genero dentro de la base de datos,
		recibe como parametros los mismos'''
		# Conexion con base de datos
		# Validacion de email
		if email_validation(email) is not True:
			return
		# Asignacion de genero
		if gender == 1: gender = 'M'
		elif gender == 2: gender = 'F'
		else:
			logging.error("El genero introducido es invalido")
			return
		# Log de datos introducidos
		logging.info(
			f'''Client creation --- Recieved the following arguments:
			Name: {firstname}
			Surname: {lastname}
			Email: {email}
			Gender: {gender}'''
		)
		# Introduccion de datos en la base de datos
		db_cursor.execute(
			'''INSERT INTO Customers
			VALUES(?,?,?,?,?,?,?)''',
			(None, firstname, lastname, email, gender, None, None)
		)
		logging.info("Succesfully created client")
		db_connection.commit()

	user_id = tk.IntVar()
	user_firstname = tk.StringVar()
	user_lastname = tk.StringVar()
	user_email = tk.StringVar()
	user_gender = tk.IntVar()

	Window = tk.Toplevel()
	Window.attributes('-type', 'dialog')
	Window.title("Agregar clienta")

	# ID
	tk.Label(Window, text="user_id").grid(row=0, column=0)
	tk.Entry(Window, textvariable=user_id).grid(
		row=0, column=1, pady=10, padx=5)

	# Nombre
	tk.Label(Window, text="Nombre").grid(row=1, column=0)
	tk.Entry(Window, textvariable=user_firstname).grid(
		row=1, column=1, pady=10, padx=5)

	# Apellido
	tk.Label(Window, text="Apellido").grid(row=2, column=0)
	tk.Entry(Window, textvariable=user_lastname).grid(
		row=2, column=1, pady=10, padx=5)

	# email
	tk.Label(Window, text="email").grid(row=3, column=0)
	tk.Entry(Window, textvariable=user_email).grid(
		row=3, column=1, pady=10, padx=5)

	# genders
	tk.Label(Window, text="gender: ").grid(
		row=4, column=0, pady=10, padx=5)
	tk.Radiobutton(Window, text="Masculino", variable=user_gender, value=1).grid(
		row=4, column=1, pady=5, padx=5)
	tk.Radiobutton(Window, text="Femenino", variable=user_gender, value=2).grid(
		row=5, column=1, pady=5, padx=5)

	tk.Button(
		Window, text="Cargar datos", command=lambda: create(user_firstname.get(), user_lastname.get(), user_email.get(), user_gender.get())) .grid(row=6, column=0, pady=5, padx=5)

def category_entry_window():
	def create():
		logging.info("Recieved the following arguments:", category_name.get())
		db_cursor.execute(
			'''INSERT INTO Categories
			VALUES(?,?)''',
			(None, category_name.get())
		)
		db_connection.commit()

	category_name = tk.StringVar()

	Window = tk.Toplevel()
	Window.attributes('-type', 'dialog')
	Window.title("Agregar categoría")

	# Entrada de categoria
	tk.Label(Window, text="Categoria").grid(row=0, column=0)
	tk.Entry(Window, textvariable=category_name).grid(
		row=0, column=1, pady=10, padx=5)

	tk.Button( Window, text="Cargar datos", command=lambda: create()).grid(row=1, column=0, pady=5, padx=5)

def product_entry_window():
	def create():
		category_id = get_category_id(dropdown.get())

		# Conectar con la base de datos
		# Insertar en la tabla de los productos
		db_cursor.execute(
			'''INSERT INTO Products
			VALUES(?,?,?)''',
			(None, category_id, product_name.get())
		)
		db_connection.commit()
	# Creacion de la nueva ventana tk.Toplevel
	Window = tk.Toplevel()
	Window.attributes('-type', 'dialog')
	Window.title("Agregar producto")
	# declaracion de variables
	product_name = tk.StringVar()
	options = get_categories()
	# Entrada de producto
	tk.Label(Window, text="Producto:").grid(row=0, column=0)
	tk.Entry(Window, textvariable=product_name).grid(
		row=0, column=1, pady=10, padx=5)

	# Dropdown menu para las categorias
	dropdown = ttk.Combobox(Window, values=options)
	dropdown.set("Elige una opcion...")
	dropdown.grid(row=0, column=2)

	# Boton para la carga de datos
	button_cargar_datos = tk.Button(
		Window, text="Cargar datos", command=lambda: create())
	button_cargar_datos.grid(row=1, column=0, pady=5, padx=5)

def order_entry_window():
	# TODO falta el agregado a la base de datos
	lista_clientas=get_clients()
	# Esto estaba para printear que clientas habia
	#for i in range(len(lista_clientas)):
	#	print (lista_clientas[i][0] + " " + lista_clientas[i][1])
	
	lista_productos = []
	class Producto():
		def __init__(self, amount, product, price):
			self.amount = amount
			self.product = product
			self.price = price
	
	def actualizar_total():
		total = 0
		for producto in lista_productos:
			total += producto.price * producto.amount
		logging.info(f"el total es {total}")
		total_displayed.set(total)

	def agregar_producto(amount, product, price):
		logging.info(f"Adding {amount} {product}'s with a price of {price} each one")
		lista_productos.append(Producto(amount, product, price))
		
		# Parte de la textbox
		# 1 - consigo que productos se quiere agregar y que cantidad
		selected_products = str(amount) + " x " + dropdown_products.get() + " c/u $" + str(price)

		# 2 - guardo en contenido_anterior lo que habia antes en la textbox, y limpio la misma
		contenido_anterior = textbox_added_products.get(1.0, "end")
		textbox_added_products.delete(1.0, "end")

		# 3 - inserto en la textbox el contendio que habia antes + los productos que quiero agregar
		textbox_added_products.insert(1.0, contenido_anterior + selected_products)
		actualizar_total()

	Window = tk.Toplevel()
	Window.attributes('-type', 'dialog')
	Window.title("Agregar orden de compra")

	amount = tk.IntVar()
	categories = get_categories()
	products = get_products()
	price = tk.IntVar()
	total_displayed = tk.IntVar()
	medios_de_pago = get_medios_de_pago()

	# Entrada de cantidad
	tk.Label(Window, text="Cantidad").grid(row=0, column=0, padx=5, pady=5)
	tk.Entry(Window, textvariable=amount).grid(
		row=1, column=0, pady=10, padx=5)

	# Dropdown menu para las categorias
	tk.Label(Window, text="Categoria").grid(row=0, column=1, padx=5, pady=5)
	dropdown_categories = ttk.Combobox(Window, values=categories)
	dropdown_categories.set("Elige una opcion...")
	dropdown_categories.grid(row=1, column=1)

	# Dropdown para los productos
	# TODO: Deberia hacer que despues de seleccionar la categoria, se active
	# un evento en el cual actualice el valor de products, lo cual
	# actualice lo que hay en el dropdown menu.
	##  Por lo tanto, no tiene utilidad por el momento :(
	tk.Label(Window, text="Producto").grid(row=0, column=2, padx=5, pady=5)
	dropdown_products = ttk.Combobox(Window, values=products)
	dropdown_products.set("Elige una opcion...")
	dropdown_products.grid(row=1, column=2)

	# Entrada de costo de producto
	tk.Label(Window, text="Precio").grid(row=0, column=3, padx=5, pady=5)
	tk.Entry(Window, textvariable=price).grid( row=1, column=3, pady=10, padx=5)

	# Textbox de los productos seleccionados
	textbox_added_products = tk.Text(Window, height=5, width=40)
	textbox_added_products.grid(row=2, column=0,columnspan=2)

	# Precio total
	tk.Label(Window, text="Total: $").grid(row=2, column=2)
	tk.Entry(Window, textvariable=total_displayed).grid(row=2, column=3)

	# Lista de clientas
	tk.Label(Window, text="Clienta").grid(row=0, column=4)
	dropdown_clients = ttk.Combobox(Window, values=lista_clientas)
	dropdown_clients.set("Elige una clienta...")
	dropdown_clients.grid(row=1, column=4)

	# Medio de pago
	tk.Label(Window, text="Medio de pago").grid(row=0, column=5)
	dropdown_medios_pago = ttk.Combobox(Window, values=medios_de_pago)
	dropdown_medios_pago.set("Elige un medio de pago...")
	dropdown_medios_pago.grid(row=1, column=5)

	# Button de Add
	boton = tk.Button(Window, text="Add", command=lambda: agregar_producto(amount.get(), dropdown_products.get(), price.get()))
	boton.grid(row=3, column=0)

def medio_de_pago_entry_window():
	def create(medio_de_pago):

		# Conectar con la base de datos
		# Insertar en la tabla de los productos
		db_cursor.execute(
			'''INSERT INTO Medios_pago
			VALUES(?,?)''',
			(None, medio_de_pago)
		)
		db_connection.commit()
		logging.info(f"Adding medio de pago with name {medio_de_pago}")

	Window = tk.Toplevel()
	Window.attributes('-type', 'dialog')
	Window.title("Agregar medio de pago")

	medio_de_pago = tk.StringVar()

	tk.Label(Window, text="Ingrese el medio de pago").grid(row=0, column=0, pady=5, padx=5)
	tk.Entry(Window, textvariable=medio_de_pago).grid(row=1, column=0, padx=5, pady=5)
	tk.Button(Window, text="Añadir", command= lambda: create(medio_de_pago.get())).grid(row=2, column=0)