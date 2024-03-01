create table violations (
  id_poursuite integer primary key,
  business_id integer,
  date text,
  description varchar(500),
  adresse varchar(100),
  date_jugement text,
  etablissement varchar(100),
  montant integer,
  proprietaire varchar(100),
  ville varchar(50),
  statut varchar(50),
  date_statut text,
  categorie varchar(50)
);

create table plaintes (
  id_plainte integer primary key,
  etablissement text,
  adresse text,
  ville text,
  date_visite text,
  nom_client text, 
  prenom_client text,
  description text
);

create table modifications (
  business_id integer primary key,
  nouveau_nom text,
  deleted integer
);
  