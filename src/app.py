from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config
from validate import *


app = Flask (__name__)

conexion = MySQL(app)

@app.route('/', methods=['GET'])

def index ():
        try:
            cursor = conexion.connection.cursor()
            sql = "SELECT id, email FROM users"
            cursor.execute(sql)
            datos = cursor.fetchall()
            dato = []
            for fila in datos:
                user = {
                      'id' : fila [0],
                      'email': fila [1]
                      }
                dato.append(user)            
            return jsonify({'dato': dato, 'mensaje': "Listar usuarios", 'confirm': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error en la consulta a la BD", 'confirm': False})  

def leer_usuario_porID (id):
        try:
            cursor = conexion.connection.cursor()
            sql = "SELECT id, email FROM users WHERE id = '{0}'".format(id)
            cursor.execute(sql)
            datos = cursor.fetchone()
            if datos != None:
                 dato= {'id': datos[0], 'email': datos[1]}
                 return dato
            else:
                 return None
        except Exception as ex:
            raise ex
    
@app.route('/<id>', methods=['GET'])
def leer_usuario(id):
     try:
          usuario =leer_usuario_porID(id)
          if usuario != None :
               return jsonify({'usuario': usuario, 'mensaje': 'usuario encontrado', 'confirm': True})
          else:
               return jsonify({'mensaje': 'usuario No encontrado', 'confirm': False})
     except Exception as ex:
          return jsonify({'mensaje': "Error", 'confirm': False})
             
def pagina_no_encontrada(error):
  return "<h1> Pagina no encontrada</h1>",484

@app.route('/', methods=['POST'])
def agregar():
    # if(validateEmail(request.json['email']) and validatePass(request.json['pass'])):
        try:
            usuario = leer_usuario_porID(request.json['id'])
            if usuario != None:
                return jsonify({'mensaje' : 'Error ya existe el ID','confirm': False})
            else:
                cursor= conexion.connection.cursor()
                sql = "INSERT INTO users (id, email, pass) VALUES ({0}, '{1}', '{2}')".format(request.json['id'],request.json['email'],request.json['pass'])
                cursor.execute(sql)
                conexion.connection.commit()
                return jsonify({'mensaje':'usuario registrado','confirm': True})
        except Exception as ex:
             return jsonify({'mensaje': 'Error usuario no registrado','confirm':False})   
    # else:
      #   return jsonify({'mensaje': 'Valores no validos', 'confirm':False})
          

def eliminar_usuario_porID(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM users WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return True
    except Exception as ex:
        raise ex

@app.route('/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        usuario = leer_usuario_porID(request.json['id'])
        if eliminar_usuario_porID(id):

            if usuario == None:
                return jsonify({'mensaje': 'No se encontró el usuario', 'confirm': False})
            else:
                return jsonify({'mensaje': 'Usuario eliminado correctamente', 'confirm': True})
            
    except Exception as ex:
        return jsonify({'mensaje': 'Error al eliminar el usuario', 'confirm': False})



def pagnoEncontrada(error):
     return jsonify({'mensaje': 'Error', 'confirm':False})

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug =True, port=3000)


 




