import sqlite3
import datetime

select_violations = """\
    select id_poursuite, violations.business_id as business_id,
        date, description, adresse, date_jugement,
        case when modifications.nouveau_nom is not null
            then modifications.nouveau_nom
            else violations.etablissement
        end as etablissement, 
        montant, proprietaire, ville, statut, date_statut, categorie
    from violations
    left join modifications
    on violations.business_id = modifications.business_id
    """


def _build_violation(result_set_item):
    violation = {}
    violation["id_poursuite"] = result_set_item[0]
    violation["business_id"] = result_set_item[1]
    violation["description"] = result_set_item[3]
    violation["adresse"] = result_set_item[4]
    violation["etablissement"] = result_set_item[6]
    violation["montant"] = result_set_item[7]
    violation["proprietaire"] = result_set_item[8]
    violation["ville"] = result_set_item[9]
    violation["statut"] = result_set_item[10]
    violation["categorie"] = result_set_item[12]

    violation["date"] = datetime.datetime.strptime(
        result_set_item[2], '%Y%m%d').strftime('%Y-%m-%d')

    violation["date_jugement"] = datetime.datetime.strptime(
        result_set_item[5], '%Y%m%d').strftime('%Y-%m-%d')

    violation["date_statut"] = datetime.datetime.strptime(
        result_set_item[11], '%Y%m%d').strftime('%Y-%m-%d')

    return violation


def _list_of_tuples_to_list(list_of_tuples):
    list = []
    for tuple in list_of_tuples:
        list.extend(tuple)
    return list


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/db.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def ajoute_demande_inspection(self, plainte):
        connection = self.get_connection()
        cursor = connection.cursor()

        query = ("""\
                insert into plaintes
                (etablissement, adresse, ville, date_visite, nom_client, 
                prenom_client, description)
                values(?, ?, ?, ?, ?, ?, ?)
                """)
        cursor.execute(query, (plainte.etablissement, plainte.adresse, plainte.ville,
                       plainte.date_visite, plainte.nom_client,
                       plainte.prenom_client,
                       plainte.description))
        connection.commit()
        cursor.execute("select last_insert_rowid()")
        result = cursor.fetchall()
        plainte.id = result[0][0]
        return plainte

    def efface_demande_inspection(self, id):
        connection = self.get_connection()
        cursor = connection.cursor()

        query = ("""\
                delete from plaintes
                where id_plainte= ?
                returning *
                """)
        cursor.execute(query, (id,))
        result = cursor.fetchall()
        connection.commit()

        return result

    def import_violations(self, contenu):
        connection = self.get_connection()
        cursor = connection.cursor()

        # Copie la liste des anciennes violations
        cursor.execute("""\
            create temporary table previous 
            as select id_poursuite from violations
            """)

        # Applique les ajouts et mises a jour
        query = ("""\
            insert or replace into violations
                (id_poursuite, business_id, date, description, adresse,
                date_jugement, etablissement, montant, proprietaire, ville,
                statut, date_statut, categorie)
            values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """)
        cursor.executemany(query, contenu)

        # Retourne uniquement les nouvelles violations
        cursor.execute("""\
            select etablissement from violations
            where violations.id_poursuite not in
                (select previous.id_poursuite from previous)
            group by etablissement
            order by etablissement
            """)
        new_entries = cursor.fetchall()
        connection.commit()

        if new_entries is None:
            return new_entries
        else:
            return _list_of_tuples_to_list(new_entries)

    def get_violations(self):
        cursor = self.get_connection().cursor()
        query = (select_violations + """\
            where modifications.deleted is not 1
            order by date desc
            """)
        cursor.execute(query)
        all_data = cursor.fetchall()
        return [_build_violation(item) for item in all_data]

    def find_violations(self, etablissement, proprietaire, adresse):
        cursor = self.get_connection().cursor()
        query = (select_violations + """\
            where etablissement like ?
                and proprietaire like ?
                and adresse like ?
                and modifications.deleted is not 1
            """)
        cursor.execute(query, ('%' + etablissement + '%', '%' +
                       proprietaire + '%', '%' + adresse + '%',))
        all_data = cursor.fetchall()
        return [_build_violation(item) for item in all_data]

    def find_violations_between_dates(self, date_debut, date_fin):
        date_debut = date_debut.strftime('%Y%m%d')
        date_fin = date_fin.strftime('%Y%m%d')

        cursor = self.get_connection().cursor()
        query = (select_violations + """\
            where date between ? and ? and modifications.deleted is not 1
            """)
        cursor.execute(query, (date_debut, date_fin,))
        all_data = cursor.fetchall()
        return [_build_violation(item) for item in all_data]

    def find_etablissement(self, etablissement):
        cursor = self.get_connection().cursor()
        query = (select_violations + """\
            where etablissement like ? and modifications.deleted is not 1
            """)
        cursor.execute(query, (etablissement,))
        all_data = cursor.fetchall()
        return [_build_violation(item) for item in all_data]

    def list_etablissements(self):
        cursor = self.get_connection().cursor()
        query = ("""\
            select distinct
            case when modifications.nouveau_nom is not null
                    then modifications.nouveau_nom
                    else violations.etablissement
            end as etablissement
            from violations
            left join modifications
            on violations.business_id = modifications.business_id
            where modifications.deleted is not 1
            order by etablissement
            """)
        cursor.execute(query,)
        resultat = cursor.fetchall()

        return _list_of_tuples_to_list(resultat)

    def rename_etablissements(self, business_id, nouveau_nom):
        # Ajoute un nom alternatif dans la base de donnees
        connection = self.get_connection()
        cursor = connection.cursor()
        query = ("""\
            insert or replace into modifications
                (business_id, nouveau_nom)
            values(?, ?)
            """)
        cursor.execute(query, (business_id, nouveau_nom))
        connection.commit()
        query = (select_violations + """\
            where violations.business_id= ? and modifications.deleted is not 1
            """)
        cursor.execute(query, (business_id,))
        all_data = cursor.fetchall()
        return [_build_violation(item) for item in all_data]

    def delete_etablissements(self, business_id):
        # Flag l'etablissement comme etant supprime
        connection = self.get_connection()
        cursor = connection.cursor()
        query = ("""\
            insert or replace into modifications
                (business_id, deleted)
            values(?, 1)
            """)
        cursor.execute(query, (business_id,))
        connection.commit()
        return []

    def list_count_infractions(self):
        cursor = self.get_connection().cursor()
        query = ("""\
            select etablissement, count(etablissement)
            from violations
            group by etablissement
            order by count(etablissement) desc
            """)
        cursor.execute(query,)
        liste_resto = cursor.fetchall()

        resultat = []
        for item in liste_resto:
            entree = {}
            entree["etablissement"] = item[0]
            entree["nombre_infractions"] = item[1]
            resultat.append(entree)

        return resultat
