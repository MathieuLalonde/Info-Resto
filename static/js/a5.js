// Formulaire A5 / D3
function recherche_date() {
    let form = document.getElementById("recherche_date");

    let erreurPresente = 0;
    // xxxxxxxxxxxx validation ici!!

    if (erreurPresente == 0) {        
        fetch("/contrevenants?" + new URLSearchParams({
            du: form["date_debut"].value,
            au: form["date_fin"].value,
        }))
            .then(response => response.json())
            .then(jsonData => affiche_compte_des_restos(jsonData))
            .catch(err => {
                console.log("Erreur avec le serveur :", err);
            });
    }
}

// Affichage resultats
function affiche_compte_des_restos(jsonData) {
    let nombre_resultats = Object.keys(jsonData).length;
    let affichage_erreur = document.getElementById("erreur_tableau");
    let affichage = document.getElementById("resultats_date");

    if (nombre_resultats == 0) {
        affichage_erreur.innerHTML = "Aucun résultat"
        affichage.innerHTML = ""
    } else {
        // Compte le nombre d'entrees par etablissement
        let compte = new Map();

        jsonData.forEach(
            
            function (violation) {
                let business_id = violation.business_id;

                if (compte.get(business_id) == undefined) {
                    compte.set(business_id, {
                        instances: 1,
                        etablissement: violation.etablissement
                    })
                } else {
                    let compte_prececent = compte.get(business_id).instances;
                    compte.set(business_id, {
                        instances: compte_prececent + 1,
                        etablissement: violation.etablissement
                    })
                }
            }
        
        );

        // Affiche les resultats
        affichage_erreur.innerHTML = ""
        affichage.innerHTML = "<tr><th>Nom de l'établissement (cliquer pour renommer)</th><th>Nombre de contraventions</th><th>Supprimer</th></tr>"
        compte.forEach((details, business_id) => {
            setTimeout(() => {
                affichage.innerHTML += "<tr id='" + business_id + "'><td>"
                    + "<a href='javascript:void(0);' onclick='show_rename_etablissement(" + business_id + ", &quot;" + details.etablissement + "&quot;)'>" + details.etablissement + "</a>"
                    + "</td><td class='centre'>" + details.instances + "</td>"
                    + "<td class='centre'>"
                    + "<a href='javascript:void(0);' onclick='delete_etablissement(" + business_id + ")'>"
                    + "<img src='static/img/poubelle.png' alt='icone de poubelle'></a></td></tr>";
            });
        });
    }
}

function show_rename_etablissement(business_id, etablissement) {
    let row = document.getElementById(business_id);

    etablissement = etablissement.replace(/'/g, "&apos;").replace(/"/g, "&quot;")

    row.firstChild.innerHTML = "<td><form class='rename_etablissement' id='form_" + business_id + "'>"
        + "<input type='text' class='rename_field' name='nouveau_nom' value='" + etablissement + "'>"
        + "<button type='button' onclick='rename_etablissement(" + business_id + ");'> Renommer </button>"
        + "</form></td>"
}

function rename_etablissement(business_id) {
    let form = document.getElementById("form_" + business_id);
    let nouveau_nom = form["nouveau_nom"].value.toUpperCase()
    let row = document.getElementById(business_id);

    fetch("/rename_contrevenant/", {
        method: "PATCH",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
        body: JSON.stringify({
            "business_id": business_id,
            "nouveau_nom": nouveau_nom,
            })
        })
        .then(response => response.json())
        .then(jsonData => jsonData[0])
        .then(jsonData => row.firstChild.innerHTML = "<td>Contrevenant renommé à :<br>"
            + "<a href='javascript:void(0);' onclick='show_rename_etablissement(" + jsonData.business_id + ",&quot;"
            + jsonData.etablissement + "&quot;)'>" + jsonData.etablissement + "</a>"
            + "</td>")
        .catch(err => {
            console.log("Erreur avec le serveur :", err);
            row.firstChild.innerHTML = "<td>Erreur avec le serveur; réessayez plus tard</td>";
        })
}

function delete_etablissement(business_id) {
    let row = document.getElementById(business_id);

    fetch("/contrevenant/" + business_id, {
        method: "DELETE",
        })
        .then(row.innerHTML = "<tr><td>contrevenant supprimé</td><td></td><td></td></tr>")
        .catch(err => {
            console.log("Erreur avec le serveur :", err);
            row.firstChild.innerHTML = "<td>Erreur avec le serveur; réessayez plus tard</td>";
        })
}
