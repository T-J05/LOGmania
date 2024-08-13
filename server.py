from flask import Flask, request, jsonify
import sqlite3
# import os
# os.environ['WERKZEUG_RUN_MAIN'] = 'false'


app = Flask(__name__)

# Configuración del token de seguridad/ contraseñas
TOKENS = ['hola1', 'hola2']  


def verificar_token(token):
    return token in TOKENS


@app.route('/', methods=['GET'])
def index():
    return "Bienvenido al servidor de logs", 200


def insertar_log(entrada_log):
    try:
        with sqlite3.connect('base_de_datos.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO logs (fecha_hora, nombre, nivel, info)
            VALUES (?, ?, ?, ?)
            ''', (entrada_log['fecha_hora'], entrada_log['nombre'], entrada_log['nivel'], entrada_log['info']))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error al insertar log: {e}")


@app.route('/logs', methods=['POST'])
def recibir_logs():
    token = request.headers.get('Authorization')
    if not verificar_token(token):
        return jsonify({"error": "No autorizado"}), 403

    entrada_log = request.json
    if not entrada_log or not isinstance(entrada_log, dict):
        return jsonify({"error": "Datos inválidos, se esperaba un JSON"}), 400
    
    # Verificar que los campos necesarios estén presentes en el JSON
    campos_requeridos = ['fecha_hora', 'nombre', 'nivel', 'info']
    for campo in campos_requeridos:
        if campo not in entrada_log:
            return jsonify({"error": f"Falta el campo {campo}"}), 400

    insertar_log(entrada_log)
    return jsonify({"status": "Log insertado"}), 201

@app.route('/logs_ver', methods=['GET'])
def obtener_logs():
    try:
        with sqlite3.connect('base_de_datos.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT fecha_hora, nombre, nivel, info FROM logs')
            logs = cursor.fetchall()
            logs_list = [
                {'fecha_hora': log[0], 'nombre': log[1], 'nivel': log[2], 'info': log[3]}
                for log in logs
            ]
    except sqlite3.Error as e:
        print(f"Error al obtener logs: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

    return jsonify(logs_list), 200

if __name__ == "__main__":
    app.run(port=5000)