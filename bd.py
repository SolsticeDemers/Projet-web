"""
Connexion à la BD
"""

import os
import contextlib
import mysql.connector


@contextlib.contextmanager
def _creer_connexion():
    """Pour créer une connexion à la BD"""
    conn = mysql.connector.connect(
        user = os.getenv("BD_UTILISATEUR"),
        password= os.getenv("BD_MDP"),
        host=os.getenv("BD_SERVEUR"),
        database=os.getenv("BD_NOM_SCHEMA"),
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
        curseur = connexion.cursor(dictionary=True, buffered=True)
        try:
            yield curseur
        finally:
            curseur.close()

def get_utilisateur(curseur, nom, mdp):
    curseur.execute("SELECT nom, id_utilisateur FROM utilisateur "
                    "WHERE  (courriel = %(nom)s OR nom=%(nom)s) AND mot_de_passe=%(mdp)s;",
                    {
                        'nom': nom,
                        'mdp': mdp
                    })
    return curseur.fetchone()

def inserer_utilisateur_bd(curseur, nom, courriel, mdp):
    """Créer un utilisateur dans la bd"""
    curseur.execute("INSERT INTO utilisateur (nom, courriel, mdp )"
                    "VALUES(%(nom)s, %(courriel)s, %(mdp)s);", {
                        'nom': nom,
                        'courriel': courriel,
                        'mdp': mdp,
                    })
    return curseur.lastrowid
