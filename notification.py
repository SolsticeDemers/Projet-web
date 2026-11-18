
from flask import Blueprint, render_template, request, redirect, session, abort
import bd

bp_notification = Blueprint('notification', __name__)


@bp_notification.route("/faire_echange/<int:id_produit>")
def faire_echange(id_produit):

    session['id_produit_echange'] = id_produit
    session['mode_echange'] = True
    return redirect('/compte/profil', code = 303)



@bp_notification.route("/creer_echange/<int:id_produit_offert>", methods=['GET', 'POST'])
def creer_echange(id_produit_offert):

    with bd.creer_curseur() as curseur:
        produit_echange = bd.get_produit_by_id(
            curseur, session['id_produit_echange'])
    with bd.creer_curseur() as curseur:
        proprio = bd.get_utilisateur_name(
            curseur, produit_echange['id_vendeur'])
    nom_proprio = proprio['nom']
    nom_produit = produit_echange['nom']
    with bd.creer_curseur() as curseur:
            produit_offert = bd.get_produit_by_id(curseur, id_produit_offert)
    nom_produit_offert = produit_offert['nom']
    if request.method == "GET":
        return render_template('faire_echange.jinja', nom_produit=nom_produit, nom_proprio=nom_proprio, nom_produit_offert=nom_produit_offert, id_produit_offert = id_produit_offert)


    with bd.creer_curseur() as curseur:
        id_echange= bd.create_echange(curseur,produit_echange['id_produit'], produit_echange['id_vendeur'], session['id_utilisateur'], produit_offert['id_produit'])
        id_notif = bd.create_notif(curseur, produit_echange['id_vendeur'])
        bd.create_notif_echange(curseur, id_echange, id_notif)
        

    session["mode_echange"] = False
    session.pop("id_produit_echange", None)


    # A changer pour la page transaction
    return redirect('/', 303)