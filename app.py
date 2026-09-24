import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for

# Cargar las variables de entorno
load_dotenv()

# Crear instancia de Flask
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la base de datos
class InventarioComputadora(db.Model):
    __tablename__ = 'inventario_computadoras'

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    procesador = db.Column(db.String(100), nullable=False)
    ram = db.Column(db.String(20), nullable=False)
    almacenamiento = db.Column(db.String(50), nullable=False)


# Ruta para consultar el inventario
@app.route('/computadoras')
def index():
    # Traer todos los registros
    computadoras = InventarioComputadora.query.all()

    return render_template(
        'index.html',
        computadoras=computadoras
    )

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    # Buscar el registro por su ID
    computadora = InventarioComputadora.query.get_or_404(id)
    
    # Eliminar el registro de la base de datos
    db.session.delete(computadora)
    db.session.commit()
    
    # Redirigir a la función index que carga el inventario
    return redirect(url_for('index'))
@app.route('/computadoras/new', methods=['GET', 'POST'])
def create_computadora():
    if request.method == 'POST':
        # Obtener datos del formulario
        marca = request.form['marca']
        modelo = request.form['modelo']
        procesador = request.form['procesador']
        ram = request.form['ram']
        almacenamiento = request.form['almacenamiento']

        # Crear nueva computadora
        nueva_computadora = InventarioComputadora(
            marca=marca,
            modelo=modelo,
            procesador=procesador,
            ram=ram,
            almacenamiento=almacenamiento
        )

        # Guardar en la base de datos
        db.session.add(nueva_computadora)
        db.session.commit()

        # Regresar al inventario
        return redirect(url_for('index'))

    # Si es GET, mostrar formulario
    return render_template('create_computadora.html')

if __name__ == '__main__':
    app.run(debug=True)