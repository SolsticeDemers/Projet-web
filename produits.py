import os
import logging

from flask import Flask, Blueprint, abort, render_template, redirect, flash
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
                           id=id,
                           produit=produit,
                           vendeur=vendeur,
                           img_source=img_source,
                           est_connecte=est_connecte
                           )


@produits_bp.route("/<int:id>/modifier", methods=['GET', 'POST'])
def modifier_produit(id):
    """Permet de modifier un produit"""
    if "id_utilisateur" not in session:
        abort(401)

    with bd.creer_curseur() as curseur:
        produit = bd.get_produit(curseur, id)
        statuts = bd.get_statuts(curseur)

    if produit is None:
        abort(404)
    if produit['id_vendeur'] != session['id_utilisateur']:
        abort(403)

    nom_image = f"produit_{id}.png"
    chemin_image = os.path.join(current_app.config["CHEMIN_IMAGES"], nom_image)

    form = AjouterProduitForm()
    form.id_statut.choices = [
            (statut['id_statut'], statut['nom_statut']) for statut in statuts]

    if request.method == 'GET':
        form.nom.data = produit['nom']
        form.description.data = produit['description']
        form.prix.data = produit['prix']
        form.id_statut.data = produit['id_statut']

    if form.validate_on_submit():
        with bd.creer_curseur() as curseur:
            bd.modifier_produit(
                curseur, id,
                request.form["nom"],
                request.form["description"],
                float(request.form["prix"]),
                int(request.form["id_statut"])
            )

        image = request.files.get("image")
        if image and image.filename:
            image.save(chemin_image)

        return redirect(url_for("produits.details_produit", id=id))

    if os.path.exists(chemin_image):
        img_source = current_app.config["ROUTE_IMAGES"] + nom_image
    else:
        img_source = url_for("static", filename="images/default.png")

    return render_template("modifier_produit.jinja", form=form, produit=produit, img_source=img_source)
