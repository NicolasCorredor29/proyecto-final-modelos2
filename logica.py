from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send, join_room, leave_room
from pyswip import Prolog

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

prolog = Prolog()
prolog.consult("pqrs.pl")  # Cargar la lógica de Prolog

# Diccionario para almacenar chats pendientes {usuario_id: [mensajes]}
chats_pendientes = {}

@app.route('/usuario', methods=['POST'])
def usuario():
    data = request.get_json()
    usuario_id = data.get("cc")  # Usamos la cédula como ID del usuario
    nombre = data.get("nombre", "Usuario")
    tipo_pqrs = data.get("tiposeleccionado", "desconocido")
    descripcion = data.get("pqr", "")
    
    # Consultar en Prolog la respuesta personalizada
    consulta = f"obtener_respuesta('{nombre}', {tipo_pqrs}, '{usuario_id}', '{descripcion}', Respuesta)"
    resultado = list(prolog.query(consulta))
    
    if resultado:
        respuesta = resultado[0]["Respuesta"]
    else:
        respuesta = "Hubo un problema al procesar su solicitud."

    # Guardar el chat en la lista de pendientes
    chats_pendientes[usuario_id] = [respuesta]

    return Response(respuesta, mimetype="text/plain")

# Endpoint para que el trabajador vea los chats pendientes
@app.route('/chats_pendientes', methods=['GET'])
def obtener_chats():
    return jsonify(list(chats_pendientes.keys()))

# WebSockets para manejar mensajes en salas privadas
@socketio.on("join")
def handle_join(data):
    usuario_id = data["usuario_id"]
    join_room(usuario_id)  # El trabajador o usuario se une a su sala
    print(f"Usuario {usuario_id} ha entrado al chat.")

@socketio.on("message")
def handle_message(data):
    usuario_id = data["usuario_id"]
    mensaje = data["mensaje"]
    
    # Guardar el mensaje en el historial del chat
    if usuario_id in chats_pendientes:
        chats_pendientes[usuario_id].append(mensaje)

    # Enviar el mensaje solo a la sala correspondiente
    send(mensaje, room=usuario_id)

@socketio.on("finalizar_chat")
def finalizar_chat(data):
    usuario_id = data["usuario_id"]
    
    if usuario_id in chats_pendientes:
        del chats_pendientes[usuario_id]  # Eliminar el chat de la lista de pendientes
    
    leave_room(usuario_id)
    send(f"El chat con {usuario_id} ha finalizado.", room=usuario_id)

if __name__ == '__main__':
    socketio.run(app, debug=True)
