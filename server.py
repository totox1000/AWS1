

from flask_app import app

from flask_app.controllers import cars, users

if __name__=="__main__":
    app.run(debug=True) # ejecuta la aplicacion en modo de depuracion