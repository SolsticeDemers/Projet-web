import os
from flask import Blueprint, session, redirect, url_for, render_template, current_app
import bd

bp_produits = Blueprint('produits', __name__)


@bp_produits.route('/mes_produits')
def mes_produits():
    """Affiche les produits ajoutés par l'utilisateur connecté"""
    if "id_utilisateur" not in session:
        return redirect(url_for("compte.authentification"))

    id_utilisateur = session["id_utilisateur"]

    with bd.creer_curseur() as curseur:
        produits = bd.get_produits_par_vendeur(curseur, id_utilisateur)

    codes_statut = {
    'En vente': 'vente',
    'Aux enchères': 'enchere',
    'À échanger': 'echange',
    'Vendu': 'vendu',
    }

    for produit in produits:
        produit["code_statut"] = codes_statut.get(produit["nom_statut"], "")

        nom_image = f"produit_{produit['id_produit']}.png"
        produit["src"] = None
        if os.path.exists(os.path.join(current_app.config["CHEMIN_IMAGES"], nom_image)):
            produit["src"] = current_app.config["ROUTE_IMAGES"] + nom_image


    return render_template('inventaire.jinja',
        produits=produits
    )

