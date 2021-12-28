from database_functions import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import functools
root = Tk()
root.attributes('-type', 'dialog')  # abrir en floating mode
#Conseguir todas las categorias y retornarlas como una lista
def get_categories():
	db_connection= sqlite3.connect("database.sqlite3")
	db_cursor = db_connection.cursor()
	db_cursor.execute("SELECT category_name FROM Categories")
	return db_cursor.fetchall()

def get_products():
	db_connection= sqlite3.connect("database.sqlite3")
	db_cursor = db_connection.cursor()
	db_cursor.execute("SELECT product_name FROM Products")
	return db_cursor.fetchall()

def get_products_by_categorie(category_id):
	db_connection= sqlite3.connect("database.sqlite3")
	db_cursor = db_connection.cursor()
	db_cursor.execute("SELECT product_name FROM Products WHERE category_id = ?",(category_id,))
	return db_cursor.fetchall()

def get_category_id(category_wanted):
	db_connection= sqlite3.connect("database.sqlite3")
	db_cursor = db_connection.cursor()
	#Conseguir la categoria seleccionada
	print(category_wanted.get())
	category_searched=category_wanted.get().strip('(),\'')
	print("searching for the category",category_searched)

	#Conseguir el ID de la categoria seleccionada
	db_cursor.execute("SELECT category_id FROM Categories WHERE category_name = ?", (category_searched,))
	category_id=db_cursor.fetchone()
	category_id = functools.reduce(lambda sub, elem: sub * 10 + elem, category_id)
	print("found the category id: ", category_id)
	return category_id

def show_info():
	messagebox.showinfo("Interfaz grafica base de datos", "Krapp Ramiro, version 1.0 2021")

def show_license():
	messagebox.showwarning("Licencia", "Producto bajo licencia GNU GPL v2.0")

def exit_program():
	valor = messagebox.askquestion("Salir", "¿Deseas salir de la aplicacion?")
	if valor == "yes":
		root.destroy()

def email_validation(x):
	a=0
	y=len(x)
	dot=x.find(".")
	at=x.find("@")
	for i in range (0,at):
		if((x[i]>='a' and x[i]<='z') or (x[i]>='A' and x[i]<='Z')):
			a=a+1
	if(a>0 and at>0 and (dot-at)>0 and (dot+1)<y):
		print("Valid Email")
		return True
	else:
		print("Invalid Email")
		return False

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
		category_id=get_category_id(dropdown)

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
	products=get_products_by_categorie()

	# Entrada de cantidad
	Label(Window, text="Cantidad:").grid(row=0, column=0)
	Entry(Window, textvariable=amount).grid(
		row=0, column=1, pady=10, padx=5)

	# Dropdown menu para las categorias
	dropdown_categories = ttk.Combobox(Window , values=categories)
	dropdown_categories.set("Elige una opcion...")
	dropdown_categories.grid(row=0, column=2)

	dropdown_products = ttk.Combobox(Window , values=products)
	dropdown_products.set("Elige una opcion...")
	dropdown_products.grid(row=0, column=3)

mi_frame = Frame(root)
mi_frame.config(width=300, height=400)
mi_frame.pack()

button_agregar_clienta = Button(mi_frame, text="Agregar clienta", command=lambda: client_entry_window())
button_agregar_clienta.grid(row=0, column=0)

button_agregar_producto = Button(mi_frame, text="Agregar Producto", command=lambda: product_entry_window())
button_agregar_producto.grid(row=0, column=1)

button_agregar_categorias = Button(mi_frame, text="Agregar categorias", command= lambda: category_entry_window())
button_agregar_categorias.grid(row=0, column=2)

button_agregar_order = Button(mi_frame, text="Agregar order", command= lambda: order_entry_window())
button_agregar_order.grid(row=0, column=3)
connect_to_database()
root.mainloop()
