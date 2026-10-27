import os

from flask import Blueprint, abort, render_template, redirect
from flask import request, session, current_app, url_for
from forms import PanierForm
import bd

produits_bp = Blueprint('produits', __name__)


@produits_bp.route('/<int:id>', methods=['GET'])
def details_produit(id):
    """Permet de voir les détails d'un produit"""
    with bd.creer_curseur() as curseur:
        produit = bd.get_produit(curseur, id)

        if produit is None:
            abort(404)

        vendeur = bd.get_vendeur(curseur, produit['id_vendeur'])

    nom_image = "produit_" + str(id) + ".png"
    chemin_image = os.path.join(
        current_app.config["CHEMIN_IMAGES"],
        nom_image
    )

    if "id_utilisateur" in session:
        est_connecte = True
    else:
        est_connecte = False

    if os.path.exists(chemin_image):
        img_source = current_app.config["ROUTE_IMAGES"] + nom_image
    else:
        img_source = url_for("static", filename="images/default.png")


    est_vendeur = False
    if est_connecte and produit["id_vendeur"] == session["id_utilisateur"]:
        est_vendeur = True

    est_disponible = False
    if produit["archive"] == False and produit["id_statut"] != 4:
        est_disponible = True

    form = PanierForm()

    return render_template('produit_details.jinja',
        produit=produit,
        vendeur=vendeur,
        img_source=img_source,
        est_connecte=est_connecte,
        est_vendeur=est_vendeur,
        est_disponible=est_disponible,
        form=form
    )
