# pylint: disable=bad-indentation
from database_functions import *
import tkinter as tk
from tkinter import messagebox, ttk
import logging
from datetime import date, datetime


def show_info():
	messagebox.showinfo("Interfaz grafica base de datos", "Krapp Ramiro, version 1.0 2021")

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
	def create(category_name):
		logging.info(f"Recieved the following arguments: {category_name}")
		db_cursor.execute(
			'''INSERT INTO Categories
			VALUES(?,?)''',
			(None, category_name)
		)
		db_connection.commit()


	category_name = tk.StringVar()

	Window = tk.Toplevel()
	Window.attributes('-type', 'dialog')
	Window.title("Agregar categor??a")

	# Entrada de categoria
	tk.Label(Window, text="Categoria").grid(row=0, column=0)
	tk.Entry(Window, textvariable=category_name).grid(
		row=0, column=1, pady=10, padx=5)

	tk.Button( Window, text="Cargar datos", command=lambda: create(category_name.get())).grid(row=1, column=0, pady=5, padx=5)

def product_entry_window():
	def create(category_id, product_name):
		logging.info(f"Agregando el producto {product_name} a la categoria con el id {category_id}")
		# Conectar con la base de datos
		# Insertar en la tabla de los productos
		db_cursor.execute(
			'''INSERT INTO Products
			VALUES(?,?,?)''',
			(None, category_id, product_name)
		)
		db_connection.commit()

	# Creacion de la nueva ventana tk.Toplevel
	Window = tk.Toplevel()
	Window.attributes('-type', 'dialog')
	Window.title("Agregar producto")
	# declaracion de variables
	product_name = tk.StringVar()
	options = get_categories()
	options = [' '.join(x) for x in options]
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
		Window, text="Cargar datos", command=lambda: create(
			get_category_id(dropdown.get()),
			product_name.get()
		)
	)
	button_cargar_datos.grid(row=1, column=0, pady=5, padx=5)

def order_entry_window():
	# Esto estaba para printear que clientas habia
	#for i in range(len(lista_clientas)):
	#	print (lista_clientas[i][0] + " " + lista_clientas[i][1])
	
	lista_productos = []
	class Producto():
		def __init__(self, amount, product, price, proffesional,senia):
			self.amount = amount
			self.product = product
			self.price = price
			self.proffesional = proffesional
			self.senia = senia
	
	def actualizar_total():
		total = 0
		for producto in lista_productos:
			total += producto.price * producto.amount
		logging.info(f"el total es {total}")
		total_displayed.set(total)

	def agregar_orderline(amount, product, price, proffesional_id, proffesional_name, senia):
		logging.info(f"Adding {amount} {product}'s with a price of {price} each one, assigned to the proffesional {proffesional_name} with the id {proffesional_id} with a se??a of {senia}")
		lista_productos.append(Producto(amount, product, price, proffesional_id, senia))
		
		# Parte de la textbox
		# 1 - consigo que productos se quiere agregar y que cantidad
		selected_products = str(amount) + " x " + dropdown_products.get() + " c/u $" + str(price) + "--" + proffesional_name

		# 2 - guardo en contenido_anterior lo que habia antes en la textbox, y limpio la misma
		contenido_anterior = textbox_added_products.get(1.0, "end")
		textbox_added_products.delete(1.0, "end")

		# 3 - inserto en la textbox el contendio que habia antes + los productos que quiero agregar
		textbox_added_products.insert(1.0, contenido_anterior + selected_products)
		actualizar_total()
	def create(orderdate, customer_id, total_amount, payment_method_id, productos, proffesional_id):
		# ------------ Logging ------------------------
		logging.info(f'''got the following data:
		orderdate: {orderdate}
		customer id: {customer_id}
		total amount: {total_amount}
		medio de pago ID: {payment_method_id},
		proffesional ID: {proffesional_id}
		''')
		for i in range(len(productos)): 
			logging.info(f'''Producto numero {i+1}:
				nombre del producto: {productos[i].product}
				cantidad del producto: {productos[i].amount}
				precio del producto: {productos[i].price}
				profesional asignado: {productos[i].proffesional}
				se??a: {productos[i].senia}'''
			)
		# ------------ ------- ------------------------
		
		db_cursor.execute(
			'''INSERT INTO Orders
			VALUES(?,?,?,?,?)''',
			(None, orderdate, customer_id, total_amount, payment_method_id)
		)
		db_cursor.execute(
			'''SELECT order_id
			FROM Orders
			WHERE orderdate = ? AND customer_id = ? AND total_amount = ? AND payment_method_id = ?''',
			(orderdate, customer_id, total_amount, payment_method_id)
		)
		order_id = db_cursor.fetchone()
		order_id = order_id[0]
		logging.info(f"got the order id with the following value: {order_id}")
		for i in range(len(productos)):
			db_cursor.execute(
				'''INSERT INTO Orderline
				VALUES (?,?,?,?,?,?,?)''',
				(None, order_id, productos[i].product, productos[i].amount, productos[i].price, productos[i].proffesional, productos[i].senia)
			)
		db_connection.commit()


	Window = tk.Toplevel()
	Window.attributes('-type', 'dialog')
	Window.title("Agregar orden de compra")

	categories = get_categories()
	categories = [' '.join(x) for x in categories]
	products = get_products()
	products = [' '.join(x) for x in products]
	medios_de_pago = get_medios_de_pago()
	medios_de_pago = [' '.join(x) for x in medios_de_pago]
	lista_clientas=get_customers()
	lista_clientas = [' '.join(x) for x in lista_clientas]
	proffesionales = get_proffesionales()
	proffesionales = [' '.join(x) for x in proffesionales]
	amount = tk.IntVar()
	price = tk.IntVar()
	total_displayed = tk.IntVar()
	senia=tk.IntVar()

	#logging.debug(f"productos: {products}")

	# Entrada de cantidad
	tk.Label(Window, text="Cantidad").grid(row=0, column=0, padx=5, pady=5)
	tk.Spinbox(Window, from_=0, to=99, textvariable=amount).grid(
		row=1, column=0, pady=10, padx=5)

	# Dropdown menu para las categorias
	tk.Label(Window, text="Categoria").grid(row=0, column=1, padx=5, pady=5)
	dropdown_categories = ttk.Combobox(Window, values=categories)
	dropdown_categories.set("Elige una opcion... [WIP]")
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

	# Seleccion de proffesional
	tk.Label(Window, text="Profesional").grid(row=0, column=6, padx=5, pady=5)
	dropdown_proffesional= ttk.Combobox(Window, values=proffesionales)
	dropdown_proffesional.set("Elige una proffesional...")
	dropdown_proffesional.grid(row=1, column=6)

	# Textbox de los productos seleccionados
	textbox_added_products = tk.Text(Window, height=5, width=40)
	textbox_added_products.grid(row=2, column=0,columnspan=2)

	# Precio total
	tk.Label(Window, text="Total: $").grid(row=2, column=2)
	tk.Entry(Window, textvariable=total_displayed).grid(row=2, column=3)

	# Logo de pura esencia
	img = tk.PhotoImage(file='./images/logo_largo.png')
	label =tk.Label(
		Window,
		image=img
	)
	label.image=img
	label.grid(row=2, column=4, columnspan=3)

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

	# Se??a
	tk.Label(Window, text="Se??a").grid(row=0, column=7)
	tk.Entry(Window, textvariable=senia).grid(row=1, column=7)

	# Button de Add
	boton = tk.Button(Window, text="Add", command=lambda: agregar_orderline(amount.get(), dropdown_products.current(), price.get(), dropdown_proffesional.current(), dropdown_proffesional.get(), senia.get()))
	boton.grid(row=3, column=0)

	# Button de Finish
	tk.Button(Window, text="Finalizar", command=lambda: 
		create(
			datetime.today().strftime('%Y-%m-%d'),
			dropdown_clients.current(),
			total_displayed.get(),
			dropdown_medios_pago.current(),
			lista_productos,
			dropdown_proffesional.current()
		)
	).grid(row=3, column=1)

def payment_method_entry_window():
	def create(medio_de_pago):
		db_cursor.execute(
			'''INSERT INTO Payment_methods
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
	tk.Button(Window, text="A??adir", command= lambda: create(medio_de_pago.get())).grid(row=2, column=0)

def proffesional_entry_window():
	def create(nombre, apellido, especializacion):
		db_cursor.execute(
			'''INSERT INTO Proffesional
			VALUES(?,?,?,?)''',
			(None, nombre, apellido, especializacion)
		)
		db_connection.commit()
		logging.info(f'''Adding proffesional with values:
		Name: {nombre}
		Surname: {apellido}
		Especializacion: {especializacion} ''')

	Window = tk.Toplevel()
	Window.attributes('-type', 'dialog')
	Window.title("Agregar profesional")

	nombre = tk.StringVar()
	apellido = tk.StringVar()
	especializacion = tk.StringVar()

	# Entrada de nombre
	tk.Label(Window, text="Nombre").grid(row=0, column=0, pady=5, padx=5)
	tk.Entry(Window, textvariable=nombre).grid(row=0, column=1, padx=5, pady=5)

	# Entrada de Apellido
	tk.Label(Window, text="Apellido").grid(row=1, column=0, pady=5, padx=5)
	tk.Entry(Window, textvariable=apellido).grid(row=1, column=1, padx=5, pady=5)
	
	# Entrada de Especializacion
	tk.Label(Window, text="Especializacion").grid(row=2, column=0, pady=5, padx=5)
	tk.Entry(Window, textvariable=especializacion).grid(row=2, column=1, padx=5, pady=5)

	# Boton para a??adir
	tk.Button(Window, text="A??adir", command= lambda: create(nombre.get(), apellido.get(), especializacion.get())).grid(row=3, column=0)

def view_general_data_window():
	Window = tk.Toplevel()
	Window.attributes('-type', 'dialog')
	Window.title("ver info")
	db_cursor.execute(
		# TODO todo el select de aca, es lo primero que tenes que hacer
		''' SELECT Orders.order_id, Orders.orderdate, Orders.customer_id, Orderline.product_id, Orderline.senia,
					Orders.payment_method_id, Orderline.price, Orderline.proffesional_id
		FROM Orders
		JOIN Orderline
		ON Orders.order_id = Orderline.order_id
		'''
	)
	datalist = db_cursor.fetchall()
	for x in datalist:
		print(x)
	datalist = [list(ele) for ele in datalist]
	for data in datalist:
		data[2] = get_customer_fullname_by_id(data[2]+1)
		data[3] = get_product_name_by_id(data[3]+1)
		data[5] = get_payment_method_name_by_id(data[5]+1)
		data[7] = get_proffesional_fullname_by_id(data[7]+1)

	for x in datalist:
		print(x)
	tk.Label(Window, text="Numero de Orden").grid(row=0, column=0, padx=5, pady=5)
	tk.Label(Window, text="Fecha").grid(row=0, column=1, padx=5, pady=5)
	tk.Label(Window, text="Clienta").grid(row=0, column=2, padx=5, pady=5)
	tk.Label(Window, text="Tratamiento").grid(row=0, column=3, padx=5, pady=5)
	tk.Label(Window, text="Se??a").grid(row=0, column=4, padx=5, pady=5)
	tk.Label(Window, text="Medio de pago").grid(row=0, column=5, padx=5, pady=5)
	tk.Label(Window, text="Precio").grid(row=0, column=6, padx=5, pady=5)
	tk.Label(Window, text="Profesional").grid(row=0, column=7, padx=5, pady=5)

	widgets = {}
	row = 1
	for order_id, date, client, treatment, senia, payment_method, price, proffesional in (datalist):
	#Order-id Fecha Clienta Tratamiento Se??a Medio de Pago Precio Profesional
		row += 1
		widgets[order_id] = {
			# tendria que googlear como funciona : en   "xxxx" : tk.Label
			"order_id": tk.Label(Window, text=order_id),
			"date": tk.Label(Window, text=date),
			"client": tk.Label(Window, text=client),
			"treatment": tk.Label(Window, text=treatment),
			"senia": tk.Label(Window, text=senia),
			"payment_method": tk.Label(Window, text=payment_method),
			"price": tk.Label(Window, text=price),
			"proffesional": tk.Label(Window, text=proffesional)
		}

		widgets[order_id]["order_id"].grid(row=row, column=0, sticky="nsew", padx=5, pady=5)
		widgets[order_id]["date"].grid(row=row, column=1, sticky="nsew", padx=5, pady=5)
		widgets[order_id]["client"].grid(row=row, column=2, sticky="nsew", padx=5, pady=5)
		widgets[order_id]["treatment"].grid(row=row, column=3, sticky="nsew", padx=5, pady=5)
		widgets[order_id]["senia"].grid(row=row, column=4, sticky="nsew", padx=5, pady=5)
		widgets[order_id]["payment_method"].grid(row=row, column=5, sticky="nsew", padx=5, pady=5)
		widgets[order_id]["price"].grid(row=row, column=6, sticky="nsew", padx=5, pady=5)
		widgets[order_id]["proffesional"].grid(row=row, column=7, sticky="nsew", padx=5, pady=5)

		Window.grid_columnconfigure(1, weight=1)
		Window.grid_columnconfigure(2, weight=1)
		# invisible row after last row gets all extra space
		Window.grid_rowconfigure(row+1, weight=1)

