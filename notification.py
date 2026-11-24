
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
    if "id_produit_echange" not in session:
        abort(409)
    with bd.creer_curseur() as curseur:
        echange_existant = bd.get_echange_existant(
            curseur,
            session['id_produit_echange'],
            session['id_utilisateur'],
            id_produit_offert
        )

    if echange_existant:
        abort(409)
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

    return redirect('/produits/transactions', 303)



def echange(notif, notifications, id_status, id_notif):

    if session['id_utilisateur'] == notif['id_utilisateur']:

        with bd.creer_curseur() as curseur:

            proprio = bd.get_utilisateur_name(

                curseur, notif['proprio'])

            proprio = proprio['nom']

            offrant = session['nom']

    else:

        with bd.creer_curseur() as curseur:

            offrant = bd.get_utilisateur_name(

                curseur, notif['id_utilisateur'])

            offrant = offrant['nom']

            proprio = session['nom']

    with bd.creer_curseur() as curseur:
        produit = bd.get_produit_by_id(
            curseur, notif['produit'])

    with bd.creer_curseur() as curseur:

        status = bd.get_statut_by_Id(

                    curseur, id_status)

    status = status['nom_statut']


    with bd.creer_curseur() as curseur:

        produit_offert = bd.get_produit_by_id(

            curseur, notif['produit_offert'])

        une_notification = {

            "id_proposition": notif['id_echange'],

            "id_notif": id_notif,

            "proprio": proprio,

            "offrant": offrant,
            "echange_nom": produit['nom'],
            "id_produit": produit['id_produit'],
            "offert_nom": produit_offert['nom'],
            "id_produit_offert": produit_offert['id_produit'],
            "status": status,

            "approuve": notif['approuver']

        }

    notifications.append(une_notification)

    return notifications


def enchere(notif, notifications, id_notif):

    """Prépare une notification d'enchère gagnée"""


    with bd.creer_curseur() as curseur:

        produit = bd.get_notif_enchere(

            curseur,

            id_notif

        )


    une_notification = {

        "id_notif": id_notif,

        "nom_produit": produit["nom"],

        "id_produit": produit["id_produit"],

        "prix": produit["prix"]

    }


    notifications.append(une_notification)


    return notifications


@bp_notification.route('/notification')
def notification():
    """Affiche les notifications de l'utilisateur"""

    if "id_utilisateur" not in session:
        abort(401)

    notifications_enchere = []
    notifications_echange = []

    with bd.creer_curseur() as curseur:
        notifications = bd.get_notification(
            curseur,
            session['id_utilisateur']
        )

        notifications_achat = bd.get_notifications_achat(
            curseur,
            session['id_utilisateur']
        )

    for notif in notifications:

        with bd.creer_curseur() as curseur:
            bd.update_notification(
                curseur,
                notif['id_notification'],
                1
            )

        if notif['id_statut'] == 3:

            with bd.creer_curseur() as curseur:
                notif_echange = bd.get_notif_echange(
                    curseur,
                    notif['id_notification']
                )

            notifications_echange = echange(
                notif_echange,
                notifications_echange,
                notif['id_statut'],
                notif['id_notification']
            )

        elif notif['id_statut'] == 2:

            notifications_enchere = enchere(
                notif,
                notifications_enchere,
                notif['id_notification']
            )

    return render_template(
        "notification.jinja",
        notifications_echange=notifications_echange,
        notifications_achat=notifications_achat,
        notifications_enchere=notifications_enchere
    )


@bp_notification.route('/accepter_echange/<int:id_echange>/<string:approuve>')

def accepter_echange(id_echange, approuve):


    if approuve == "oui":

        reponse = 1
    else:

        reponse = 0

    with bd.creer_curseur() as curseur:

        bd.update_offer(curseur, id_echange, reponse)

        id_notification= bd.create_notif_offrant(curseur, id_echange)

        bd.create_notif_echange(curseur,id_echange, id_notification)

    if reponse == 1:
        with bd.creer_curseur() as curseur:
            echange= bd.get_echange_by_id(curseur, id_echange)
            bd.update_produit_echange(curseur, echange['produit_offert'], session['id_utilisateur'])
            bd.update_produit_echange(curseur, echange['produit'], echange['id_utilisateur'])
        

    return redirect("/notification/notification", code=303)
