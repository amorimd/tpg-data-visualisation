# Visualisation des données de fréquentation des tpg

Ce dépôt contient des scripts Python (Plotly et Dash) pour visualiser les données de fréquentation des transports publics genevois (tpg). Les données sont agrégées au niveau de la ligne et du jour, et enrichies avec des données météorologiques et des informations sur les vacances et les jours fériés.

Les sources de données utilisées sont les suivantes:

- TPG Open Data: Ridership per day per stop per line, [voir ici](https://opendata.tpg.ch/explore/dataset/montees-par-arret-par-ligne/information/?disjunctive.ligne&disjunctive.ligne_type_act&disjunctive.jour_semaine&disjunctive.horaire_type&disjunctive.arret&disjunctive.arret_code_long)
  - Source: transports publics genevois (tpg), état en date du 29/04/2026
- Meteo Suisse: Automatic Weather Stations - Measurement data, daily data for Genève Cointrin (GVE), [voir ici](https://data.geo.admin.ch/browser/index.html#/collections/ch.meteoschweiz.ogd-smn/items/gve)
  - Source: MétéoSuisse

## Application de visualisation

### Description

L'application de visualisation est développée avec Dash, un framework Python pour créer des applications web interactives.
Elle propose deux visualisations de données: la fréquentation quotidienne des toutes les lignes et la frequentation quotidienne par ligne.

### Localement

Cloner le dépôt et installer les dépendances (voir `requirements.txt`). L'application se lance en executant `python data_visualisation_app.py` dans le dossier `dash_app`. L'application sera accessible à l'adresse `http://localhost:8050`.
