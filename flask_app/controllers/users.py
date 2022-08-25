from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.car import Car
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#................................................................................................................

# INDEX.HTML
#ASOCIADO AL TEMPLATE DE INDEX.HTML
@app.route('/')
def index():
    return render_template('index.html')

#ASOCIADO AL TEMPLATE DE INDEX.HTML
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user=User.get_by_id(data)
    cars=Car.get_all()
    return render_template("dashboard.html",user=user, cars=cars)
#...................................................................................................................
#ASOCIADO A LA TABLA LOGIN DEL INDEX.HTML
@app.route('/login',methods=['POST'])
def login():
    # ver si el nombre de usuario proporcionado existe en la base datos
    user = User.get_by_email(request.form)
# usuario no esta registrado en la base de datos
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        # si obtenemos el false despues de verificar la constraseña
        flash("Invalid Password","login")
        return redirect('/')
        # si las contraseñas coinciden, configuramos el user_id en sesion
    # almacenar id de usuario en la sesion
    session['user_id'] = user.id
    return redirect('/dashboard')

#ASOCIADO A LA TABLA REGISTER DEL INDEX.HTML
@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        # redirigimos a la plantilla con el formulario
        return redirect('/')
        #...hacer otras cosas
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
#..........................................................................................................................
#DASHBOARD.HTML

    return redirect('/dashboard')

#DEL DASHBOARD.HTM BOTON HACIA LOGOUT REDIRIGE AL INDEX.HTML (REGISTRO INICIAL)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')