/**
 * */

/* global envoyerRequeteAjax */ 

"use strict"


const id_proposition = document.getElementById("courriel")
const approuve = document.getElementById("message")

async function accepterEchange() {
    const offrant = document.getElementById("nom_offrant")
    const proprio = document.getElementById("proprio")
    const objet = document.getElementById("objet_convoite")
    const produitOffert = document.getElementById("produit_offert")

    try{
        const reponse = await envoyerRequeteAjax(
            `/api/accepter_echange/${id_proposition}/${approuve}`,
            "GET",
            null)
    }
    catch (err){
        if (err.name === "AbortError") {
            console.log("Une requête Ajax a été annulée")
        } else {
            console.error("Erreur lors d'une requête Ajax")
            console.error(err)
            // erreur.textContent = "Erreur lors de la requête. Veuillez réessayer."
            // controleur = null
            // chargement.classList.add("masquer")
        }
    }
}

async function refuserEchange() {
    const offrant = document.getElementById("nom_offrant")
    const proprio = document.getElementById("proprio")
    const objet = document.getElementById("objet_convoite")
    const produitOffert = document.getElementById("produit_offert")

    try{
        const reponse = await envoyerRequeteAjax(
            `/api/accepter_echange/${id_proposition}/${approuve}`,
            "GET",
            null)
    }
    catch (err){
        if (err.name === "AbortError") {
            console.log("Une requête Ajax a été annulée")
        } else {
            console.error("Erreur lors d'une requête Ajax")
            console.error(err)
            // erreur.textContent = "Erreur lors de la requête. Veuillez réessayer."
            // controleur = null
            // chargement.classList.add("masquer")
        }
    }
}



/**
 * Appelée lors de l'initialisation de la page
 */
function initialisation() {
    document.getElementById("echange_accepter").addEventListener("click", accepterEchange)
    document.getElementById("echange_refuser").addEventListener("click", refuserEchange)
    
    
    
}

window.addEventListener("DOMContentLoaded", initialisation)