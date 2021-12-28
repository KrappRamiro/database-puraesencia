from database_functions import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

def show_info():
	messagebox.showinfo("Interfaz grafica base de datos", "Krapp Ramiro, version 1.0 2021")

def show_license():
	messagebox.showwarning("Licencia", "Producto bajo licencia GNU GPL v2.0")

def client_entry_window():
	def create():
		db_connection= sqlite3.connect("database.sqlite3")
		db_cursor = db_connection.cursor()
		if email_validation(user_email.get()) is not True:
			return

		print("Value of check button:",user_gender.get())
		if user_gender.get()==1:
			gender='M'
			print("Recieved gender male")
		elif user_gender.get()==2:
			gender='F'
			print("Recieved gender female")
		else:
			print("No recieved gender")

		print(
			"Recieved the following arguments:\nName:", user_firstname.get(), 
			"\nSurname:", user_lastname.get(), 
			"\nEmail:", user_email.get(),
			"\nGender:", gender
		)
		db_cursor.execute('''
			INSERT INTO Customers
			VALUES(?,?,?,?,?,?,?)''',(None,user_firstname.get(),user_lastname.get(),user_email.get(), gender,None, None)
		)
		db_connection.commit()


	user_id=IntVar()
	user_firstname=StringVar()
	user_lastname=StringVar()
	user_email=StringVar()
	user_gender=IntVar()

	Window = Toplevel()
	Window.attributes('-type', 'dialog')

	# ID
	Label(Window, text="user_id").grid(row=0, column=0)
	Entry(Window, textvariable=user_id).grid(
		row=0, column=1, pady=10, padx=5)

	# Nombre
	Label(Window, text="Nombre").grid(row=1, column=0)
	Entry(Window, textvariable=user_firstname).grid(
		row=1, column=1, pady=10, padx=5)

	# Apellido
	Label(Window, text="Apellido").grid(row=2, column=0)
	Entry(Window, textvariable=user_lastname).grid(
		row=2, column=1, pady=10, padx=5)

	# email
	Label(Window, text="email").grid(row=3, column=0)
	Entry(Window, textvariable=user_email).grid(
		row=3, column=1, pady=10, padx=5)
	
	# genders
	Label(Window, text="gender: ").grid(
		row=4, column=0, pady=10, padx=5)
	Radiobutton(Window, text="Masculino", variable=user_gender, value=1).grid(
		row=4, column=1, pady=5, padx=5)
	Radiobutton(Window, text="Femenino", variable=user_gender, value=2).grid(
		row=5, column=1, pady=5, padx=5)

	button_cargar_datos = Button(Window, text="Cargar datos", command=lambda: create())
	button_cargar_datos.grid(row=6, column=0, pady=5, padx=5)

def category_entry_window():
	def create():
		db_connection= sqlite3.connect("database.sqlite3")
		db_cursor = db_connection.cursor()

		print( "Recieved the following arguments:", category_name.get())
		db_cursor.execute('''
			INSERT INTO Categories
			VALUES(?,?)''',(None,category_name.get())
		)
		db_connection.commit()

	category_name= StringVar()

	Window = Toplevel()
	Window.attributes('-type', 'dialog')

	# Entrada de categoria
	Label(Window, text="Categoria").grid(row=0, column=0)
	Entry(Window, textvariable=category_name).grid(
		row=0, column=1, pady=10, padx=5)

	button_cargar_datos = Button(Window, text="Cargar datos", command=lambda: create())
	button_cargar_datos.grid(row=1, column=0, pady=5, padx=5)

def product_entry_window():
	def create():
		category_id=get_category_id(dropdown.get())

		#Conectar con la base de datos
		db_connection= sqlite3.connect("database.sqlite3")
		db_cursor = db_connection.cursor()
		#Insertar en la tabla de los productos
		db_cursor.execute('''
			INSERT INTO Products
			VALUES(?,?,?)''',(None,category_id, product_name.get())
		)
		db_connection.commit()
	
	#declaracion de variables
	product_name = StringVar()
	# Cargar en una lista options todas las categorias
	options=get_categories()

	#Creacion de la nueva ventana toplevel
	Window = Toplevel()
	Window.attributes('-type', 'dialog')

	# Entrada de producto
	Label(Window, text="Producto:").grid(row=0, column=0)
	Entry(Window, textvariable=product_name).grid(
		row=0, column=1, pady=10, padx=5)

	# Dropdown menu para las categorias
	dropdown = ttk.Combobox(Window , values=options)
	dropdown.set("Elige una opcion...")
	dropdown.grid(row=0, column=2)

	# Boton para la carga de datos
	button_cargar_datos = Button(Window, text="Cargar datos", command=lambda: create())
	button_cargar_datos.grid(row=1, column=0, pady=5, padx=5)

def order_entry_window():
	Window = Toplevel()
	Window.attributes('-type', 'dialog')

	amount = IntVar()
	categories=get_categories()
	products=get_products()

	# Entrada de cantidad
	Label(Window, text="Cantidad:").grid(row=0, column=0)
	Entry(Window, textvariable=amount).grid(
		row=0, column=1, pady=10, padx=5)

	# Dropdown menu para las categorias
	dropdown_categories = ttk.Combobox(Window , values=categories)
	dropdown_categories.set("Elige una opcion...")
	dropdown_categories.grid(row=0, column=2)

	# Dropdown para los productos
	# TODO: Deberia hacer que despues de seleccionar la categoria, se active
	# un evento en el cual actualice el valor de products, lo cual
	# actualice lo que hay en el dropdown menu.
	dropdown_products = ttk.Combobox(Window , values=products)
	dropdown_products.set("Elige una opcion...")
	dropdown_products.grid(row=0, column=3)

	# Textbox de los productos seleccionados
	added_products=Text(Window, height=5, width=30).grid(row=1,column=0)
	added_products.delete(1.0,"end")
	added_products.insert(5.0, "holaaaaa")
