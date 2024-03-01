// Formulaire A6
function recherche_resto() {
    let form = document.getElementById("recherche_resto");

    fetch("/contrevenant?" + new URLSearchParams({
        etablissement: form["etablissement"].value,
    }))
        .then(response => response.json())
        .then(jsonData => affiche_details_des_restos(jsonData))
        .catch(err => {
            console.log("Erreur avec le serveur :", err);
        });
}

// Affichage resultats A6
function affiche_details_des_restos(jsonData) {
    let nombre_resultats = Object.keys(jsonData).length;
    let affichage_erreur = document.getElementById("erreur_resto");
    let affichage = document.getElementById("resultats_resto");

    // Verifie le nombre de resultats meme si l'existence du resto
    // dans la liste nous indique qu'il y a au moins un resultat:
    if (nombre_resultats == 0) {
        affichage_erreur.innerHTML = "Aucun résultat"
        affichage.innerHTML = ""

    } else {
        affichage_erreur.innerHTML = ""
        affichage.innerHTML = ""

        jsonData.forEach(violation => {
            setTimeout(() => {
                affichage.innerHTML +=
                    "<br>" + 
                    "<span class='fiche'>" +
                        "<div class='fiche_cat'>Categorie : " + violation.categorie + "</div>" +
                        "<div class='fiche_ville'>Ville : " + violation.ville + "</div>" +

                        "<div class='fiche_etablisseement'>Etablissement : <span class='rouge'>" + violation.etablissement + "</span></div>" +
                        "<div class='fiche_busid'>Business ID: " + violation.business_id + "</div>" +

                        "<div class='fiche_addr'>Adresse : " + violation.adresse + "</div>" +
                        "<div class='fiche_prop'>Proprietaire : " + violation.proprietaire + "</div>" +
                        "<div class='fiche_statut'>Statut : " + violation.statut +" (" + violation.date_statut + ")</div>" +

                        "<div class='fiche_poursuite'>Poursuite : " + violation.id_poursuite +" (" + violation.date + ")</div>" +
                        "<div class='fiche_desc'>Description : " + violation.description + "</div>" +
                        
                        "<div class='fiche_date_juge'>Date du jugement : " + violation.date_jugement + "</div>" +
                        "<div class='fiche_montant'>Montant de l'amande : " + violation.montant + "</div>" +
                    "</span>" +
                    "<br>" + 
                    "<br>"
            });
        });
    }
}
