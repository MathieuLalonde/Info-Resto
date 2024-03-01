Info-Resto

# Instructions pour la correction

Voici une liste des points développés dans ce projet et de brèves instruction explicant comment les tester :

## A1

En lançant le fichier `a1.py`, la liste des contraventions sera automatiquement téléchargée et son contenu stocké dans la base de données. 

p.s. Au besoin, le script de création pour la base de donnéees est `db\db.sql`

## A2

L'application Flask peut être lancée avec une commande `make` et sera ensuite accessible via `localhost:5000`.

En entrant des valeurs dans l'un (ou plusieurs) des trois champs de `Recherche générale` et appuyant sur le bouton de recherche, une recherche sera lancée.

## A3

À minuit, les données seront mises à jour. L'heure peut être reconfigurée en modifiant la valeur `update_time` dans le fichier `config.yaml` et effectuant une sauvegarde dans le fichier `index.py` pour relancer l'application principale.

## A4

En navigant à [localhost:5000/contrevenants?du=2020-05-08&au=2022-05-15](http://localhost:5000/contrevenants?du=2020-05-08&au=2022-05-15), un fichier `contrevenants.json` sera automatiquement téléchargé. 

À noter: Les champs `du` et `au` sont optionels; si l'une des deux dates est abscente, elle sera remplacée par une date min/max. Une requête sans date inclura donc toutes les entrées.

La documentation pour ce service est diponible sur [localhost:5000/doc](http://localhost:5000/doc)

## A5

Le formulaire `Recherche par date` de la page d'accueil permet de lancer la même recherche via le site web.

À noter: Les fonctionalitées du point D3 ont été implémentées dans l'affichage des résultats.

## A6

Le formulaire `Recherche par établissement` de la page d'accueil permet de sélectionner le restaurent voulu et d'afficher ses infractions.

<br/>

## B1

Pour s'assurer de détecter de nouvelles contraventions, la façon la plus simple est d'en effacer quelques unes pour ensuite de faire une mise-à-jour de la base de données.

Du répertoire principal du projet, lancez:

```
sqlite3 db/db.db "delete from violations where date=20211025;"
```
Il y a ensuite deux façons de forcer une mise-à-jour:
- Via le backgroundScheduler (comme à l'étape A3).
- En décommentant la route `@app.route('/update')` (au bas d'index.py) et visitant ensuite [localhost:5000/update](http://localhost:5000/update).

La base de données sera mise à jour et un courriel sera automatiquement envoyé à l'adresse spécifiée comme `receiver_email` dans le fichier `config.yaml`.

<br/>

## C1, C2 et C3

Les étapes C1, C2 et C3 peuvent toutes être validées en visitant leurs url respectives pour y télécharger les documents désirés :

[localhost:5000/liste_etablissements_json](http://localhost:5000/liste_etablissements_json)

[localhost:5000/liste_etablissements_xml](http://localhost:5000/liste_etablissements_xml)

[localhost:5000/liste_etablissements_csv](http://localhost:5000/liste_etablissements_csv)

La documentation pour les trois services est diponible sur [localhost:5000/doc](http://localhost:5000/doc)

<br/>

## D1

Pour faire une demande d'inspection via le service REST, on envoit une demande `POST` à `localhost:5000/demande_inspection` accompagnée d'une body JSON :

```
curl -X POST http://localhost:5000/demande_inspection/ \
    -H "Content-Type: application/json, Accept: application/json" \
    -d '{"etablissement": "RESTAURANT CHEZ BOB", "adresse": "123 Rue Main", "ville": "Montreal", "date_visite": "2011-08-07", "nom_client": "Bond", "prenom_client": "James", "description": "Il y avait des coquerelles partout."}'
```

La documentation pour ce service est diponible sur [localhost:5000/doc](http://localhost:5000/doc)

La demande peut également être faite sur le site web: [localhost:5000/plainte](http://localhost:5000/plainte) ou en cliquant le lien `Déposer une plainte`.

## D2

Pour supprimer une demande d'inspection via le service REST, on envoit une demande `DELETE` à `localhost:5000/demande_inspection/` suivi de l'index numérique de la demande à suppimer

```
curl -X DELETE http://localhost:5000/demande_inspection/1
```

## D3

Le formulaire `Recherche par date` de la page d'accueil permet de lancer une recherche par date.

À la droite des résultats, l'icone d'une poubelle permet de supprimer n'importe lequel des contrevenants affichés de la base de données. 

Pour les renommer, il suffit de cliquer sur son nom et un champ apparaîtera pour le renommer. 


