from flask import Flask
import requests as rq
import logging
import random as rd

# Desactivar logs de werkzeug
logging.getLogger('werkzeug').disabled = True
app = Flask(__name__)
token = 'hola2'  # Token para el servicio
url = "http://127.0.0.1:5000/logs"  # URL para enviar el log al servidor

class LogManejadorHttp(logging.Handler):
    def __init__(self, url, token):
        super().__init__()
        self.url = url
        self.token = token
        self.formatter = logging.Formatter('%(asctime)s')
    def emit(self, record):
        if "This is a development server" in record.msg or "Running on" in record.msg or "Press CTRL+C to quit" in record.msg:
            return 
        self.format(record)
        entrada_log = {
            'fecha_hora': record.asctime,
            'nivel': record.levelname,
            'nombre': 'service2',
            'info': record.msg
        }
        encabezado = {'Authorization': self.token}  # Encabezado para verificar token
        try:
            respuesta = rq.post(self.url, json=entrada_log, headers=encabezado)
            respuesta.raise_for_status()
        except rq.exceptions.HTTPError as err:
            print(f'Error HTTP al enviar log: {err}')
        except Exception as e:
            print(f'Error enviando log: {e}')

# Configuración de logging manual
logger = logging.getLogger()  # Obtén el logger raíz
logger.setLevel(logging.INFO)  # Establece el nivel del logger
loggin_url = LogManejadorHttp(url, token)  # Tu manejador personalizado

# Elimina cualquier otro manejador asociado para evitar duplicados
if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(loggin_url)  # Agrega nuevamente el manejador

# Configuración de Flask
app = Flask(__name__)


@app.route("/dividir",methods=['GET'])
def dividir():
    nr = 5
    try:
        resultado = nr//0
        print(resultado)
    
    except Exception as e:
        logging.error(f'No se puede dividir con 0: {e}')

if __name__ == "__main__":
    app.run(port=5002)