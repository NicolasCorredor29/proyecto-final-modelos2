from flask import Flask, request, Response, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, send
from pyswip import Prolog

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Habilitar WebSockets

prolog = Prolog()
prolog.consult("pqrs.pl")

@app.route('/usuario', methods=['POST'])
def usuario():
    if request.method == 'POST':
        data = request.get_json()
        print("Diccionario recibido:", data)

        nombre = data.get("nombre", "Usuario")
        tipo_pqrs = data.get("tiposeleccionado", "desconocido")
        cedula = data.get("cc", "")
        descripcion = data.get("pqr", "")

        consulta = f"obtener_respuesta('{nombre}', {tipo_pqrs}, '{cedula}', '{descripcion}', Respuesta)"
        resultado = list(prolog.query(consulta))

        if resultado:
            respuesta = resultado[0]["Respuesta"]
        else:
            respuesta = "Hubo un problema al procesar su solicitud."

        return Response(respuesta, mimetype="text/plain")

# Manejar mensajes en el chat
@socketio.on("message")
def handle_message(msg):
    print(f"Mensaje recibido: {msg}")
    send(msg, broadcast=True)  # Envía el mensaje a todos los clientes conectados


if __name__ == '__main__':
    socketio.run(app, debug=True)
