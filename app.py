import os

from flask import Flask

from produits import produits_bp

app = Flask(__name__, static_url_path='')
app.secret_key = os.environ.get("SECRET_KEY", "dev")

app.config["CHEMIN_POUR_AJOUT"] = os.path.join(app.static_folder, "images")
app.config["ROUTE_POUR_AJOUT"] = "/images/"

app.register_blueprint(produits_bp, url_prefix='/produits')
