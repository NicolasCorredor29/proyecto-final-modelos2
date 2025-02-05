from flask import Flask, render_template, request
from flask_cors import CORS


app=Flask(__name__)
CORS(app, resources={r"/usuario": {"origins": "*"}})
#Uso una lista con los nombres de mis llaves en el diccionario que voy a recibir
aux=['fecha','tiposeleccionado','nombre','direccion','correo','cc','telefono','pqr']
aux2=[]

@app.route('/usuario', methods=['GET','POST'])
def usuario():
    data=request.get_json()
    if request.method=='POST':
        print("Entró a post")
        print(data)
        print(type(data))
        #Aqui recorro mi diccionario y haciendo uso de mi lista auxiliar me quedo con los valores de mi diccionario
        for i in range(8):
            aux2.append(data[aux[i]])
        print(aux2)
        hecho=f"PQRS({aux2[0]},{aux2[1]},{aux2[2]},{aux2[3]},{aux2[4]},{aux2[5]},{aux2[6]},{aux2[7]})"
        with open("bd.pl", "a") as archivo:
            # Escribir el hecho en el archivo
            archivo.write(hecho)
    else:
        print("Entró a get")
        print(data)
        print(type(data))
        #Aqui recorro mi diccionario y haciendo uso de mi lista auxiliar me quedo con los valores de mi diccionario
        for i in range(8):
            aux2.append(data[aux[i]])
        print(aux2)
        hecho=f"PQRS({aux2[0]},{aux2[1]},{aux2[2]},{aux2[3]},{aux2[4]},{aux2[5]},{aux2[6]},{aux2[7]})"
        with open("bd.pl", "a") as archivo:
            # Escribir el hecho en el archivo
            archivo.write(hecho)
    return ""



if __name__ == '__main__':
    app.run(debug=True)   
