/**
 * */

/* global envoyerRequeteAjax */

"use strict"

let intervalVerif

const imgNotif = document.getElementById("img_notif")
const nbNotification = document.getElementById("nb_notification")

async function afficherNotif() {

    let nouvelleNotif = await envoyerRequeteAjax(`/api/verifNotif`,
        "GET", null
    )
    console.log("Notification")
    if (nouvelleNotif.nouvelle == true) {
        console.log("Alarm")
        imgNotif.src = "/images/alarm.png"
        imgNotif.alt = "image de nouvelle notification"
        nbNotification.textContent= nouvelleNotif.nb_notif
    } else {
        console.log("Bell")
        imgNotif.src = "/images/bell.png"
        imgNotif.alt = "image d'il n'y a pas de nouvelle notif"
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