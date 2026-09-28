"Projet web"

import os
import logging
from flask import Flask, render_template
import bd
from compte import bp_compte

app = Flask(__name__, static_url_path='')
app.register_blueprint(bp_compte, url_prefix='/compte')

@app.route('/')
def index():
    return render_template('_modele.jinja', nom_page= 'Accueil')

@app.route('/erreur')
def erreur():
    return render_template('erreur.jinja', nom_page= 'erreur')