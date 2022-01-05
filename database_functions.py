import logging
import sqlite3
from tkinter import messagebox

db_connection = sqlite3.connect("database.sqlite3")
db_cursor = db_connection.cursor()

def connect_to_database():
	try:
		logging.info("Starting connection with database")
		#messagebox.showinfo("Informacion", "Conectando a base de datos")
		db_cursor.execute(
			''' CREATE TABLE IF NOT EXISTS Customers (
				customer_id 			INTEGER PRIMARY KEY AUTOINCREMENT,
				first_name				TEXT 	NOT NULL,
				last_name				TEXT 	NOT NULL,
				email 					TEXT	UNIQUE,
				gender					TEXT 	DEFAULT 'x',
				mercado_pago_id 		TEXT 	UNIQUE,
				mercado_pago_alias		TEXT 	UNIQUE
			)'''
		)
		db_cursor.execute(
			''' CREATE TABLE IF NOT EXISTS Payment_methods (
				payment_method_id			INTEGER PRIMARY KEY AUTOINCREMENT,
				payment_method_name			TEXT NOT NULL UNIQUE
			)'''
		)
		db_cursor.execute(
			''' CREATE TABLE IF NOT EXISTS Proffesional (
				proffesional_id	hthttps://github.com/othneildrew/Best-README-Templatetps://github.com/othneildrew/Best-README-Template		INTEGER PRIMARY KEY AUTOINCREMENT,
				first_name				TEXT NOT NULL,
				last_name				TEXT NOT NULL,
				especialization			TEXT
			)'''
		)
		db_cursor.execute(
			''' CREATE TABLE IF NOT EXISTS Orders (
				order_id				INTEGER PRIMARY KEY AUTOINCREMENT,
				orderdate				TEXT 	NOT NULL,
				customer_id				INTEGER	NOT NULL,
				total_amount			FLOAT 	NOT NULL,
				payment_method_id		INTEGER NOT NULL,
				proffesional_id			INTEGER NOT NULL,
				FOREIGN KEY(proffesional_id)	REFERENCES Proffesional(proffesional_id)	  ON DELETE CASCADE
				FOREIGN KEY(customer_id) 		REFERENCES Customers(customer_id)			  ON DELETE CASCADE,
				FOREIGN KEY(payment_method_id) 	REFERENCES Payment_methods(payment_method_id) ON DELETE CASCADE
			)'''
		)
		db_cursor.execute(
			'''
			CREATE TABLE IF NOT EXISTS Categories (
				category_id				INTEGER	PRIMARY KEY AUTOINCREMENT,
				category_name			TEXT NOT NULL UNIQUE
			)'''
		)
		db_cursor.execute(
			''' CREATE TABLE IF NOT EXISTS Products (
				product_id				INTEGER	PRIMARY KEY AUTOINCREMENT,
				category_id				INTEGER NOT NULL,
				product_name			TEXT NOT NULL UNIQUE,
				FOREIGN KEY(category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
			)'''
		)
		db_cursor.execute(
			''' CREATE TABLE IF NOT EXISTS Orderline (
				orderline_id			INTEGER	PRIMARY KEY AUTOINCREMENT,
				order_id				INTEGER NOT NULL,
				product_id				INTEGER NOT NULL,
				quantity				INTEGER NOT NULL,
				price					FLOAT 	NOT NULL,
				FOREIGN KEY(order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
				FOREIGN KEY(product_id) REFERENCES Products(product_id) ON DELETE CASCADE
			)'''
		)

	except:
		messagebox.showerror(
			"Error", "Ha ocurrido un error desconocido conectando a la base de datos")

def get_categories():
	'''Retorna una lista con el nombre de cada categoria'''

	db_cursor.execute("SELECT category_name FROM Categories")
	return db_cursor.fetchall()

def get_products():
	'''Retorna una lista con el nombre de cada producto'''

	db_cursor.execute("SELECT product_name FROM Products")
	return db_cursor.fetchall()

def get_product_id_by_name(product):

	db_cursor.execute("SELECT product_id FROM Products WHERE product_name = ?", (product,)
	)
	return db_cursor.fetchall()

def get_products_by_categorie(category_id):
	'''Retorna una lista con el nombre de cada producto cuya category_id sea igual a la pasada por parametro'''

	db_cursor.execute(
		"SELECT product_name FROM Products WHERE category_id = ?", (category_id,))
	return db_cursor.fetchall()

def get_clients():
	'''Retorna una lista con el nombre de todos los clientes'''

	db_cursor.execute("SELECT first_name, last_name FROM Customers")
	return db_cursor.fetchall()

def get_medios_de_pago():
	'''Retorna una lista con el nombre de todos los medios de pago'''

	db_cursor.execute("SELECT payment_method_name FROM Payment_methods")
	return db_cursor.fetchall()

def get_medio_de_pago_id_by_name(payment_method):

	db_cursor.execute(
		"SELECT payment_method_id FROM Medio_pago WHERE payment_method_name = ?", (payment_method,)
	)
	return db_cursor.fetchall()

def get_category_id(category_wanted):
	'''retorna el id de la categoria pasada por parametro'''

	logging.info(f"Searching for the id of the category {category_wanted}")
	# Conseguir el ID de la categoria seleccionada
	db_cursor.execute(
		"SELECT category_id FROM Categories WHERE category_name = ?", (category_wanted,))
	category_id = db_cursor.fetchone()
	category_id = category_id[0]
	#Checkeo si se encontro la categoria
	if category_id != []:
		logging.info(f"ID of category {category_wanted} is: {category_id}")
		return category_id
	else:
		logging.warning("Category not found")
		return None

def get_customer_id_by_name(firstname, lastname):

	logging.info(f"Looking for {firstname} {lastname}")

	db_cursor.execute(
		"SELECT customer_id FROM Customers WHERE first_name = ? AND last_name = ?",(firstname,lastname)
	)
	customer_id = db_cursor.fetchone()
	customer_id = customer_id[0]
	#Checkeo si se encontro la categoria
	if customer_id != []:
		logging.info(f"ID of customer {firstname} {lastname} is: {customer_id}")
		return customer_id
	else:
		logging.warning("customer not found")
		return None

def get_proffesionales():
	'''Retorna la lista de proffesionales'''
	db_cursor.execute("SELECT first_name, last_name FROM Proffesional")
	return db_cursor.fetchall()


def email_validation(x):
	a = 0
	y = len(x)
	dot = x.find(".")
	at = x.find("@")
	for i in range(0, at):
		if((x[i] >= 'a' and x[i] <= 'z') or (x[i] >= 'A' and x[i] <= 'Z')):
			a = a+1
	if(a > 0 and at > 0 and (dot-at) > 0 and (dot+1) < y):
		logging.info("Valid Email")
		return True
	else:
		logging.warning("Invalid Email")
		return False
