from database_functions import *
from tkinter import *
from tkinter import messagebox
root = Tk()
root.attributes('-type', 'dialog')  # abrir en floating mode

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

	# ID
	Label(Window, text="Category name").grid(row=0, column=0)
	Entry(Window, textvariable=category_name).grid(
		row=0, column=1, pady=10, padx=5)

	button_cargar_datos = Button(Window, text="Cargar datos", command=lambda: create())
	button_cargar_datos.grid(row=6, column=0, pady=5, padx=5)

mi_frame = Frame(root)
mi_frame.config(width=300, height=400)
mi_frame.pack()

button_agregar_clienta = Button(mi_frame, text="Agregar clienta", command=lambda: client_entry_window())
button_agregar_clienta.grid(row=0, column=0)

button_agregar_producto = Button(mi_frame, text="Agregar Producto", command=lambda: category_entry_window())
button_agregar_producto.grid(row=0, column=1)

button_agregar_categorias = Button(mi_frame, text="Agregar categorias")
button_agregar_categorias.grid(row=0, column=2)

button_agregar_order = Button(mi_frame, text="Agregar order")
button_agregar_order.grid(row=0, column=3)
connect_to_database()
root.mainloop()
