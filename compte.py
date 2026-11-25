"""
Ce script décrit le blue print Compte
"""
import os
import re
import hashlib

from flask import Blueprint, current_app, render_template, request, redirect, session, abort, url_for
import bd
from forms import ArchiverProduitForm, ModifierProfilForm


regex_courriel = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
)

bp_compte = Blueprint('compte', __name__)


def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(
        mdp_en_clair.encode()
    ).hexdigest()


@bp_compte.route('/authentification', methods=['GET', 'POST'])


def authentification():
    """Formulaire d'authentification"""
    if request.method == 'GET':
        return render_template(
            "compte/authentification.jinja",
            nom_page="Authentification"
        )
    nom = request.form.get("nom", "").strip()
    mdp = request.form.get("mdp", "")
    classe_nom = ""
    classe_mdp = ""
    erreur_nom = ""
    erreur_mdp = ""
    est_valide = True
    if nom == "":
        classe_nom = "is-invalid"
        erreur_nom = "Veuillez entrer votre nom d'utilisateur ou courriel."
        est_valide = False
    if mdp == "":
        classe_mdp = "is-invalid"
        erreur_mdp = "Veuillez entrer votre mot de passe."
        est_valide = False
    # Vérifier si le nom ou le courriel existe
    if nom != "":
        with bd.creer_curseur() as curseur:
            compte_existant = (
                bd.get_nom_unique(curseur, nom)
                or bd.get_courriel_unique(curseur, nom)
            )
        if compte_existant is None:
            classe_nom = "is-invalid"
            erreur_nom = "Ce nom d'utilisateur ou courriel n'existe pas."
            est_valide = False
        else:
            classe_nom = "is-valid"
    # Vérifier le mot de passe si les champs précédents sont valides
    if est_valide:
        with bd.creer_curseur() as curseur:
            utilisateur = bd.get_utilisateur(
                curseur, nom, hacher_mdp(mdp)
            )
        if utilisateur is None:
            classe_mdp = "is-invalid"
            erreur_mdp = "Mot de passe incorrect."
            est_valide = False
    if est_valide:
        session.permanent = True
        session['id_utilisateur'] = utilisateur['id_utilisateur']
        session['nom'] = utilisateur['nom']
        return redirect('/', code=303)
    return render_template(
        "compte/authentification.jinja",
        nom=nom,
        classe_nom=classe_nom,
        classe_mdp=classe_mdp,
        erreur_nom=erreur_nom,
        erreur_mdp=erreur_mdp
    )


@bp_compte.route('/creer_compte', methods=['GET', 'POST'])


def creer_compte():
    """Affiche un formulaire"""
    if request.method == 'GET':
        return render_template(
            "compte/creer_compte.jinja",
            page="Créer un compte"
        )
    nom = request.form.get("nom", "").strip()
    courriel = request.form.get("courriel", "").strip()
    mdp1 = request.form.get("mdp1")
    mdp2 = request.form.get("mdp2")
    classe_nom = ""
    classe_courriel = ""
    classe_mdp1 = ""
    classe_mdp2 = ""
    liste_courriel = []
    liste_nom = []
    erreur = False
    num_nom_erreur = 0
    num_courriel_erreur = 0
    num_mdp_erreur = 0
    image = request.files.get("image")
    erreur_image = None
    if image and image.filename:
        if not image.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            erreur_image = "Choisissez une image PNG ou JPG."
            erreur = True
    with bd.creer_curseur() as curseur:
        dict_compte = bd.get_nom_utiliser(curseur)
    for u in dict_compte:
        liste_courriel.append(
            u['courriel']
        )
    for u in dict_compte:
        liste_nom.append(
            u['nom']
        )
    if nom == "" or nom is None:
        classe_nom = "is-invalid"
        erreur = True
        num_nom_erreur = 1
    elif nom in liste_nom:
        classe_nom = "is-invalid"
        erreur = True
        num_nom_erreur = 2
    else:
        classe_nom = "is-valid"
    if courriel == "" or courriel is None:
        classe_courriel = "is-invalid"
        erreur = True
        num_courriel_erreur = 1
    elif not re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        courriel
    ):
        classe_courriel = "is-invalid"
        erreur = True
        num_courriel_erreur = 2
    elif courriel in liste_courriel:
        classe_courriel = "is-invalid"
        erreur = True
        num_courriel_erreur = 3
    else:
        classe_courriel = "is-valid"
    if mdp1 == "" or mdp1 is None:
        classe_mdp1 = "is-invalid"
        erreur = True
    else:
        classe_mdp1 = "is-valid"
    if mdp2 == "" or mdp2 is None:
        classe_mdp2 = "is-invalid"
        erreur = True
        num_mdp_erreur = 1
    elif mdp2 != mdp1:
        classe_mdp2 = "is-invalid"
        erreur = True
        num_mdp_erreur = 2
    else:
        classe_mdp2 = "is-valid"
    if erreur is True:
        return render_template(
            "compte/creer_compte.jinja",
            page="Créer un compte",
            classe_mdp2=classe_mdp2,
            classe_mdp1=classe_mdp1,
            classe_nom=classe_nom,
            classe_courriel=classe_courriel,
            num_mdp_erreur=num_mdp_erreur,
            num_nom_erreur=num_nom_erreur,
            num_courriel_erreur=num_courriel_erreur,
            nom=nom,
            courriel=courriel,
            mdp1=mdp1,
            mdp2=mdp2,
            erreur_image=erreur_image
        )
    mdp1 = hacher_mdp(mdp1)
    with bd.creer_curseur() as curseur:
        id_util = bd.inserer_utilisateur_bd(
            curseur,
            nom,
            courriel,
            mdp1
        )
    if image and image.filename:
        nom_image = f"vendeur_{id_util}.png"
        chemin_image = os.path.join(
            current_app.config["CHEMIN_IMAGES"],
            nom_image
        )
        image.save(chemin_image)
    session.permanent = True
    session['id_utilisateur'] = id_util
    session['nom'] = nom
    return redirect("/", code=303)


@bp_compte.route('/deconnection')


def deconnection():
    """Détruit la session"""
    session.clear()
    return redirect("/", code=303)


@bp_compte.route("/profil")


def profil():
    """Affiche le profil de l'utilisateur connecté"""
    if "id_utilisateur" not in session:
        return redirect(url_for("compte.authentification"))
    id_utilisateur = session["id_utilisateur"]
    with bd.creer_curseur() as curseur:
        utilisateur = bd.get_vendeur(curseur, id_utilisateur)
        if utilisateur is None:
            abort(404)
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
        nom_image_vendeur = f"vendeur_{id_utilisateur}.png"
        chemin_image_vendeur = os.path.join(
            current_app.config["CHEMIN_IMAGES"],
            nom_image_vendeur
        )
        if os.path.exists(chemin_image_vendeur):
            image_vendeur = (
                current_app.config["ROUTE_IMAGES"] + nom_image_vendeur
            )
        else:
            image_vendeur = url_for(
                "static",
                filename="images/default_user.png"
            )

       

        return render_template(
            'profil.jinja',
            produits=produits,
            form_archiver=form,
            utilisateur=utilisateur,
            image_vendeur=image_vendeur
        )


@bp_compte.route("/modifier_profil", methods=["GET", "POST"])


def modifier_profil():
    """Affiche et modifie le profil de l'utilisateur connecté."""
    if "id_utilisateur" not in session:
        return redirect(url_for("compte.authentification"))
    id_utilisateur = session["id_utilisateur"]
    form = ModifierProfilForm()
    nom_image = f"vendeur_{id_utilisateur}.png"
    chemin_image = os.path.join(
        current_app.config["CHEMIN_IMAGES"],
        nom_image
    )
    if os.path.exists(chemin_image):
        image_vendeur = current_app.config["ROUTE_IMAGES"] + nom_image
    else:
        image_vendeur = url_for("static", filename="images/default_user.png")
    with bd.creer_curseur() as curseur:
        utilisateur = bd.get_vendeur(curseur, id_utilisateur)
        if utilisateur is None:
            abort(404)
        if request.method == "GET":
            form.nom.data = utilisateur["nom"]
            form.courriel.data = utilisateur["courriel"]
        elif form.validate_on_submit():
            erreur = False
            compte_nom = bd.get_nom_unique(curseur, form.nom.data)
            if compte_nom and compte_nom["id_utilisateur"] != id_utilisateur:
                form.nom.errors.append("Ce nom est déjà utilisé.")
                erreur = True
            if not regex_courriel.fullmatch(form.courriel.data):
                form.courriel.errors.append(
                    "Veuillez entrer un courriel valide.")
                erreur = True
            else:
                compte_courriel = bd.get_courriel_unique(
                    curseur,
                    form.courriel.data
                )
                if (compte_courriel and compte_courriel["id_utilisateur"] != id_utilisateur):
                    form.courriel.errors.append(
                        "Ce courriel est déjà utilisé.")
                    erreur = True
            mdp_actuel = form.mdp_actuel.data or ""
            nouveau_mdp = form.mdp1.data or ""
            confirmation_mdp = form.mdp2.data or ""
            # Si les trois champs sont vides, le mot de passe ne change pas.
            if mdp_actuel or nouveau_mdp or confirmation_mdp:
                if not mdp_actuel:
                    form.mdp_actuel.errors.append(
                        "Veuillez entrer votre mot de passe actuel.")
                    erreur = True
                elif hacher_mdp(mdp_actuel) != utilisateur["mot_de_passe"]:
                    form.mdp_actuel.errors.append(
                        "Le mot de passe actuel est incorrect.")
                    erreur = True
                if not nouveau_mdp:
                    form.mdp1.errors.append(
                        "Veuillez entrer un nouveau mot de passe.")
                    erreur = True
                if nouveau_mdp != confirmation_mdp:
                    form.mdp2.errors.append(
                        "Les nouveaux mots de passe ne correspondent pas.")
                    erreur = True
            if not erreur:
                bd.modifier_utilisateur(
                    curseur,
                    id_utilisateur,
                    form.nom.data,
                    form.courriel.data
                )
                if nouveau_mdp:
                    bd.modifier_mot_de_passe(
                        curseur,
                        id_utilisateur,
                        hacher_mdp(nouveau_mdp)
                    )
                if form.image.data:
                    form.image.data.save(chemin_image)
                session["nom"] = form.nom.data
                return redirect(url_for("compte.profil"), code=303)
    return render_template(
        "compte/modifier_profil.jinja",
        form=form,
        image_vendeur=image_vendeur
    )


@bp_compte.route("/profil/<int:id_utilisateur>")
def profil_public(id_utilisateur):
    """Affiche le profil public d'un vendeur."""

    with bd.creer_curseur() as curseur:
        utilisateur = bd.get_vendeur(curseur, id_utilisateur)

        if utilisateur is None:
            abort(404)

        produits = bd.get_produits_par_vendeur(curseur, id_utilisateur)

    codes_statut = {
        "En vente": "vente",
        "Aux enchères": "enchere",
        "À échanger": "echange",
        "Vendu": "vendu"
    }

    for produit in produits:
        produit["code_statut"] = codes_statut.get(produit["nom_statut"], "")

        nom_image = f"produit_{produit['id_produit']}.png"
        chemin_image = os.path.join(
            current_app.config["CHEMIN_IMAGES"],
            nom_image
        )

        if os.path.exists(chemin_image):
            produit["src"] = current_app.config["ROUTE_IMAGES"] + nom_image
        else:
            produit["src"] = url_for("static", filename="images/default.png")

    nom_image_vendeur = f"vendeur_{id_utilisateur}.png"
    chemin_image_vendeur = os.path.join(
        current_app.config["CHEMIN_IMAGES"],
        nom_image_vendeur
    )

    if os.path.exists(chemin_image_vendeur):
        image_vendeur = current_app.config["ROUTE_IMAGES"] + nom_image_vendeur
    else:
        image_vendeur = url_for("static", filename="images/default_user.png")

    return render_template(
        "profil_public.jinja",
        utilisateur=utilisateur,
        produits=produits,
        image_vendeur=image_vendeur
    )