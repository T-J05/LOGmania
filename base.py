import sqlite3

def crear_bd ():
    conn = sqlite3.connect('base_de_datos.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora TEXT NOT NULL,
    nombre TEXT NOT NULL,
    nivel TEXT NOT NULL ,
    info TEXT
    )''')
    conn.commit()
    conn.close()
crear_bd()


