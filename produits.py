from flask import session, redirect, url_for, render_template
from . import bd, bp_produits


@bp_produits.route('/inventaire', methods=['GET', 'POST'])
def details_produit():
    """Permet d'afficher les produits de l'inventaire pour un utilisateur connecté"""
    if "id_utilisateur" not in session:
        return redirect(url_for("authentification"))

    id_utilisateur = session["id_utilisateur"]

    with bd.creer_curseur() as curseur:
        produits = bd.get_produits_par_utilisateur(curseur, id_utilisateur)

    return render_template('inventaire.jinja',
        produits=produits
    )