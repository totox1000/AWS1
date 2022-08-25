#CARPETA CONTROLADORES
# 1. RECIBE SOLICITUDES ENTRANTES
# 2. LOGICA MINIMA
# 3. LLAMA MODELOS PARA AGREGAR/PROCESAR DATOS
# 4. DETERMINA LA RESPUESTA ADECUADA


from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.car import Car
from flask_app.models.user import User


#Ruta new car
@app.route('/new/car', methods=['GET'])
def new_car():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_car.html',user=User.get_by_id(data))

#Ruta crear auto
@app.route('/create/car',methods=['POST'])
def create_car():
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Car.validate_Car(request.form):
        return redirect('/new/car')

    data = {
        "precio": request.form["precio"],
        "model": request.form["model"],
        "Year": request.form["Year"],
        "Make": request.form["Make"],
        "Description": request.form["Description"],
        "user_id": session["user_id"] # no cambiar esta linea
    }
    print(data, "/*"*20)
    Car.save(data)
    return redirect('/dashboard')

#.........................................................................................................
#Ruta editar auto
@app.route('/edit/car/<int:car_id>')
def edit_car(car_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "car_id":car_id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_car.html",edit=Car.get_one(data),user=User.get_by_id(user_data))
#............................................................................................................
# Ruta actualizar auto
@app.route('/update/car',methods=['POST'])
def update_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_Car(request.form):
        return redirect('/new/car')
    data = {
        "id": int(request.form["id"]),
        "precio": int(request.form["precio"]),
        "model": request.form["model"],
        "Year": request.form["Year"],
        "Make": request.form["Make"],
        "Description": request.form["Description"],
        "user_id": session["user_id"] # no cambiar esta linea
    }
    x = Car.update(data)
    print(x, "RESULTADO EDITAR AUTO")
    return redirect('/dashboard')
#.............................................................................................................
# Ruta show car
@app.route('/car/<int:id>')
def show_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "car_id":id
    }
    #print(data)
    user_data = {
        "id":session['user_id']
    }

    return render_template("show_car.html",car=Car.get_one(data), user=User.get_by_id(user_data))
#...........................................................................................................
# Ruta eliminar auto
@app.route('/destroy/car/<int:id>')
def destroy_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Car.destroy(data)
    return redirect('/dashboard')

#....................................................................................................
#Ruta autos vendidos
@app.route('/vendidos/car', methods=['GET'])
def vendidos():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('vendidos.html',user=User.get_by_id(data))


#/////////////////////////////////////
@app.route("/comprar/<int:id>")
def comprar(id):
    data = {
        "id_comprador": session['user_id'],
        "id_auto": id
    }
    Car.comprar(data)
    return redirect('/dashboard')