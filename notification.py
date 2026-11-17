
from flask import Blueprint, render_template, request, redirect, session, abort
import bd

bp_notification = Blueprint('notification', __name__)


# @bp_notification.route("/faire_echange")
# def faire_echange(id_produit):
#     session['id_produit_echange'] = id_produit
#     return redirect('/creer_echange', code = 303)



@bp_notification.route("/creer_echange/<int:id_produit_echange>", methods=['GET', 'POST'])
def creer_echange(id_produit_echange):
    if request.method == 'GET':
          print("get")
    else:
          print("post")      
    
    with bd.creer_curseur() as curseur:
        produit_echange = bd.get_produit(curseur, id_produit_echange)
        print("AAAAAAAA")
        print(produit_echange)
    print(produit_echange['id_vendeur'])
    with bd.creer_curseur() as curseur:
        nom_proprio = bd.get_utilisateur_name(curseur,produit_echange['id_vendeur'])
    nom_proprio = nom_proprio['nom']
    nom_produit = produit_echange['nom']
    with bd.creer_curseur() as curseur:
                produits = bd.get_produits_par_vendeur(
                    curseur,
                    session['id_utilisateur']
                )
    if request.method == "GET":
        return render_template('faire_echange.jinja', nom_produit = nom_produit, nom_proprio = nom_proprio, produits = produits)

    