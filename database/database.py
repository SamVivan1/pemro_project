import sqlite3

def createDatabase():
    connect = sqlite3.connect('database.db')
    connect.close()

def createTables():
    connect = sqlite3.connect('database.db')
    
    sql = """CREATE TABLE plants (
        id_tree INTEGER PRIMARY KEY,
        sensor INTEGER,
        value REAL
        
    )"""
    connect.execute(sql)
    connect.close()