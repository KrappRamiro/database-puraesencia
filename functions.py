import sqlite3
from tkinter import *
from tkinter import messagebox
def connect_to_database():
	try:
		print("Starting connection with database")
		messagebox.showinfo("Informacion", "Conectando a base de datos")
		db_connection = sqlite3.connect("database.sqlite3")
		db_cursor = db_connection.cursor()	
		db_cursor.execute('''
			CREATE TABLE IF NOT EXISTS Customers (
				customer_id 			INTEGER PRIMARY KEY AUTOINCREMENT,
				first_name				TEXT 	NOT NULL,
				last_name				TEXT 	NOT NULL,
				email 					TEXT	UNIQUE,
				gender					TEXT 	DEFAULT '?',
				mercado_pago_id 		TEXT 	UNIQUE,
				mercado_pago_alias		TEXT 	UNIQUE
			)'''
		)
		db_cursor.execute('''
			CREATE TABLE IF NOT EXISTS Orders (
				order_id				INTEGER PRIMARY KEY AUTOINCREMENT,
				orderdate				TEXT 	NOT NULL,
				customer_id				INTEGER	NOT NULL,
				total_amount			FLOAT 	NOT NULL,
				medio_pago				TEXT,
				FOREIGN KEY(customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
			)'''
		)
		db_cursor.execute('''
			CREATE TABLE IF NOT EXISTS Categories (
				category_id				INTEGER	PRIMARY KEY AUTOINCREMENT,
				category_name			TEXT NOT NULL UNIQUE
			)'''
		)
		db_cursor.execute('''
			CREATE TABLE IF NOT EXISTS Products (
				product_id				INTEGER	PRIMARY KEY AUTOINCREMENT,
				category_id				INTEGER,
				title 					TEXT NOT NULL UNIQUE,
				FOREIGN KEY(category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
			)'''
		)
		db_cursor.execute('''
			CREATE TABLE IF NOT EXISTS Orderline (
				orderline_id			INTEGER	PRIMARY KEY AUTOINCREMENT,
				order_id				INTEGER,
				product_id				INTEGER,
				quantity				INTEGER,
				FOREIGN KEY(order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
				FOREIGN KEY(product_id) REFERENCES Products(product_id) ON DELETE CASCADE
			)'''
		)
	except:
		messagebox.showerror("Error","Ha ocurrido un error desconocido conectando a la base de datos")

root = Tk()
root.attributes('-type', 'dialog')  # abrir en floating mode

mi_frame = Frame(root)
mi_frame.config(width=300, height=400)
mi_frame.pack()

connect_to_database()
root.mainloop()