import os
import logging
from forms import ArchiverProduitForm

from flask import  Flask, Blueprint, abort, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from forms import AjouterProduitForm
from flask import request, session, current_app, url_for

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

        nom_image = f"produit_{produit['id_produit']}.png"
        produit["src"] = None

        if os.path.exists(
            os.path.join(
                current_app.config["CHEMIN_IMAGES"],
                nom_image
            )
        ):
            produit["src"] = (
                current_app.config["ROUTE_IMAGES"]
                + nom_image
            )

    form = ArchiverProduitForm()

    return render_template(
        'inventaire.jinja',
        produits=produits,
        form_archiver=form
    )


@bp_produits.route('/<int:id>', methods=['GET', 'POST'])
def details_produit(id):
    """Permet de voir les détails d'un produit"""

    form = ArchiverProduitForm()

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
        id=id,
        produit=produit,
        vendeur=vendeur,
        img_source=img_source,
        est_connecte=est_connecte,
        form_archiver=form
    )

@bp_produits.route("/ajouter_produit", methods=['GET', 'POST'])
def ajouter_produit():
    """Permet d'ajouter un produit"""

    if "id_utilisateur" not in session:
        abort(401)

    form = AjouterProduitForm()

    if request.method == "GET":
        form.id_statut.data = 1

    with bd.creer_curseur() as curseur:
        statuts = bd.get_statuts(curseur)
    form.id_statut.choices = [(s["id_statut"], s["nom_statut"]) for s in statuts]

    if form.validate_on_submit():
        nom = request.form["nom"]
        description = request.form["description"]
        prix = float(request.form["prix"])
        id_statut = int(request.form["id_statut"])
        image = request.files.get("image")

        with bd.creer_curseur() as curseur:
            id_produit = bd.ajouter_produit(
                curseur,
                session["id_utilisateur"],
                nom,
                description,
                prix,
                id_statut
            )

        if image and image.filename:
            nom_image = f"produit_{id_produit}.png"
            chemin = os.path.join(current_app.config["CHEMIN_IMAGES"], nom_image)
            image.save(chemin)

        return redirect(url_for("produits.details_produit", id=id_produit))

    return render_template("ajouter_produit.jinja", form=form)


@bp_produits.route("/<int:id>/archiver", methods=['POST'])
def archiver_produit(id):
    """Permet d'archiver un produit"""

    if "id_utilisateur" not in session:
        abort(401)

    form = ArchiverProduitForm()

    if not form.validate_on_submit():
        abort(400)

    with bd.creer_curseur() as curseur:
        produit = bd.get_produit(curseur, id)

        if produit is None:
            abort(404)

        if produit['id_vendeur'] != session['id_utilisateur']:
            abort(403)

        bd.archiver_produit(curseur, id)

    return redirect(url_for("compte.profil"))
