"""
Ce script décrit le blue print Compte
"""
import re
import hashlib
from flask import Blueprint, render_template, request, redirect, session
import bd

regex_courriel = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

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

@bp_compte.route('/creer_compte', methods=['GET', 'POST'])
def creer_compte():
    """Affiche un formulaire"""
    if request.method == 'GET':
        return render_template("compte/creer_compte.jinja", page="Créer un compte")
    nom= request.form.get("nom")
    courriel= request.form.get("courriel")
    ville= request.form.get("ville")
    mdp1= request.form.get("mdp1")
    mdp2= request.form.get("mdp2")

    liste_courriel = []

    with bd.creer_curseur() as curseur:
        dict_courriel = bd.get_courriel_utiliser(curseur)

    for u in dict_courriel:
        liste_courriel.append(u['courriel'])

    a_une_erreur = False

    if mdp1 == "" or mdp1 is None:
        return render_template("compte/creer_compte.jinja", page="Créer un compte")

    if mdp2 == "" or mdp2 is None:
        return render_template("compte/creer_compte.jinja",
            page="Créer un compte")
    elif mdp2 != mdp1:
        return render_template("compte/creer_compte.jinja",
            page="Créer un compte")

    if nom == "" or nom is None:
        return render_template("compte/creer_compte.jinja",
            page="Créer un compte")

    if courriel == "" or courriel is None:
        return render_template("compte/creer_compte.jinja",
            page="Créer un compte")
    elif regex_courriel.match(courriel) is True:
        return render_template("compte/creer_compte.jinja",
            page="Créer un compte")
    elif courriel in liste_courriel:
        return render_template("compte/creer_compte.jinja",
            page="Créer un compte")

    if ville == "default":
        return render_template("compte/creer_compte.jinja",
            page="Créer un compte")

    mdp1 = hacher_mdp(mdp1)
    mdp2 = hacher_mdp(mdp2)

    if a_une_erreur is False:
        with bd.creer_curseur() as curseur:
            id_util =  bd.inserer_utilisateur_bd(curseur, courriel, mdp1, nom, ville)
            session.permanent = True
            session['id_utilisateur'] = id_util
            session['nom'] = nom
        return redirect("/", code=303)
