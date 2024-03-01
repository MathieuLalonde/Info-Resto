from flask import Flask
from flask import g
from flask import jsonify
from flask import make_response
from flask import render_template
from flask import request, Response
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import csv
import datetime
from dicttoxml import dicttoxml
import io
import requests
import yaml

from .database import Database
from .plainte import Plainte
from .schemas import schema_ajoute_plainte, schema_rename_contrevenant
from . import courriel

# Va chercher la configuration dans le YAML
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)["update_config"]

update_time = datetime.datetime.strptime(config["update_time"], '%H:%M')
mtl_data = config["mtl_data"]

app = Flask(__name__, static_folder="static")
schema = JsonSchema(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


def escape_html(s):
    s = s.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
    s = s.replace('"', '&quot;').replace("'", '&apos;')
    return s


@app.route('/')
def accueil():
    etablissements = get_db().list_etablissements()
    return render_template('accueil.html', etablissements=etablissements)


@app.route('/plainte/')
def deposer_plainte():
    return render_template('plainte.html')


@app.route('/recherche')
def recherhche():
    etablissement = request.args.get("nom") or ""
    proprietaire = request.args.get("proprietaire") or ""
    adresse = request.args.get("rue") or ""

    violations = get_db().find_violations(etablissement, proprietaire, adresse)
    return render_template('resultats.html', violations=violations)


@app.route('/doc')
def documentation():
    return render_template('doc.html')


@app.route('/contrevenants', methods=["GET"])
def get_contrevenants():
    date_debut = request.args.get("du")
    date_fin = request.args.get("au")

    if (date_debut):
        try:
            date_debut = datetime.date.fromisoformat(date_debut)
        except ValueError:
            return "Erreur : La date de début doit être en format ISO 8610 \
                (AAA-MM-DD)\n", 400
    else:
        date_debut = datetime.date.min

    if (date_fin):
        try:
            date_fin = datetime.date.fromisoformat(date_fin)
        except ValueError:
            return "Erreur : La date de fin doit être en format ISO 8610 \
                (AAA-MM-DD)\n", 400
    else:
        date_fin = datetime.date.max

    violations = get_db().find_violations_between_dates(date_debut, date_fin)
    output = make_response(jsonify(violations))
    output.headers["Content-Disposition"] = "attachment; \
        filename=contrevenants.json"
    output.headers["Content-type"] = "application/json"
    return output


@app.route('/contrevenant/', methods=["GET"])
def get_etablissement():
    etablissement = request.args.get("etablissement").upper()

    if not etablissement:
        print("not etablissement")
        violations = []
    else:
        violations = get_db().find_etablissement(etablissement)
    return jsonify(violations)


@app.route('/contrevenant/<business_id>', methods=["DELETE"])
def delete_etablissement(business_id):
    result = get_db().delete_etablissements(business_id)
    if not result:
        return "Aucun etablissement correspondant\n", 404
    else:
        print("Demande d'inspection supprimée")
        return "Etablissement supprimé\n", 200


@app.route('/rename_contrevenant/', methods=["PATCH"])
@schema.validate(schema_rename_contrevenant)
def rename_etablissement():
    data = request.get_json()
    nouveau_nom = escape_html(data["nouveau_nom"]).upper()

    result = get_db().rename_etablissements(data["business_id"], nouveau_nom)

    if not result:
        return "Aucun etablissement correspondant\n", 404
    else:
        return result, 200


@app.route('/liste_etablissements_json/', methods=["GET"])
def get_liste_json():
    violations = get_db().list_count_infractions()
    output = make_response(jsonify(violations))

    output.headers["Content-Disposition"] = "attachment; \
        filename=etablissements.json"
    output.headers["Content-type"] = "application/json"
    return output


@app.route('/liste_etablissements_xml/', methods=["GET"])
def get_liste_xml():
    violations = get_db().list_count_infractions()
    output = make_response(dicttoxml(violations))

    output.headers["Content-Disposition"] = "attachment; \
        filename=etablissements.xml"
    output.headers["Content-type"] = "application/xml"
    return output


@app.route('/liste_etablissements_csv/', methods=["GET"])
def get_liste_csv():
    violations = get_db().list_count_infractions()
    file = io.StringIO()
    writer = csv.writer(file)

    writer.writerow(violations[0].keys())
    for row in violations:
        writer.writerow(row.values())
    output = make_response(file.getvalue())

    output.headers["Content-Disposition"] = "attachment; \
        filename=etablissements.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/demande_inspection/', methods=["POST"])
@schema.validate(schema_ajoute_plainte)
def post_demande_inspection():

    data = request.get_json()
    plainte = Plainte(
        escape_html(data["etablissement"]),
        escape_html(data["adresse"]),
        escape_html(data["ville"]),
        escape_html(data["date_visite"]),
        escape_html(data["nom_client"]),
        escape_html(data["prenom_client"]),
        escape_html(data["description"])
    )
    plainte = get_db().ajoute_demande_inspection(plainte)
    return jsonify(plainte.asDictionary()), 201


@app.route('/demande_inspection/<id>', methods=["DELETE"])
def delete_demande_inspection(id):
    result = get_db().efface_demande_inspection(id)
    if not result:
        return "404: Aucune demande d'inspection correspondante\n", 404
    else:
        print("Demande d'inspection supprimée")
        return "Demande d'inspection supprimée\n", 200


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# @app.route('/update')
def update_db():
    # Fait la mise a jour de la bd a partir des donnees de la ville de Montreal
    with app.app_context():
        with requests.get(mtl_data) as fichier:
            lignes = fichier.content.decode('utf-8').splitlines()[1:]
            contenu = csv.reader(lignes)
            changements = get_db().import_violations(contenu)

        if changements:
            print("Base de données mise à jour")

            sujet = "Mise à jour de la base de données d'INFO-RESTO"
            plain_text = render_template(
                'email_nouveau_plain.html', etablissements=changements)
            html = render_template(
                'email_nouveau_html.html', etablissements=changements)

            courriel.send_email(sujet, plain_text, html)
        else:
            print("La Base de données est déjà à jour")
    return Response(status=204)


# Lance le BackgroundSchduler a l'ouverture de Flask et le ferme a sa sortie
scheduler = BackgroundScheduler(timezone="America/Montreal")
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# Effectue une mise-a-jour de la bd tous les jours a l'heure specifiee dans
scheduler.add_job(func=update_db, trigger="cron",
                  hour=update_time.hour, minute=update_time.minute)
