import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuración de base de datos
db_uri = os.getenv('DATABASE_URL', '')
if db_uri.startswith('postgres://'):
    db_uri = db_uri.replace('postgres://', 'postgresql://', 1)

if db_uri and 'sslmode=' not in db_uri and 'localhost' not in db_uri and '127.0.0.1' not in db_uri:
    separator = '&' if '?' in db_uri else '?'
    db_uri = f"{db_uri}{separator}sslmode=require"

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri if db_uri else 'sqlite:///computadoras.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos
class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    computers = db.relationship('Computer', backref='brand', lazy=True)

class Computer(db.Model):
    __tablename__ = 'computers'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    processor = db.Column(db.String(100), nullable=False)
    ram = db.Column(db.String(50), nullable=False)
    storage = db.Column(db.String(50), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id', ondelete='SET NULL'), nullable=True)

# Creación de tablas e inserción de datos iniciales
with app.app_context():
    db.create_all()
    if not Brand.query.first():
        marcas = [Brand(name='Dell'), Brand(name='HP'), Brand(name='Lenovo'), Brand(name='Apple'), Brand(name='Asus')]
        db.session.add_all(marcas)
        db.session.commit()

    if not Computer.query.first():
        hp = Brand.query.filter_by(name='HP').first()
        pc_demo = Computer(
            model='Pavilion 15',
            processor='Intel Core i5 12va Gen',
            ram='16 GB',
            storage='512 GB SSD',
            brand_id=hp.id if hp else None
        )
        db.session.add(pc_demo)
        db.session.commit()

# Rutas
@app.route('/')
def index():
    computers = Computer.query.all()
    return render_template('index.html', computers=computers)

@app.route('/computer/new', methods=['GET', 'POST'])
def add_computer():
    if request.method == 'POST':
        model = request.form.get('model')
        processor = request.form.get('processor')
        ram = request.form.get('ram')
        storage = request.form.get('storage')
        brand_id = request.form.get('brand_id')

        new_pc = Computer(
            model=model,
            processor=processor,
            ram=ram,
            storage=storage,
            brand_id=brand_id
        )
        db.session.add(new_pc)
        db.session.commit()
        return redirect(url_for('index'))

    brands = Brand.query.all()
    return render_template('create_computer.html', brands=brands)

@app.route('/computer/edit/<int:id>', methods=['GET', 'POST'])
def edit_computer(id):
    computer = Computer.query.get_or_404(id)
    brands = Brand.query.all()

    if request.method == 'POST':
        computer.brand_id = request.form.get('brand_id')
        computer.model = request.form.get('model')
        computer.processor = request.form.get('processor')
        computer.ram = request.form.get('ram')
        computer.storage = request.form.get('storage')

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_computer.html', computer=computer, brands=brands)

if __name__ == '__main__':
    app.run(debug=True)