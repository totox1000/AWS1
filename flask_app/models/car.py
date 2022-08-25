

from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

# TABLA CARS: Es importante que esta lista sea igual al la base de datos
class Car:
    db_name = 'cars'

    def __init__(self,db_data): # uno elige el nombre db_data u otra cosa
        self.id = db_data['id']
        precio=db_data['precio']
        precio='{:,}'.format(precio).replace(',','.')
        self.precio = precio
        self.model = db_data['model']
        self.Year = db_data['Year']
        self.Make = db_data['Make']
        self.Description = db_data['Description']
        self.user_id = db_data['user_id']
    

# bloque completo 1 de aqui abajo

#CREAR..Es importante que esta lista sea igual al la base de datos
    @classmethod
    def save(cls,data):
        query = """INSERT INTO cars (precio, model, Year, Make, Description, user_id)
        VALUES (%(precio)s,%(model)s,%(Year)s,%(Make)s,%(Description)s, %(user_id)s);"""
        result = connectToMySQL(cls.db_name).query_db(query, data)
        print("crear cars", result)
        return result

#LEER
## obtiene todas los autos y los devuelve en una lista de objetos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars JOIN users ON cars.user_id=users.id ;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_cars = []
        for row in results:
            #print(row['date_made'])
            all_cars.append( cls(row) )
        return results

# aqui termina el bloque completo 1 //

# VIEW ESTO AGREGAR UN LINK DE VER EN EL DASHBOARD.HTML DONDE SE MUESTRAN LOS AUTOS INGRESADOS
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM cars WHERE id = %(car_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        #print(results[0])
        return cls( results[0] )

#EDITAR...ESTO AGREGAR UN LINK DE EDIT EN EL DASHBOARD.HTML DONDE SE MUESTRAN LOS AUTOS INGRESADOS
    @classmethod
    def update(cls, data):
        query = """UPDATE cars SET precio=%(precio)s, model=%(model)s, Year=%(Year)s, Make=%(Make)s, Description=%(Description)s WHERE (id = %(id)s);"""
        return connectToMySQL(cls.db_name).query_db(query,data)

#BORRAR...ESTO AGREGAR UN LINK DE DELETE EN EL DASHBOARD.HTML DONDE SE MUESTRAN LOS AUTOS INGRESADOS
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

#COMPRAR VEHICULO
    @classmethod
    def comprar(cls,data):
        query = " UPDATE cars SET vendedor_id = %(id_comprador)s WHERE (id = %(id_auto)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

# METODO DE VALIDACION PARA INGRESAR EL NUEVO AUTO ASOCIADO (new_car.html) 
# SI NO SE CUMPLEN CON LOS CARACTERES MINIMOS APARECERAN ESTAS ALERTAS
# TABLA AGREGAR AUTO A LA VENTA
    @staticmethod
    def validate_Car(car):
        is_valid = True
        # MODELO
        if len(car['model']) < 3:
            is_valid = False
            flash("Model must be at least 3 characters","car")
            # MARCA
        if len(car['Make']) < 3:
            is_valid = False
            flash("Make must be at least 3 characters","car")
            # DESCRIPCION
        if len(car['Description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","car")
            # AÑO
        if car['Year'] == "":
            is_valid = False
            flash("Please enter a year","car")
        return is_valid





