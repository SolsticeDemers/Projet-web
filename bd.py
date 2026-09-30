def get_produits_par_vendeur(curseur, id_vendeur):
    """Retourne la liste des produits pour un vendeur donné"""
    curseur.execute(
        "SELECT * FROM produits WHERE id_vendeur = %s",
        (id_vendeur,)
    )
    return curseur.fetchall()