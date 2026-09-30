import os

from flask import Flask, render_template, request
import bd
from compte import bp_compte


app = Flask(__name__, static_url_path='')
app.register_blueprint(bp_compte, url_prefix='/compte')
app.secret_key = os.getenv("SECRET_SESSION")

app.config["ROUTE_IMAGES"] = "/css/images/utiles/"

app.config["CHEMIN_IMAGES"] = os.path.join(
    app.root_path,
    "static",
    "css",
    "images",
    "utiles"
)


@app.route("/")
def index():
    """Affiche la page d'accueil"""

    with bd.creer_curseur() as curseur:

        nouveaux_produits = bd.get_nouveaux_produits(curseur)

        vendeurs = bd.get_utilisateurs_populaires(curseur)

        produit_du_jour = bd.get_produit_aleatoire(curseur)

        produits_aleatoires = bd.get_produits_aleatoires(curseur)


    for produit in nouveaux_produits:

        produit["src"] = None

        nom_image = (
            "produit_"
            + str(produit["id_produit"])
            + ".png"
        )

        chemin_image = os.path.join(
            app.config["CHEMIN_IMAGES"],
            nom_image
        )

        if os.path.exists(chemin_image):

            produit["src"] = (
                app.config["ROUTE_IMAGES"]
                + nom_image
            )


    for produit in produits_aleatoires:

        produit["src"] = None

        nom_image = (
            "produit_"
            + str(produit["id_produit"])
            + ".png"
        )

        chemin_image = os.path.join(
            app.config["CHEMIN_IMAGES"],
            nom_image
        )

        if os.path.exists(chemin_image):

            produit["src"] = (
                app.config["ROUTE_IMAGES"]
                + nom_image
            )


    if produit_du_jour is not None:

        produit_du_jour["src"] = None

        nom_image = (
            "produit_"
            + str(produit_du_jour["id_produit"])
            + ".png"
        )

        chemin_image = os.path.join(
            app.config["CHEMIN_IMAGES"],
            nom_image
        )

        if os.path.exists(chemin_image):

            produit_du_jour["src"] = (
                app.config["ROUTE_IMAGES"]
                + nom_image
            )

    return render_template(
        "index.jinja",
        titre="Accueil",
        nouveaux_produits=nouveaux_produits,
        vendeurs=vendeurs,
        produit_du_jour=produit_du_jour,
        produits_aleatoires=produits_aleatoires
    )


@app.route("/produits/recherche")
def recherche_produits():
    """Permet de rechercher plusieurs produits"""

    mot_cle = request.args.get("mot_cle", "")

    prix_min = request.args.get(
        "prix_min",
        type=float
    )

    prix_max = request.args.get(
        "prix_max",
        type=float
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )


    if page is None or page < 1:
        page = 1


    if prix_min is None:
        prix_min = 0


    if prix_max is None:
        prix_max = 999999999


    limite = 12

    offset = (page - 1) * limite


    with bd.creer_curseur() as curseur:

        if not mot_cle:

            produits = bd.get_produits(
                curseur,
                prix_min,
                prix_max,
                limite,
                offset
            )

            if produits is None:
                produits = []

            produits = produits[
                offset:offset + limite
            ]

        else:

            produits = bd.get_produits_recherche_filtre(
                curseur,
                mot_cle,
                prix_min,
                prix_max,
                limite,
                offset
            )

            if produits is None:
                produits = []


    for produit in produits:

        produit["src"] = None

        nom_image = (
            "produit_"
            + str(produit["id_produit"])
            + ".png"
        )

        chemin_image = os.path.join(
            app.config["CHEMIN_IMAGES"],
            nom_image
        )

        if os.path.exists(chemin_image):

            produit["src"] = (
                app.config["ROUTE_IMAGES"]
                + nom_image
            )


    return render_template(
        "recherche.jinja",
        titre="Recherche de produits",
        produits=produits,
        mot_cle=mot_cle,
        prix_min=prix_min,
        prix_max=prix_max,
        page=page,
        limite=limite
    )


@app.errorhandler(400)
def erreur_400(e):
    return render_template(
        "erreur.jinja",
        titre="Erreur 400",
        code=400,
        message="La requête est invalide"
    ), 400


@app.errorhandler(401)
def erreur_401(e):
    return render_template(
        "erreur.jinja",
        titre="Erreur 401",
        code=401,
        message="Vous devez être connecté pour accéder à cette page"
    ), 401


@app.errorhandler(403)
def erreur_403(e):
    return render_template(
        "erreur.jinja",
        titre="Erreur 403",
        code=403,
        message="Vous n'avez pas accès à cette page"
    ), 403


@app.errorhandler(404)
def erreur_404(e):
    return render_template(
        "erreur.jinja",
        titre="Erreur 404",
        code=404,
        message="La page demandée n'existe pas"
    ), 404


@app.errorhandler(500)
def erreur_500(e):
    return render_template(
        "erreur.jinja",
        titre="Erreur 500",
        code=500,
        message="Le serveur a rencontré une erreur"
    ), 500


if __name__ == "__main__":
    app.run(debug=True)