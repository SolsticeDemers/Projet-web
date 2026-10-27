import os

from flask import Blueprint, session, redirect, url_for, render_template
from flask import current_app, abort
import bd


bp_produits = Blueprint('produits', __name__)


@bp_produits.route('/mes_produits')
def mes_produits():
    """Affiche les produits ajoutés par l'utilisateur connecté"""

    if "id_utilisateur" not in session:
        return redirect(url_for("compte.authentification"))

    id_utilisateur = session["id_utilisateur"]

    with bd.creer_curseur() as curseur:
        produits = bd.get_produits_par_vendeur(
            curseur,
            id_utilisateur
        )

    codes_statut = {
        'En vente': 'vente',
        'Aux enchères': 'enchere',
        'À échanger': 'echange',
        'Vendu': 'vendu',
    }

    for produit in produits:

        produit["code_statut"] = codes_statut.get(
            produit["nom_statut"],
            ""
        )

        nom_image = (
            "produit_"
            + str(produit["id_produit"])
            + ".png"
        )

        produit["src"] = None

        chemin_image = os.path.join(
            current_app.config["CHEMIN_IMAGES"],
            nom_image
        )

        if os.path.exists(chemin_image):
            produit["src"] = (
                current_app.config["ROUTE_IMAGES"]
                + nom_image
            )

    return render_template(
        'inventaire.jinja',
        produits=produits
    )


@bp_produits.route('/<int:id>', methods=['GET', 'POST'])
def details_produit(id):
    """Permet de voir les détails d'un produit"""

    with bd.creer_curseur() as curseur:
        produit = bd.get_produit(curseur, id)

        if produit is None:
            abort(404)

        vendeur = bd.get_vendeur(
            curseur,
            produit['id_vendeur']
        )

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
        img_source = (
            current_app.config["ROUTE_IMAGES"]
            + nom_image
        )
    else:
        img_source = url_for(
            "static",
            filename="images/default.png"
        )

    return render_template(
        'produit_details.jinja',
        produit=produit,
        vendeur=vendeur,
        img_source=img_source,
        est_connecte=est_connecte
    )