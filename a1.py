import requests
import csv
from database import Database


url = 'https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-'\
      '5955efeb91a0/resource/7f939a08-be8a-45e1-b208-d8744dca8fc6/'\
      'download/violations.csv'


def get_db():
    _database = Database()
    return _database


with requests.get(url) as fichier:
    lignes = fichier.content.decode('utf-8').splitlines()[1:]
    contenu = csv.reader(lignes)
    get_db().import_violations(contenu)
