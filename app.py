from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clienti.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PORT'] = int(os.environ.get('PORT', 10000))
db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    settore = db.Column(db.String(100), nullable=False)
    iniziative = db.Column(db.Text, nullable=False)
    dipendenti = db.Column(db.String(100), nullable=False)
    valutazione_marchio = db.Column(db.String(100), nullable=False)
    supporto = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    filtro_settore = request.args.get('settore')
    filtro_iniziative = request.args.get('iniziative')
    filtro_dipendenti = request.args.get('dipendenti')
    
    query = Cliente.query
    if filtro_settore:
        query = query.filter(Cliente.settore.contains(filtro_settore))
    if filtro_iniziative:
        query = query.filter(Cliente.iniziative.contains(filtro_iniziative))
    if filtro_dipendenti:
        query = query.filter(Cliente.dipendenti.contains(filtro_dipendenti))
    
    clienti = query.all()
    return render_template('index.html', clienti=clienti)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=app.config['PORT'])
