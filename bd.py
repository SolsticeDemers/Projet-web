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
        user=os.getenv("BD_UTILISATEUR"),
        password=os.getenv("BD_MDP"),
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
        AND p.archive = FALSE
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
        AND p.archive = FALSE
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
        AND p.archive = FALSE
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
            AND a.paye = TRUE

        GROUP BY
            u.id_utilisateur,
            u.nom

        ORDER BY
            nb_ventes DESC,
            vente_totale DESC

        LIMIT 3
    """)

    return curseur.fetchall()


def get_produits(
    curseur,
    prix_min,
    prix_max,
    limite,
    offset,
    trier_par,
    ordre
):
    """Permet d'obtenir et de trier les produits"""

    if trier_par == "prix":

        if ordre == "DESC":
            tri = "ORDER BY p.prix DESC"

        else:
            tri = "ORDER BY p.prix ASC"

    else:

        if ordre == "DESC":
            tri = "ORDER BY p.nom DESC"

        else:
            tri = "ORDER BY p.nom ASC"


    requete = """
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
        AND s.nom_statut <> 'Vendu'
        AND p.archive = FALSE

        """ + tri + """

        LIMIT %(limite)s OFFSET %(offset)s
    """


    curseur.execute(requete, {
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
    offset,
    trier_par,
    ordre
):
    """Permet de rechercher des produits"""

    if trier_par == "prix":

        if ordre == "DESC":
            tri = "ORDER BY p.prix DESC"

        else:
            tri = "ORDER BY p.prix ASC"

    else:

        if ordre == "DESC":
            tri = "ORDER BY p.nom DESC"

        else:
            tri = "ORDER BY p.nom ASC"


    requete = """
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
            AND s.nom_statut <> 'Vendu'
        )

        AND p.prix BETWEEN %(min)s AND %(max)s
        AND s.nom_statut <> 'Vendu'
        AND p.archive = FALSE

        """ + tri + """

        LIMIT %(limite)s OFFSET %(offset)s
    """


    curseur.execute(requete, {
        "mot_cle": "%" + mot_cle + "%",
        "min": prix_min,
        "max": prix_max,
        "limite": limite,
        "offset": offset
    })

    return curseur.fetchall()

def get_utilisateur(curseur, nom, mdp):
    """Permet d'obtenir un utilisateur avec son nom/courriel et mot de passe"""

    curseur.execute("""
        SELECT
            nom,
            id_utilisateur
        FROM utilisateur
        WHERE (
            courriel = %(nom)s
            OR nom = %(nom)s
        )
        AND mot_de_passe = %(mdp)s
    """, {
        "nom": nom,
        "mdp": mdp
    })

    return curseur.fetchone()


def get_produit(curseur, id_produit):
    """Permet d'obtenir un produit par son identifiant"""

    curseur.execute("""
        SELECT *
        FROM produit WHERE id_produit=%(id_produit)s
             """, {
                 'id_produit': id_produit,
        })
    return curseur.fetchone()

def get_vendeur(curseur, id_utilisateur):
    """Permet d'obtenir un vendeur par son identifiant"""

    curseur.execute("""
        SELECT *
        FROM utilisateur WHERE id_utilisateur=%(id_utilisateur)s
             """, {
                 'id_utilisateur': id_utilisateur,
        })
    return curseur.fetchone()
def inserer_utilisateur_bd(curseur, nom, courriel, mdp):
    """Créer un utilisateur dans la bd"""

    curseur.execute("""
        INSERT INTO utilisateur (
            nom,
            courriel,
            mot_de_passe
        )
        VALUES (
            %(nom)s,
            %(courriel)s,
            %(mdp)s
        )
    """, {
        "nom": nom,
        "courriel": courriel,
        "mdp": mdp
    })

    return curseur.lastrowid

def get_nom_unique(curseur, nom):
    """Vérifie l'existance d'un nom"""

    curseur.execute("""
        SELECT
            id_utilisateur,
            nom
        FROM utilisateur
        WHERE nom = %(nom)s
    """, {
        "nom": nom
    })

    return curseur.fetchone()

def get_courriel_unique(curseur, courriel):
    """Vérifie l'existance d'un courriel"""

    curseur.execute("""
        SELECT
            id_utilisateur,
            courriel
        FROM utilisateur
        WHERE courriel = %(courriel)s
    """, {
        "courriel": courriel
    })

    return curseur.fetchone()

def get_nom_utiliser(curseur):
    """Dictionnaire de nom et courriel déjà utilisé"""

    curseur.execute("""
        SELECT
            id_utilisateur,
            nom,
            courriel
        FROM utilisateur
    """)

    return curseur.fetchall()

def get_produits_par_vendeur(curseur, id_vendeur):
    """Retourne la liste des produits pour un vendeur donné"""

    curseur.execute(
        """
        SELECT
            p.id_produit,
            p.nom,
            p.description,
            p.prix,
            s.nom_statut
        FROM produit p
        JOIN statut_produit s
            ON p.id_statut = s.id_statut
        WHERE p.id_vendeur = %(id_vendeur)s
        AND p.archive = FALSE
        """,
        {
            'id_vendeur': id_vendeur
        }
    )

    return curseur.fetchall()


def get_enchere_future(curseur):
    """Permet d'obtenir les 4 prochains produits mis aux enchères"""
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
        WHERE s.nom_statut = 'Aux enchères' AND NOW() < p.date
        AND p.archive = FALSE
        ORDER BY p.date ASC
        LIMIT 4
    """)

    return curseur.fetchall()


def ajouter_produit(curseur, id_vendeur, nom, description, prix, id_statut):
    """Ajouter un produit dans la bd"""
    curseur.execute("INSERT INTO produit (id_vendeur, nom, description, prix, id_statut, date) "
                    "VALUES(%(id_vendeur)s, %(nom)s, %(description)s, %(prix)s, %(id_statut)s, CURDATE());", {
                        'id_vendeur': id_vendeur,
                        'nom': nom,
                        'description': description,
                        'prix': prix,
                        'id_statut': id_statut
                    })
    return curseur.lastrowid

def get_statuts(curseur):
    """Retourne tous les statuts de produit"""
    curseur.execute("SELECT id_statut, nom_statut FROM statut_produit")
    return curseur.fetchall()

def get_statut_by_Id(curseur, id):
    """Retourne le nom du statut de produit"""
    curseur.execute("SELECT nom_statut FROM statut_produit WHERE id_statut = %(id)s;",
                        {
                            'id' : id
                        })
    return curseur.fetchone()

def archiver_produit(curseur, id_produit):
    """Archive un produit"""

    curseur.execute(
        """
        UPDATE produit
        SET archive = TRUE
        WHERE id_produit = %(id_produit)s
        """,
        {
            "id_produit": id_produit
        }
    )


def ajouter_au_panier(curseur, id_acheteur, id_produit):
    """Permet d'ajouter un produit au panier"""
    curseur.execute(
        "INSERT IGNORE INTO achat "
        "(id_produit, id_acheteur, prix_achat, date_achat, paye) "
        "SELECT id_produit, %(id_acheteur)s, prix, CURDATE(), FALSE "
        "FROM produit WHERE id_produit = %(id_produit)s",
        {
            "id_acheteur": id_acheteur,
            "id_produit": id_produit
        }
    )

def supprimer_du_panier(curseur, id_acheteur, id_produit):
    """Permet de retirer un produit du panier"""
    curseur.execute(
        "DELETE FROM achat " \
        "WHERE id_acheteur = %(id_acheteur)s "
        "AND id_produit = %(id_produit)s " \
        "AND paye = FALSE",
        {
            "id_acheteur": id_acheteur,
            "id_produit": id_produit
        }
    )

def get_panier(curseur, id_acheteur):
    """Permet de retourner les produits dans le panier"""
    curseur.execute("""
        SELECT p.id_produit, p.description, p.nom, p.prix, p.archive, p.id_statut
        FROM achat a
        JOIN produit p ON a.id_produit = p.id_produit
        WHERE a.id_acheteur = %(id_acheteur)s
        AND a.paye = FALSE""",
        {
            "id_acheteur": id_acheteur
        })
    return curseur.fetchall()

def confirmer_achat(curseur, id_acheteur, id_produit, prix):
    """Permet de confirmer l'achat d'un produit du panier"""
    curseur.execute(
        "UPDATE achat SET paye = TRUE, prix_achat = %(prix)s, "
        "date_achat = CURDATE() "
        "WHERE id_acheteur = %(id_acheteur)s " \
        "AND id_produit = %(id_produit)s " \
        "AND paye = FALSE",
        {
            "id_acheteur": id_acheteur,
            "id_produit": id_produit,
            "prix": prix
        }
    )

def marquer_vendu(curseur, id_produit):
    """Change le statut du produit pour Vendu"""
    curseur.execute(
        "UPDATE produit SET id_statut = 4 "
        "WHERE id_produit = %(id_produit)s",
        {
            "id_produit": id_produit
        }
    )

def get_nb_articles_panier(curseur, id_acheteur):
    """Permet de compter les produits dans le panier"""
    curseur.execute(
        "SELECT COUNT(*) AS nb FROM achat "
        "WHERE id_acheteur = %(id_acheteur)s "
        "AND paye = FALSE",
        {
            "id_acheteur": id_acheteur
        }
    )
    return curseur.fetchone()["nb"]


def modifier_produit(curseur, id_produit, nom, description, prix, id_statut):
    """Modifier un produit dans la bd"""
    curseur.execute(
        "UPDATE produit SET nom = %(nom)s, description = %(description)s, "
        "prix = %(prix)s, id_statut = %(id_statut)s "
        "WHERE id_produit = %(id_produit)s",
        {
            "id_produit": id_produit,
            "nom": nom,
            "description": description,
            "prix": prix,
            "id_statut": id_statut
        }
    )


def get_notification(curseur, id_utilisateur):
    curseur.execute("SELECT * FROM notification WHERE id_destinataire = %(id_utilisateur)s;",
                    {
                        'id_utilisateur' : id_utilisateur
                    })
    return curseur.fetchall()

def get_utilisateur_name(curseur, id):
    curseur.execute("SELECT nom FROM utilisateur WHERE id_utilisateur = %(id)s;",
                    {
                        'id' : id
                    })
    return curseur.fetchone()

def get_produit_by_id(curseur, id):
    curseur.execute("SELECT * FROM produit WHERE id_produit = %(id)s;",
                    {
                        'id' : id
                    })
    return curseur.fetchall()

def update_offer(curseur, id_proposition, approuve):
    curseur.execute("UPDATE `echange` SET `approuver`= %(approuve)s WHERE id_echange = %(id)s;",
                    {
                        'id' : id_proposition,
                        'approuve' : approuve
                    })


def create_notif_offrant(curseur, id):
    curseur.execute("INSERT INTO `notification`( `id_destinataire`, `id_statut`, `notif_vue`, `date`)" \
    " VALUES ((SELECT e.id_utilisateur FROM notification_echange n JOIN echange e ON n.id_echange = e.id_echange WHERE e.id_echange = %(id)s)" \
    ", 3 , 0, CURRENT_DATE);",{
        'id' : id
    })
    return curseur.lastrowid

def create_notif_echange(curseur, id_echange, id_notification):
    curseur.execute("INSERT INTO `notification_echange` (`id_notification`, `id_echange`) VALUES (%(id_notification)s, %(id_echange)s);",{
        'id_notification' : id_notification,
        'id_echange' : id_echange
    })



def get_notif_echange(curseur, id):

    curseur.execute("""
        SELECT
        e.*
        FROM notification n
        JOIN notification_echange j
            ON n.id_notification = j.id_notification
        JOIN echange e
            ON j.id_echange = e.id_echange
        WHERE n.id_notification =  %(id)s
    """,
        {
            'id' : id
        })
    return curseur.fetchone()

def get_nouvelle_notification(curseur, id_utilisateur):
    curseur.execute("SELECT * FROM notification WHERE id_destinataire = %(id_utilisateur)s and notif_vue = 0;",
                    {
                        'id_utilisateur' : id_utilisateur
                    })
    return curseur.fetchall()

def update_notification(curseur, id_proposition, vue):
    curseur.execute("UPDATE `notification` SET `notif_vue`= %(vue)s WHERE id_notification = %(id)s;",
                    {
                        'id' : id_proposition,
                        'vue' : vue
                    })
 
