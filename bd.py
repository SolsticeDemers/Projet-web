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
                        'id': id
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
        "INSERT INTO achat "
        "(id_produit, id_acheteur, prix_achat, date_achat, paye) "
        "SELECT id_produit, %(id_acheteur)s, prix, CURDATE(), FALSE "
        "FROM produit WHERE id_produit = %(id_produit)s",
        {
            "id_acheteur": id_acheteur,
            "id_produit": id_produit
        }
    )

def get_produit_pour_panier(curseur, id_produit):
    curseur.execute("""
        SELECT *
        FROM produit
        WHERE id_produit = %(id_produit)s
        FOR UPDATE
    """, {
        "id_produit": id_produit
    })

    return curseur.fetchone()


def get_achat_par_produit(curseur, id_produit):
    curseur.execute("""
        SELECT id_acheteur, paye
        FROM achat
        WHERE id_produit = %(id_produit)s
        FOR UPDATE
    """, {
        "id_produit": id_produit
    })

    return curseur.fetchone()


def supprimer_du_panier(curseur, id_acheteur, id_produit):
    """Permet de retirer un produit du panier"""
    curseur.execute(
        "DELETE FROM achat "
        "WHERE id_acheteur = %(id_acheteur)s "
        "AND id_produit = %(id_produit)s "
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
        "WHERE id_acheteur = %(id_acheteur)s "
        "AND id_produit = %(id_produit)s "
        "AND paye = FALSE",
        {
            "id_acheteur": id_acheteur,
            "id_produit": id_produit,
            "prix": prix
        }
    )
    return curseur.rowcount


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


def modifier_utilisateur(curseur, id_utilisateur, nom, courriel):
    """Met à jour le nom et le courriel d'un utilisateur."""

    curseur.execute("""
        UPDATE utilisateur
        SET nom = %(nom)s,
            courriel = %(courriel)s
        WHERE id_utilisateur = %(id_utilisateur)s
    """, {
        "id_utilisateur": id_utilisateur,
        "nom": nom,
        "courriel": courriel
    })


def modifier_mot_de_passe(curseur, id_utilisateur, mot_de_passe):
    """Enregistre le nouveau mot de passe haché."""

    curseur.execute("""
        UPDATE utilisateur
        SET mot_de_passe = %(mot_de_passe)s
        WHERE id_utilisateur = %(id_utilisateur)s
    """, {
        "id_utilisateur": id_utilisateur,
        "mot_de_passe": mot_de_passe
    })


def get_notification(curseur, id_utilisateur):
    curseur.execute("""
        SELECT *
        FROM notification
        WHERE id_destinataire = %(id_utilisateur)s
          AND (
              notif_vue = 0
              OR date_lecture > DATE_SUB(NOW(), INTERVAL 15 DAY)
          )
        ORDER BY date DESC""",
        {
            "id_utilisateur": id_utilisateur
        })

    return curseur.fetchall()


def get_utilisateur_name(curseur, id):
    curseur.execute("SELECT nom FROM utilisateur WHERE id_utilisateur = %(id)s;",
                    {
                        'id': id
                    })
    return curseur.fetchone()


def get_produit_by_id(curseur, id):
    curseur.execute("SELECT * FROM produit WHERE id_produit = %(id)s;",
                    {
                        'id': id
                    })
    return curseur.fetchall()


def update_offer(curseur, id_proposition, approuve):
    curseur.execute("UPDATE `echange` SET `approuver`= %(approuve)s WHERE id_echange = %(id)s;",
                    {
                        'id': id_proposition,
                        'approuve': approuve
                    })


def create_notif_offrant(curseur, id):
    curseur.execute("INSERT INTO `notification`( `id_destinataire`, `id_statut`, `notif_vue`, `date`)"
                    " VALUES ((SELECT e.id_utilisateur FROM notification_echange n JOIN echange e ON n.id_echange = e.id_echange WHERE e.id_echange = %(id)s)"
                    ", 3 , 0, CURRENT_DATE);", {
                        'id': id
                    })
    return curseur.lastrowid


def create_notif_echange(curseur, id_echange, id_notification):
    curseur.execute("INSERT INTO `notification_echange` (`id_notification`, `id_echange`) VALUES (%(id_notification)s, %(id_echange)s);", {
        'id_notification': id_notification,
        'id_echange': id_echange
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
                        'id': id
                    })
    return curseur.fetchone()


def get_nouvelle_notification(curseur, id_utilisateur):
    curseur.execute("SELECT * FROM notification WHERE id_destinataire = %(id_utilisateur)s and notif_vue = 0;",
                    {
                        'id_utilisateur': id_utilisateur
                    })
    return curseur.fetchall()


def update_notification(curseur, id_proposition, vue):
    curseur.execute("""
        UPDATE notification
        SET notif_vue = %(vue)s, date_lecture = NOW()
        WHERE id_notification = %(id)s
          AND notif_vue = 0""",
          {
            "id": id_proposition,
            "vue": vue
        })


def get_achat_paye(curseur, id_acheteur, id_produit):
    """Trouver l'achat payé et le vendeur qui lui correspond"""
    curseur.execute("""
        SELECT a.id_achat, p.id_vendeur
        FROM achat a
        JOIN produit p ON p.id_produit = a.id_produit
        WHERE a.id_acheteur = %(id_acheteur)s
          AND a.id_produit = %(id_produit)s
          AND a.paye = TRUE
    """, {
        "id_acheteur": id_acheteur,
        "id_produit": id_produit
    })
    return curseur.fetchone()


def creer_notification_achat(curseur, id_vendeur):
    """Créer une notification pour le vendeur que son produit est vendu"""

    curseur.execute("""INSERT INTO notification
        (
            id_destinataire, id_statut, notif_vue, date
        )
        VALUES (%(id_vendeur)s, 1, 0, CURRENT_DATE)""",
                    {
                        "id_vendeur": id_vendeur
                    }
                    )

    return curseur.lastrowid


def lier_notification_achat(curseur, id_notification, id_achat):
    """Permet de lier une notification à un achat"""

    curseur.execute("INSERT INTO notification_achat (id_notification, id_achat) "
                    "VALUES (%(id_notification)s, %(id_achat)s)",
                    {
                        'id_notification': id_notification,
                        'id_achat': id_achat
                    })


def get_notifications_achat(curseur, id_utilisateur):
    """Retourne les notifications de vente non lues."""

    curseur.execute("""SELECT
            n.id_notification,
            p.id_produit,
            p.nom AS nom_produit,
            a.prix_achat,
            u.id_utilisateur AS id_acheteur,
            u.nom AS nom_acheteur
        FROM notification n

        JOIN notification_achat na
        ON na.id_notification = n.id_notification
        JOIN achat a
        ON a.id_achat = na.id_achat
        JOIN produit p
        ON p.id_produit = a.id_produit
        JOIN utilisateur u
        ON u.id_utilisateur = a.id_acheteur

        WHERE n.id_destinataire = %(id_utilisateur)s
        AND (n.notif_vue = 0 OR n.date_lecture > DATE_SUB(NOW(), INTERVAL 15 DAY)
)
        ORDER BY n.date DESC""",
                    {
                        "id_utilisateur": id_utilisateur
                    }
                    )

    return curseur.fetchall()


def ajouter_mise(curseur, id_produit, id_utilisateur, montant):
    """Enregistre une mise"""

    curseur.execute("""
        INSERT INTO mise (
            id_produit,
            id_utilisateur,
            montant
        )
        VALUES (
            %(id_produit)s,
            %(id_utilisateur)s,
            %(montant)s
        )
    """, {
        "id_produit": id_produit,
        "id_utilisateur": id_utilisateur,
        "montant": montant
    })


def modifier_prix_produit(curseur, id_produit, nouveau_prix):
    """Modifie le prix actuel d'un produit"""

    curseur.execute("""
        UPDATE produit
        SET prix = %(nouveau_prix)s
        WHERE id_produit = %(id_produit)s
    """, {
        "nouveau_prix": nouveau_prix,
        "id_produit": id_produit
    })


def get_mise_gagnante(curseur, id_produit):
    """Retourne la mise la plus élevée pour un produit"""

    curseur.execute("""
        SELECT *
        FROM mise
        WHERE id_produit = %(id_produit)s
        ORDER BY montant DESC
        LIMIT 1
    """, {
        "id_produit": id_produit
    })

    return curseur.fetchone()


def get_encheres_terminees(curseur):
    """Retourne les enchères dont la date de fin est dépassée"""

    curseur.execute("""
        SELECT *
        FROM produit
        WHERE id_statut = 2
        AND date_fin IS NOT NULL
        AND date_fin <= NOW()
    """)

    return curseur.fetchall()


def get_encheres_utilisateur(curseur, id_utilisateur):
    """Retourne les enchères en cours sur lesquelles l'utilisateur a misé"""

    curseur.execute("""
        SELECT DISTINCT
            p.*
        FROM mise m
        JOIN produit p
            ON m.id_produit = p.id_produit
        WHERE m.id_utilisateur = %(id_utilisateur)s
        AND p.id_statut = 2
        AND p.date_fin IS NOT NULL
        AND p.date_fin > NOW()
        ORDER BY p.date_fin ASC
    """, {
        "id_utilisateur": id_utilisateur
    })

    return curseur.fetchall()


def create_notif_gagnant(curseur, id_utilisateur):
    """Crée une notification pour le gagnant d'une enchère"""

    curseur.execute("""
        INSERT INTO notification (
            id_destinataire,
            id_statut,
            notif_vue,
            date
        )
        VALUES (
            %(id_utilisateur)s,
            2,
            0,
            CURRENT_DATE
        )
    """, {
        "id_utilisateur": id_utilisateur
    })

    return curseur.lastrowid


def create_notif_enchere(curseur, id_notification, id_produit):
    """Relie une notification à une enchère"""

    curseur.execute("""
        INSERT INTO notification_enchere (
            id_notification,
            id_produit
        )
        VALUES (
            %(id_notification)s,
            %(id_produit)s
        )
    """, {
        "id_notification": id_notification,
        "id_produit": id_produit
    })


def get_notif_enchere(curseur, id_notification):
    """Retourne le produit associé à une notification d'enchère"""

    curseur.execute("""
        SELECT p.*
        FROM notification_enchere ne
        JOIN produit p
            ON ne.id_produit = p.id_produit
        WHERE ne.id_notification = %(id_notification)s
    """, {
        "id_notification": id_notification
    })

    return curseur.fetchone()


def get_historique_encheres(curseur, id_utilisateur, tri="recent"):
    """Retourne les enchères gagnées par l'utilisateur"""

    if tri == "ancien":
        ordre = "ORDER BY p.date_fin ASC"
    elif tri == "prix_croissant":
        ordre = "ORDER BY p.prix ASC"
    elif tri == "prix_decroissant":
        ordre = "ORDER BY p.prix DESC"
    else:
        ordre = "ORDER BY p.date_fin DESC"

    requete = """
        SELECT
            p.id_produit,
            p.nom,
            p.prix,
            p.date_fin
        FROM notification n
        JOIN notification_enchere ne
            ON n.id_notification = ne.id_notification
        JOIN produit p
            ON ne.id_produit = p.id_produit
        WHERE n.id_destinataire = %(id_utilisateur)s
        AND n.id_statut = 2
    """ + ordre

    curseur.execute(requete, {
        "id_utilisateur": id_utilisateur
    })

    return curseur.fetchall()


def get_historique_achats(curseur, id_utilisateur, tri="recent"):
    """Retourne les achats payés de l'utilisateur"""

    if tri == "ancien":
        ordre = "ORDER BY a.date_achat ASC"
    elif tri == "prix_croissant":
        ordre = "ORDER BY a.prix_achat ASC"
    elif tri == "prix_decroissant":
        ordre = "ORDER BY a.prix_achat DESC"
    else:
        ordre = "ORDER BY a.date_achat DESC"

    requete = """
        SELECT
            p.id_produit,
            p.nom,
            a.prix_achat,
            a.date_achat
        FROM achat a
        JOIN produit p
            ON a.id_produit = p.id_produit
        WHERE a.id_acheteur = %(id_utilisateur)s
        AND a.paye = 1
    """ + ordre

    curseur.execute(requete, {
        "id_utilisateur": id_utilisateur
    })

    return curseur.fetchall()

def get_historique_echanges(curseur, id_utilisateur):
    """Retourne l'historique des échanges"""

    curseur.execute("""
        SELECT
            e.id_echange,
            e.id_utilisateur AS id_offrant,
            e.produit AS id_produit_demande,
            d.nom AS nom_produit_demande,
            e.produit_offert AS id_produit_offert,
            offert.nom AS nom_produit_offert,
            partenaire.nom AS nom_partenaire
        FROM echange e
        JOIN produit d
            ON d.id_produit = e.produit
        LEFT JOIN produit offert
            ON offert.id_produit = e.produit_offert
        JOIN utilisateur partenaire
            ON partenaire.id_utilisateur = CASE
                WHEN e.id_utilisateur = %(id_utilisateur)s THEN e.proprio
                ELSE e.id_utilisateur
            END
        WHERE e.approuver = 1
          AND (
              e.id_utilisateur = %(id_utilisateur)s
              OR e.proprio = %(id_utilisateur)s
          )
        ORDER BY e.id_echange DESC""",
        {
            "id_utilisateur": id_utilisateur
        })

    return curseur.fetchall()
