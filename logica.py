from flask import Flask, request, Response
from flask_cors import CORS
from pyswip import Prolog

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

prolog = Prolog()
prolog.consult("pqrs.pl")  # Cargar la lógica en Prolog

@app.route('/usuario', methods=['POST'])
def usuario():
    if request.method == 'POST':
        data = request.get_json()
        print("Diccionario recibido:", data)

        nombre = data.get("nombre", "Usuario")
        tipo_pqrs = data.get("tiposeleccionado", "desconocido")
        cedula = data.get("cc", "")
        descripcion = data.get("pqr", "")

        # Consultar en Prolog
        consulta = f"obtener_respuesta('{nombre}', {tipo_pqrs}, '{cedula}', '{descripcion}', Respuesta)"
        resultado = list(prolog.query(consulta))

        if resultado:
            respuesta = resultado[0]["Respuesta"]
            if isinstance(respuesta, bytes):  
                respuesta = respuesta.decode("utf-8")
        else:
            respuesta = "Hubo un problema al procesar su solicitud."

        return Response(respuesta, mimetype="text/plain")

if __name__ == '__main__':
    app.run(debug=True)
