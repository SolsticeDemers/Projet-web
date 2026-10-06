"Projet web"

import os
import logging
from flask import Flask, render_template
import bd
from compte import bp_compte
from produits import produits_bp

app = Flask(__name__, static_url_path='')
app.register_blueprint(bp_compte, url_prefix='/compte')
app.register_blueprint(produits_bp, url_prefix='/produits')

app.secret_key = os.environ.get("SECRET_KEY", "dev")

@app.route('/')
def index():
    return render_template('_modele.jinja', nom_page= 'Accueil')

@app.route('/erreur')
def erreur():
    return render_template('erreur.jinja', nom_page= 'erreur')
