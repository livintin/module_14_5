# -*- coding: utf-8 -*-
import sqlite3

connection = sqlite3.connect("initiate_db.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
);
''')

cursor.execute('''INSERT INTO Products (title, description, price) VALUES (
    "Липосомальный витамин D",
    "Улучшенная формула всем известного витамина D, которая максимально эффективно усваивается организмом.",
    1691
);''')

cursor.execute('''INSERT INTO Products (title, description, price) VALUES (
    "Липосомальный витамин C",
    "Улучшенная формула всем известного витамина C, которая максимально эффективно усваивается организмом.",
    1776
);''')

cursor.execute('''INSERT INTO Products (title, description, price) VALUES (
    "Липосомальный глутатион",
    "Глутатион – помощник в поддержании молодости, красоты и здоровья организма.",
    2176
);''')

cursor.execute('''INSERT INTO Products (title, description, price) VALUES (
    "Липосомальный B-комплекс",
    "Биоактивная липосомальная формула для восстановления работы нервной системы и активности мозга.",
    2691
);''')

connection.commit()
connection.close()


def get_all_products():
    connection = sqlite3.connect('initiate_db.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    res = cursor.fetchall()
    connection.close()
    return res


connection = sqlite3.connect("initiate_db.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER NOT NULL,
balance INTEGER NOT NULL
);
''')

def add_user(username, email, age):
    connection = sqlite3.connect("initiate_db.db")
    cursor = connection.cursor()
    cursor.execute(f'''
        INSERT INTO Users (username, email, age, balance) VALUES ('{username}', '{email}', '{age}', 1000)    
        ''')
    connection.commit()

def is_included(username):
    connection = sqlite3.connect("initiate_db.db")
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()
    connection.commit()
    if user is None:
        return False
    else:
        return True
