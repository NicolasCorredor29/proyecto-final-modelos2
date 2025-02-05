from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from pyswip import Prolog

app = Flask(__name__)
CORS(app)

prolog = Prolog()


# Diccionarios para almacenar PQRS y respuestas enviadas
pqrs_pendientes = {}
respuestas_enviadas = {}

#Voy a usar listar auxiliares para tomar la información de los diccionarios
#json
aux=['fecha','tiposeleccionado','nombre','direccion','correo','cc','telefono','pqr']

@app.route('/usuario', methods=['POST'])
def usuario():
    aux2=[]
    """Recibe los datos del PQRS y los almacena"""
    data = request.get_json()
    usuario_id = data.get("cc") 
    for i in range(8):
            aux2.append(data[aux[i]])
    hecho=f"PQRS({aux2[0]},{aux2[1]},{aux2[2]},{aux2[3]},{aux2[4]},{aux2[5]},{aux2[6]},{aux2[7]}).\n"
    with open("bd.pl", "a") as archivo:
            # Escribir el hecho en el archivo
            archivo.write(hecho)
    
    # Guardar PQRS en la lista de pendientes
    pqrs_pendientes[usuario_id] = data

    return Response("Su PQRS ha sido registrada.", mimetype="text/plain")

@app.route('/pqrs_pendientes', methods=['GET'])
def obtener_pqrs():
    """Devuelve la lista de PQRS pendientes"""
    return jsonify(pqrs_pendientes)

@app.route('/enviar_respuesta', methods=['POST'])
def enviar_respuesta():
    """Recibe la respuesta del administrador y la almacena"""
    data = request.get_json()
    print(data)
    usuario_id = data.get("cc")
    respuesta = data.get("respuesta")
    hecho=f"RESPUESTA({usuario_id},{respuesta}).\n"
    with open("bd.pl", "a") as archivo:
            # Escribir el hecho en el archivo
            archivo.write(hecho)

    if usuario_id in pqrs_pendientes:
        respuestas_enviadas[usuario_id] = respuesta  # Guardar respuesta
        del pqrs_pendientes[usuario_id]  # Eliminar PQRS ya respondido

        print("Respuestas almacenadas:", respuestas_enviadas) 

        return Response(f"Respuesta enviada a {usuario_id}", mimetype="text/plain")

    return Response("No se encontró la PQRS para este usuario.", mimetype="text/plain")

@app.route('/obtener_respuesta/<usuario_id>', methods=['GET'])
def obtener_respuesta(usuario_id):
    """Devuelve la respuesta enviada al usuario si existe"""
    respuesta = respuestas_enviadas.get(usuario_id, "Aún no hay respuesta disponible.")

    print(f"Consulta de respuesta para {usuario_id}: {respuesta}")  

    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
