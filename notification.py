
from flask import Blueprint, render_template, request, redirect, session, abort
import bd

bp_notification = Blueprint('notification', __name__)


@bp_notification.route("/faire_echange")
def faire_echange(id_produit):
    session['id_produit_echange'] = id_produit



@bp_notification.route("/creer_echange", methods=['GET', 'POST'])
def creer_echange():
    with bd.creer_curseur() as curseur:
        produit_echange = bd.get_produit_by_id(curseur, session['id_produit_echange'])
        nom_proprio = bd.get_utilisateur_name(curseur,produit_echange['id_vendeur'])
    nom_produit = produit_echange['nom']
    
    if request.method == "GET":
        return render_template('faire_echange.jinja', nom_produit = nom_produit, nom_proprio = nom_proprio)

    