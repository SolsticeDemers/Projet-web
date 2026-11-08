"""Blueprint api"""
from flask import Blueprint, request, jsonify, session
import bd
bp_api = Blueprint("api", __name__)


@bp_api.route('/courriel_unique')
def courriel_unique():

    courriel = request.args.get("courriel")

    with bd.creer_curseur() as curseur:
        compte = bd.get_courriel_unique(curseur, courriel)
    if compte is not None:
        is_unique = False
    else:
        is_unique = True
    return jsonify(is_unique)


@bp_api.route('/nom_unique')
def nom_unique():

    nom = request.args.get("nom")

    with bd.creer_curseur() as curseur:
        compte = bd.get_nom_unique(curseur, nom)
    if compte is not None:
        is_unique = False
    else:
        is_unique = True
    return jsonify(is_unique)




@bp_api.route("/verifNotif")
def verif_nouvelle_notif():

    with bd.creer_curseur() as curseur:
        nouvelle_notif = bd.get_nouvelle_notification(
            curseur, session['id_utilisateur'])

        est_nouvelle = True
        nb_notif = len(nouvelle_notif)
        reponse = {
            "nouvelle": nb_notif > 0,
            "nb_notif": nb_notif,
            "nouvelles_notif": nouvelle_notif
        }
        return reponse
