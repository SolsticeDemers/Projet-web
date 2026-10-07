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


@bp_compte.route('/authentification', methods=['GET', 'POST'])
def authentification():
    """Formulaire d'authentification"""

    if request.method == 'GET':
        return render_template("compte/authentification.jinja", nom_page="Authentification")

    nom = request.form.get("nom")
    mdp = request.form.get("mdp")

    # valider que les champs ne sont pas vide

    mdp = hacher_mdp(mdp)

    with bd.creer_curseur() as curseur:
        utilisateur = bd.get_utilisateur(curseur, nom, mdp)
    if utilisateur is not None:
        session.permanent = True
        session['id_utilisateur'] = utilisateur['id_utilisateur']
        session['nom'] = utilisateur['nom']
        return redirect('/', code=303)

    return render_template("compte/authentification.jinja", nom_page="Marche pas")


@bp_compte.route('/creer_compte', methods=['GET', 'POST'])
def creer_compte():
    """Affiche un formulaire"""
    if request.method == 'GET':
        return render_template("compte/creer_compte.jinja", page="Créer un compte")
    nom = request.form.get("nom")
    courriel = request.form.get("courriel")
    # ville= request.form.get("ville")
    mdp1 = request.form.get("mdp1")
    mdp2 = request.form.get("mdp2")

    classe_nom = ""
    classe_courriel = ""
    # classe_ville =""
    classe_mdp1 = ""
    classe_mdp2 = ""

    liste_courriel = []
    liste_nom = []

    erreur = False
    num_nom_erreur = 0
    num_courriel_erreur = 0
    num_mdp_erreur = 0

    with bd.creer_curseur() as curseur:
        dict_compte = bd.get_nom_utiliser(curseur)

    for u in dict_compte:
        liste_courriel.append(u['courriel'])

    for u in dict_compte:
        liste_nom.append(u['nom'])

    if mdp1 == "" or mdp1 is None:
        classe_mdp1 = "is-invalid"
        erreur = True
        return render_template("compte/creer_compte.jinja", page="Créer un compte",
                               classe_mdp1=classe_mdp1, nom=nom, courriel=courriel)
    else:
        classe_mdp1 = "is-valid"

    if mdp2 == "" or mdp2 is None:
        classe_mdp2 = "is-invalid"
        erreur = True
        num_mdp_erreur = 1
        return render_template("compte/creer_compte.jinja",
                               page="Créer un compte",
                               classe_mdp2=classe_mdp2,
                               num_mdp_erreur=num_mdp_erreur,
                               nom=nom,
                               courriel=courriel,
                               mdp1=mdp1)
    elif mdp2 != mdp1:
        classe_mdp2 = "is-invalid"
        erreur = True
        num_mdp_erreur = 2
        return render_template("compte/creer_compte.jinja",
                               page="Créer un compte",
                               classe_mdp2=classe_mdp2,
                               num_mdp_erreur=num_mdp_erreur,
                               nom=nom,
                               courriel=courriel)
    else:
        classe_mdp2 = "is-valid"

    if nom == "" or nom is None:
        classe_nom = "is-invalid"
        erreur = True
        num_nom_erreur = 1
        return render_template("compte/creer_compte.jinja",
                               page="Créer un compte",
                               classe_nom=classe_nom,
                               num_nom_erreur=num_nom_erreur,
                               mdp1=mdp1,
                               mdp2=mdp2,
                               courriel=courriel)
    elif nom in liste_nom:
        classe_nom = "is-invalid"
        erreur = True
        num_nom_erreur = 2
        return render_template("compte/creer_compte.jinja",
                               page="Créer un compte",
                               classe_nom=classe_nom,
                               num_nom_erreur=num_nom_erreur,
                               mdp1=mdp1,
                               mdp2=mdp2,
                               courriel=courriel)

    if courriel == "" or courriel is None:
        classe_courriel = "is-invalid"
        erreur = True
        num_courriel_erreur = 1
        return render_template("compte/creer_compte.jinja",
                               page="Créer un compte",
                               classe_courriel=classe_courriel,
                               num_courriel_erreur=num_courriel_erreur,
                               mdp1=mdp1,
                               mdp2=mdp2,
                               nom=nom)
    elif regex_courriel.match(courriel) is True:
        classe_courriel = "is-invalid"
        erreur = True
        num_courriel_erreur = 2
        return render_template("compte/creer_compte.jinja",
                               page="Créer un compte",
                               classe_courriel=classe_courriel,
                               num_courriel_erreur=num_courriel_erreur,
                               mdp1=mdp1,
                               mdp2=mdp2,
                               nom=nom)
    elif courriel in liste_courriel:
        classe_courriel = "is-invalid"
        erreur = True
        num_courriel_erreur = 3
        return render_template("compte/creer_compte.jinja",
                               page="Créer un compte",
                               classe_courriel=classe_courriel,
                               num_courriel_erreur=num_courriel_erreur,
                               mdp1=mdp1,
                               mdp2=mdp2,
                               nom=nom)
    else:
        classe_courriel = "is-valid"

    # if ville == "default":
    #     return render_template("compte/creer_compte.jinja",
    #         page="Créer un compte")

    mdp1 = hacher_mdp(mdp1)

    if erreur is False:
        with bd.creer_curseur() as curseur:
            id_util = bd.inserer_utilisateur_bd(curseur, nom, courriel, mdp1)
            session.permanent = True
            session['id_utilisateur'] = id_util
            session['nom'] = nom
        return redirect("/", code=303)

@bp_compte.route('/deconnection')
def deconnection():
    """Détruit la session"""
    if session is not None:
        session.pop("nom", default=None)
        session.pop("id_utilisateur", default=None)
        session.clear()
    return redirect("/", code=303)
