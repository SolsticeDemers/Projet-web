"""
Ce script décrit le blue print Compte
"""
import re
import hashlib
from flask import Blueprint, render_template, request, redirect, session
import bd

bp_compte = Blueprint('compte', __name__)


def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(mdp_en_clair.encode()).hexdigest()


@bp_compte.route('/authentification', methods= ['GET', 'POST'])
def authentification():
    """Formulaire d'authentification"""

    if request.method == 'GET':
        return render_template("compte/authentification.jinja", nom_page="Authentification")

    nom = request.form.get("nom")
    mdp = request.form.get("mdp")

    # valider que les champs ne sont pas vide

    # mdp = hacher_mdp(mdp)

    with bd.creer_curseur() as curseur:
        utilisateur = bd.get_utilisateur(curseur, nom, mdp)
    if utilisateur is not None:
        # session.permanent = True
        # session['id_utilisateur'] = utilisateur['id_utilisateur']
        # session['nom'] = utilisateur['nom']
        return redirect('/', code=303)

    return redirect('/erreur')
