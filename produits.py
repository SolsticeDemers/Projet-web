import os
import logging

from flask import  Flask, Blueprint, abort, render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from forms import AjouterProduitForm
from flask import request, session, current_app, url_for
import bd



produits_bp = Blueprint('produits', __name__)

@produits_bp.route('/<int:id>', methods=['GET', 'POST'])
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


    return render_template('produit_details.jinja',
        produit=produit,
        vendeur=vendeur,
        img_source=img_source,
        est_connecte=est_connecte
    )

@produits_bp.route("/ajouter_produit", methods=['GET', 'POST'])
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

