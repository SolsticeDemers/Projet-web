
def get_produit(curseur, id):
    """Permet d'obtenir un produit par son identifiant"""
    curseur.execute("""
        SELECT *
        FROM produit WHERE id_produit=%(id)s
             """, {
                 'id': id,
        })
    return curseur.fetchone()


def get_vendeur(curseur, id_vendeur):
    """Permet d'obtenir un vendeur par son identifiant"""
    curseur.execute("""
        SELECT *
        FROM vendeur WHERE id_vendeur=%(id_vendeur)s
             """, {
                 'id_vendeur': id_vendeur,
        })
    return curseur.fetchone()

