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

        curseur = connexion.cursor(
            dictionary=True,
            buffered=True
        )

        try:
            yield curseur

        finally:
            curseur.close()


def get_nouveaux_produits(curseur):
    """Permet d'obtenir les 4 produits les plus récents"""

    curseur.execute("""
        SELECT
            p.id_produit,
            p.nom,
            p.description,
            p.prix,
            p.date,
            s.nom_statut
        FROM produit p
        JOIN statut_produit s
            ON p.id_statut = s.id_statut
        WHERE s.nom_statut <> 'Vendu'
        ORDER BY p.date DESC
        LIMIT 4
    """)

    return curseur.fetchall()


def get_produit_aleatoire(curseur):
    """Permet d'obtenir un produit au hasard"""

    curseur.execute("""
        SELECT
            p.id_produit,
            p.nom,
            p.description,
            p.prix,
            p.date,
            s.nom_statut
        FROM produit p
        JOIN statut_produit s
            ON p.id_statut = s.id_statut
        WHERE s.nom_statut <> 'Vendu'
        ORDER BY RAND()
        LIMIT 1
    """)

    return curseur.fetchone()


def get_produits_aleatoires(curseur):
    """Permet d'obtenir 4 produits au hasard"""

    curseur.execute("""
        SELECT
            p.id_produit,
            p.nom,
            p.description,
            p.prix,
            p.date,
            s.nom_statut
        FROM produit p
        JOIN statut_produit s
            ON p.id_statut = s.id_statut
        WHERE s.nom_statut <> 'Vendu'
        ORDER BY RAND()
        LIMIT 4
    """)

    return curseur.fetchall()
def get_utilisateurs_populaires(curseur):
    """Retourne les 3 vendeurs les plus populaires"""

    curseur.execute("""
        SELECT
            u.id_utilisateur,
            u.nom,
            COUNT(a.id_achat) AS nb_ventes,
            COALESCE(SUM(a.prix_achat), 0) AS vente_totale

        FROM utilisateur u

        LEFT JOIN produit p
            ON u.id_utilisateur = p.id_vendeur

        LEFT JOIN achat a
            ON p.id_produit = a.id_produit

        GROUP BY
            u.id_utilisateur,
            u.nom

        ORDER BY
            nb_ventes DESC,
            vente_totale DESC

        LIMIT 3
    """)

    return curseur.fetchall()

def get_produits(curseur, prix_min, prix_max, limite, offset):
    """Permet d'obtenir tous les produits"""

    curseur.execute("""
        SELECT
            p.id_produit,
            p.nom,
            p.description,
            p.prix,
            p.date,
            s.nom_statut

        FROM produit p

        JOIN statut_produit s
            ON p.id_statut = s.id_statut

        WHERE p.prix BETWEEN %(min)s AND %(max)s

        ORDER BY p.nom ASC

        LIMIT %(limite)s OFFSET %(offset)s
    """, {
        "min": prix_min,
        "max": prix_max,
        "limite": limite,
        "offset": offset
    })

    return curseur.fetchall()


def get_produits_recherche_filtre(
    curseur,
    mot_cle,
    prix_min,
    prix_max,
    limite,
    offset
):
    """Permet de rechercher des produits"""

    curseur.execute("""
        SELECT
            p.id_produit,
            p.nom,
            p.description,
            p.prix,
            p.date,
            s.nom_statut

        FROM produit p

        JOIN statut_produit s
            ON p.id_statut = s.id_statut

        WHERE (
            p.nom LIKE %(mot_cle)s
            OR p.description LIKE %(mot_cle)s
        )

        AND p.prix BETWEEN %(min)s AND %(max)s

        ORDER BY p.nom ASC

        LIMIT %(limite)s OFFSET %(offset)s
    """, {
        "mot_cle": "%" + mot_cle + "%",
        "min": prix_min,
        "max": prix_max,
        "limite": limite,
        "offset": offset
    })

    return curseur.fetchall()

def get_utilisateur(curseur, nom, mdp):
    curseur.execute("SELECT nom, id_utilisateur FROM utilisateur "
                    "WHERE  (courriel = %(nom)s OR nom=%(nom)s) AND mot_de_passe=%(mdp)s;",
                    {
                        'nom': nom,
                        'mdp': mdp
                    })
    return curseur.fetchone()
