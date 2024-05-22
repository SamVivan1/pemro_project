import sqlite3

def createDatabase():
    connect = sqlite3.connect('database.db')
    connect.close()

def createTables():
    connect = sqlite3.connect('database.db')
    
    sql = """CREATE TABLE plants (
        id_tree INTEGER PRIMARY KEY,
        sensor_1 INTEGER,
        sensor_2 INTEGER,
        sensor_3 INTEGER,
        sensor_4 INTEGER,
        sensor_5 INTEGER,
        sensor_6 INTEGER,
        sensor_7 INTEGER,
        sensor_8 INTEGER,
        sensor_9 INTEGER,
        sensor_10 INTEGER
    )"""
    connect.execute(sql)
    connect.close()