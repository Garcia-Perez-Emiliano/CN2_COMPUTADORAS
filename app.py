import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

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

if __name__ == '__main__':
    app.run(debug=True)