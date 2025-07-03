import mysql.connector
from mysql.connector import Error
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# Hàm kết nối cơ sở dữ liệu
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Npv2707@",
            database="cua_hang"
        )
        return connection
    except Error as e:
        messagebox.showerror("Lỗi kết nối", f"Lỗi kết nối đến MySQL: {e}")
        return None