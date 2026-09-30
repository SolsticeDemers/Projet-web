from flask import Flask
from produits import bp_produits

app = Flask(__name__, static_url_path='')

app.register_blueprint(bp_produits, url_prefix='/produits')