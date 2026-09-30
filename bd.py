"""
Connexion à la BD
"""

import contextlib
import mysql.connector


@contextlib.contextmanager
def _creer_connexion():
    """Pour créer une connexion à la BD"""

    conn = mysql.connector.connect(
        user="42005c",
        password="qwerty123",
        host="127.0.0.1",
        database="vintagemarket",
        raise_on_warnings=True
    )

    try:
        yield conn

    except Exception:
        conn.rollback()
        raise

    else:
        conn.commit()

    finally:
        conn.close()


@contextlib.contextmanager
def creer_curseur():
    """Permet d'avoir les enregistrements dans un dictionnaire"""

    with _creer_connexion() as connexion:

        curseur = connexion.cursor(
            dictionary=True,
            buffered=True
        )

        try:
            yield curseur

        finally:
            curseur.close()

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

