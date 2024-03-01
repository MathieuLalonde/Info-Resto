schema_ajoute_plainte = {
    "type": "object",
    "default": {},
    "title": "Schema ajout de plaintes",
    "required": [
        "etablissement",
        "adresse",
        "ville",
        "date_visite",
        "nom_client",
        "prenom_client",
        "description"
    ],
    "properties": {
        "etablissement": {
            "type": "string",
            "default": "",
            "title": "Le schema etablissement",
            "examples": [
                "Chez Jean-Guy"
            ]
        },
        "adresse": {
            "type": "string",
            "default": "",
            "title": "Le schema adresse",
            "examples": [
                "321 Chemin de la Rive"
            ]
        },
        "ville": {
            "type": "string",
            "default": "",
            "title": "Le schema ville",
            "examples": [
                "Montreal"
            ]
        },
        "date_visite": {
            "type": "string",
            "default": "",
            "title": "Le schema date_visite",
            "examples": [
                "2020-10-23"
            ]
        },
        "nom_client": {
            "type": "string",
            "default": "",
            "title": "Le schema nom_client",
            "examples": [
                "Jackson"
            ]
        },
        "prenom_client": {
            "type": "string",
            "default": "",
            "title": "Le schema prenom_client",
            "examples": [
                "Steve"
            ]
        },
        "description": {
            "type": "string",
            "default": "",
            "title": "Le schema description",
            "examples": [
                "Il y avait beacoup de coquerelles partout!"
            ]
        }
    },
    "additionalProperties": False,
    "examples": [{
        "etablissement": "Chez Jean-Guy",
        "adresse": "321 Chemin de la Rive",
        "ville": "Montreal",
        "date_visite": "2020-10-23",
        "nom_client": "Jackson",
        "prenom_client": "Steve",
        "description": "Il y avait beacoup de coquerelles partout!"
    }]
}

schema_rename_contrevenant = {
    "type": "object",
    "default": {},
    "title": "Schema ajout de plaintes",
    "required": [
        "business_id",
        "nouveau_nom"
    ],
    "properties": {
        "business_id": {
            "type": "number",
            "default": "",
            "title": "Le schema business_id",
            "examples": [
                "123456"
            ]
        },
        "nouveau_nom": {
            "type": "string",
            "default": "",
            "title": "Le schema nouveau_nom",
            "examples": [
                "LE RESTO RENOMÉ INC."
            ]
        },
    },
    "additionalProperties": False,
    "examples": [{
        "business_id": "123456",
        "nouveau_nom": "LE RESTO RENOMÉ INC."
    }]
}
