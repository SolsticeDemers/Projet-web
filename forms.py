from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, PasswordField
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Optional, NumberRange, Length


class AjouterProduitForm(FlaskForm):
    nom = StringField(
        "Nom",
        validators=[
            DataRequired(message="Le nom du produit est obligatoire."),
            Length(max=150, message="Le nom ne peut pas dépasser 150 caractères.")
        ]
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired(message="La description est obligatoire.")]
    )
    prix = DecimalField(
        "Prix",
        validators=[
            InputRequired(message="Le prix est obligatoire."),
            NumberRange(min=0, message="Le prix ne peut pas être négatif.")
        ]
    )
    id_statut = RadioField(
        "Statut",
        coerce=int,
        validators=[InputRequired(message="Veuillez choisir un statut.")]
    )
    image = FileField(
        "Image du produit",
        validators=[
            Optional(),
            FileAllowed(["png", "jpg", "jpeg"], "Images PNG ou JPG seulement.")
        ]
    )
    submit = SubmitField("Ajouter le produit")

class ArchiverProduitForm(FlaskForm):
    submit = SubmitField("Supprimer")

class PanierForm(FlaskForm):
    submit = SubmitField("Ajouter au panier")

class ModifierProfilForm(FlaskForm):
    nom = StringField(
        "Nom d'utilisateur",
        filters=[lambda valeur: valeur.strip() if valeur else ""],
        validators=[
            DataRequired(message="Le nom d'utilisateur est obligatoire.")
        ]
    )

    courriel = StringField(
        "Courriel",
        filters=[lambda valeur: valeur.strip() if valeur else ""],
        validators=[
            DataRequired(message="Le courriel est obligatoire.")
        ]
    )

    mdp_actuel = PasswordField("Mot de passe actuel")
    mdp1 = PasswordField("Nouveau mot de passe")
    mdp2 = PasswordField("Confirmer le nouveau mot de passe")

    image = FileField(
        "Image de profil",
        validators=[
            Optional(),
            FileAllowed(
                ["png", "jpg", "jpeg"],
                "Images PNG ou JPG seulement."
            )
        ]
    )

    submit = SubmitField("Modifier")
