// Formulaire ajout de plainte D1
function demander_inspection() {
    let form = document.getElementById("demande_inspection");
    let confirmation = document.getElementById("confirmation_plainte");

    fetch("/demande_inspection", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "etablissement": form["etablissement"].value,
            "adresse": form["adresse"].value,
            "ville": form["ville"].value,
            "date_visite": form["date_visite"].value,
            "nom_client": form["nom_client"].value,
            "prenom_client": form["prenom_client"].value,
            "description": form["description"].value
        })
    })
        .then(response => response.json())
        .then(form.innerHTML = "")
        .then(jsonData => confirmation.innerHTML =
            "Votre plainte a été déposée avec succes. Votre numéro de plainte est le " + jsonData.id + ".")
}