/**
 * */

/* global envoyerRequeteAjax */

"use strict"

let intervalVerif

const nbNotification = document.getElementById("nb_notification")

async function afficherNotif() {

    let nouvelleNotif = await envoyerRequeteAjax(`/api/verifNotif`,
        "GET", null
    )

    if (nouvelleNotif.nouvelle == true) {
        nbNotification.textContent= nouvelleNotif.nb_notif
    } else {
        nbNotification.textContent= ""
    }

}

/**
 * Appelée lors de l'initialisation de la page
 */
function initialisation() {
    console.log("JS chargé !");
    afficherNotif()
    intervalVerif = setInterval(afficherNotif, 2000)
    console.log(document.getElementById("img_notif"));



}

window.addEventListener("DOMContentLoaded", initialisation)