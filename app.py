from flask import Flask,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__) #Crea el objeto app de la clase Flask
CORS(app) #permite acceder desde el front al back

# configuro la base de datos, con el nombre el usuario y la clave
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user:password@localhost/proyecto'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

# ---------fin configuracion-----------

#definimos la tabla
class Adm(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    usuario=db.Column(db.String(100))
    nombre=db.Column(db.String(100))
    email=db.Column(db.String(100))
    password=db.Column(db.String(50))
    def __init__(self,usuario,nombre,email,password):
        self.usuario = usuario
        self.nombre = nombre
        self.email = email
        self.password = password

    #Si hay mas tablas para crear las definimos aca

with app.app_context():
    db.create_all() #Crea las tablas

class UserSchema(ma.Schema):
    class Meta:
        fields=('id','usuario','nombre','email','password')
    
user_schema=UserSchema() #El objeto para traer un producto
users_schema=UserSchema(many=True) #Trae muchos registro de producto



#Creamos los endpoint
#GET
#POST
#Delete
#Put

#Get endpoint del get
@app.route('/usuarios',methods=['GET'])
def get_Users():
    all_users = Adm.query.all() #heredamos del db.model
    result= users_schema.dump(all_users) #lo heredamos de ma.schema
                                                #Trae todos los registros de la tabla y los retornamos en un JSON
    return jsonify(result)


@app.route('/usuarios/<id>',methods=['GET'])
def get_user(id):
    user=Adm.query.get(id)
    return user_schema.jsonify(user)   # retorna el JSON de un producto recibido como parametro




@app.route('/usuarios/<id>',methods=['DELETE'])
def delete_user(id):
    user=Adm.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)   # me devuelve un json con el registro eliminado


@app.route('/usuarios', methods=['POST']) # crea ruta o endpoint
def create_user():
    #print(request.json)  # request.json contiene el json que envio el cliente
    usuario=request.json['usuario']
    nombre=request.json['nombre']
    email=request.json['email']
    password=request.json['password']
    new_user=Adm(usuario,nombre,email,password)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)


@app.route('/usuarios/<id>' ,methods=['PUT'])
def update_user(id):
    user=Adm.query.get(id)
 
    user.usuario=request.json['usuario']
    user.nombre=request.json['nombre']
    user.email=request.json['email']
    user.password=request.json['password']


    db.session.commit()
    return user_schema.jsonify(user)

#Programa Principal
if __name__ == '__main__':
    app.run(debug=True, port=5000)

