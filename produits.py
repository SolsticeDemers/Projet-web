from flask import Blueprint, abort, render_template, redirect
from flask import request, session, current_app, url_for
import bd

produits_bp = Blueprint('produits', __name__)

@produits_bp.route('/<int:identifiant>', methods=['GET'])
def details_produit(identifiant):
    """Permet de voir les détails d'un produit"""
    with bd.creer_curseur() as curseur:
        produit = bd.get_produit(curseur, identifiant)
    if produit is None:
        abort(404)
    return render_template('details_produit.html', #mettre info produit
    )