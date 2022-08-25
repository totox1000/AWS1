# TABLA USERS

# CARPETA MODELO/USER.PY
# 1. PUEDE CONSTRUIR TABLAS DE BASES DE DATOS
# 2. MANEJA LA LOGICA QUE SE BASA EN DATOS
# 3. SE INTERRELACIONA CON LA BASE DE DATOS

from flask_app.config.mysqlconnection import connectToMySQL
import re	# el modulo regex
# crea un objeto de expresion regular que usaremos mas adelante   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
#...........................................................................
# TABLA USER: Es importante que esta lista sea igual al la base de datos
class User:
    db_name = "cars"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

#LEER..Selecciona la tabla de datos users Selecciona toda la tabla
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # # Esta consulta se asegura de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL(cls.db_name).query_db(query) # el (cls.db_name) deberia ser cambiado por el nombre de la base de datos
        # crear una lista vacía para agregar nuestras instancias de user
        users = []
        # Iterar sobre los resultados de la base de datos y crear instancias de users con cls
        for row in results:
            users.append( cls(row))
        return users

#.......................................................................................

#CREAR...Es importante que esta lista sea igual al la base de datos
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)




#LEER..Selecciona la tabla de datos users a la columna email
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        # no se encontro un usuario coincidente
        if len(results) < 1:
            return False
        return cls(results[0])

#LEER..Selecciona la tabla de datos users a la primera columna  id
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results, "GETBYID")
        print(cls(results[0]), "GETBYID")
        return cls(results[0])

# METODO DE VALIDACION PARA INGRESAR EL NUEVO USUARIO ASOCIADO AL (index.html) 
# SI NO SE CUMPLEN CON LOS CARACTERES MINIMOS APARECERAN ESTAS ALERTAS
# TABLA REGISTER EN index.hml
    @staticmethod
    def validate_register(user):
        is_valid = True
        # prueba si un campo coincide con el patron
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)
            # Email
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
            # first Name
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
            # Last Name
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
            # Password
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
            # Confirm Password
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid