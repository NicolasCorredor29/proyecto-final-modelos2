from flask import Flask, request
from flask_cors import CORS


app=Flask(__name__)
CORS(app, resources={r"/usuario": {"origins": "*"}})
#Uso una lista con los nombres de mis llaves en el diccionario que voy a recibir
aux=['fecha','tiposeleccionado','nombre','direccion','correo','cc','telefono','pqr']
aux2=[]

@app.route('/usuario', methods=['POST'])
def usuario():
    if request.method=='POST':
        data=request.get_json()
        print(data)
        print(type(data))
        #Aqui recorro mi diccionario y haciendo uso de mi lista auxiliar me quedo con los valores de mi diccionario
        for i in range(8):
            aux2.append(data[aux[i]])
        print(aux2)

    return ""


if __name__ == '__main__':
    app.run(debug=True)   
