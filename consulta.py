import sqlite3

# Conexión a la base de datos SQLite
conn = sqlite3.connect('base_de_datos.db')
cursor = conn.cursor()

# Definir el rango de fechas y horas
fecha_inicio = '2024-08-12 23:45:38,267'
fecha_fin = '2024-08-12 23:48:17,238'

# Consulta SQL para obtener los registros dentro del rango de fechas y horas
consulta = """
SELECT * FROM logs
WHERE fecha_hora BETWEEN ? AND ?
"""

# Ejecutar la consulta
cursor.execute(consulta, (fecha_inicio, fecha_fin))

# Obtener los resultados
resultados = cursor.fetchall()

# Mostrar los resultados
for fila in resultados:
    print(fila)

# Cerrar la conexión
conn.close()