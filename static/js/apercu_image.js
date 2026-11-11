/**
 * Permet de visualiser l'image sélectionnée avant d'enregistrer la modification du produit
 * */

"use strict"

const champImage = document.getElementById("image");
const apercu = document.getElementById("apercu-image");

champImage.addEventListener("change", () => {
    const fichier = champImage.files[0];

    if (fichier) {
        apercu.src = URL.createObjectURL(fichier);
    } else {
        apercu.src = apercu.getAttribute("data-img-initiale");
    }
});