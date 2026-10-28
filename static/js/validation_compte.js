/**
 * Pour valider les champs du formulaire de création de compte.
 */


/* global envoyerRequeteAjax */


"use strict"

const re = new RegExp(/(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)/)

const courriel = document.getElementById("courriel")
const mdp1 = document.getElementById("mdp1")
const mdp2 = document.getElementById("mdp2")
const nom = document.getElementById("nom")
const formulaire = document.getElementsByTagName("form")

async function validerCourriel() {
    courriel.className = ""
    let parametres = {
        "courriel": courriel.value
    }
    const courrielIsUnique = await envoyerRequeteAjax('/api/courriel_unique', "GET", parametres)

    if (courriel.value == "") {
        courriel.className = "is-invalid"
    }
    else if (!re.test(courriel.value)) {
        courriel.className = "is-invalid"
    }
    else if (!courrielIsUnique) {
        courriel.className = "is-invalid"
    }
    else {
        courriel.className = "is-valid"
        return true
    }
    return false
}

async function validerNom() {
    nom.className = ""
    let parametres = {
        "nom": nom.value
    }
    const nomIsUnique = await envoyerRequeteAjax('/api/nom_unique', "GET", parametres)
    if (nom.value == "") {
        nom.className = "is-invalid"
        return false
    }
    else if (!nomIsUnique) {
        nom.className = "is-invalid"
    }
    nom.className = "is-valid"
    return true
}

function validerMDP1() {
    mdp1.className = ""
    if (mdp1.value == "") {
        mdp1.className = "is-invalid"
    }
    else {
        mdp1.className = "is-valid"
        return true
    }
    return false
}

function validerMDP2() {
    mdp2.className = ""
    if (mdp2.value == "") {
        mdp2.className = "is-invalid"
    }
    else if (mdp1.value != mdp2.value) {
        mdp2.className = "is-invalid"
    }
    else {
        mdp2.className = "is-valid"
        return true
    }
    return false
}

function envoyerBloquer(e) {
    e.preventDefault()
}

/**
 * Appelée lors de l'initialisation de la page
 */
function initialisation() {
    document.getElementById("nom").addEventListener("blur", validerNom)
    document.getElementById("courriel").addEventListener("blur", validerCourriel)
    document.getElementById("mdp1").addEventListener("blur", validerMDP1)
    document.getElementById("mdp2").addEventListener("blur", validerMDP2)
    if (validerNom | validerCourriel | validerMDP1 | validerMDP2) {
        formulaire.addEventListener("submit", envoyerBloquer())
    }
}

window.addEventListener("DOMContentLoaded", initialisation)