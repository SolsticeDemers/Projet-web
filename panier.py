from flask import Blueprint, abort, redirect, render_template, request, session, url_for
import bd
import os
from flask import current_app
from forms import PanierForm

bp_panier = Blueprint("panier", __name__)


@bp_panier.route("/")
def voir_panier():
    """Affiche le panier de l'utilisateur connecté"""
    if "id_utilisateur" not in session:
        abort(401)

    achat_reussi = request.args.get("achat") == "ok"

    with bd.creer_curseur() as curseur:
        produits = bd.get_panier(curseur, session["id_utilisateur"])

    total = 0
    est_indisponible = False

    for p in produits:
        nom_image = "produit_" + str(p["id_produit"]) + ".png"
        chemin_image = os.path.join(
            current_app.config["CHEMIN_IMAGES"], nom_image)

        if os.path.exists(chemin_image):
            p["src"] = current_app.config["ROUTE_IMAGES"] + nom_image
        else:
            p["src"] = "/images/default.png"

        if p["archive"] == False and p["id_statut"] != 4:
            total = total + p["prix"]
        else:
            est_indisponible = True

    return render_template("panier.jinja", produits=produits, total=total,
                           est_indisponible=est_indisponible, form=PanierForm(), achat_reussi=achat_reussi)


@bp_panier.route("/ajouter/<int:id>", methods=["POST"])
def ajouter(id):
    """Ajoute un produit au panier"""
    if "id_utilisateur" not in session:
        abort(401)
    if not PanierForm().validate_on_submit():
        abort(400)

    with bd.creer_curseur() as curseur:
        produit = bd.get_produit_pour_panier(curseur, id)

        if produit is None or produit["archive"] or produit["id_statut"] == 4:
            abort(404)

        if produit["id_vendeur"] == session["id_utilisateur"]:
            abort(403)

        achat = bd.get_achat_par_produit(curseur, id)

        if achat is None:
            bd.ajouter_au_panier(curseur, session["id_utilisateur"], id)

        elif achat["id_acheteur"] != session["id_utilisateur"] or achat["paye"]:
            abort(409, "Ce produit n'est plus disponible.")

    return redirect(url_for("panier.voir_panier"))


@bp_panier.route("/retirer/<int:id>", methods=["POST"])
def retirer(id):
    """Retire un produit du panier"""
    if "id_utilisateur" not in session:
        abort(401)
    if not PanierForm().validate_on_submit():
        abort(400)

    with bd.creer_curseur() as curseur:
        bd.supprimer_du_panier(curseur, session["id_utilisateur"], id)

    return redirect(url_for("panier.voir_panier"))


@bp_panier.route("/confirmer", methods=["POST"])
def confirmer():
    """Enregistre l'achat des produits du panier"""
    if "id_utilisateur" not in session:
        abort(401)
    if not PanierForm().validate_on_submit():
        abort(400)

    id_acheteur = session["id_utilisateur"]

    with bd.creer_curseur() as curseur:
        produits = bd.get_panier(curseur, id_acheteur)

        if len(produits) == 0:
            return redirect(url_for("panier.voir_panier"))

        for p in produits:
            if p["archive"] == True or p["id_statut"] == 4:
                return redirect(url_for("panier.voir_panier"))

        for p in produits:
            nb_achats = bd.confirmer_achat(
                curseur, id_acheteur, p["id_produit"], p["prix"]
            )

            if nb_achats != 1:
                abort(409, "Cet achat a déjà été confirmé ou n'est plus disponible.")

            bd.marquer_vendu(curseur, p["id_produit"])

            achat = bd.get_achat_paye(
                curseur, id_acheteur, p["id_produit"]
            )

            if achat is None:
                abort(409, "Impossible de trouver l'achat confirmé.")

            id_notification = bd.creer_notification_achat(
                curseur, achat["id_vendeur"]
            )

            bd.lier_notification_achat(
                curseur, id_notification, achat["id_achat"]
            )

    return redirect(url_for("panier.voir_panier", achat="ok"))
