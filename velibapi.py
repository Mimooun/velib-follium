import requests
import json
import sqlite3

# Créer une connexion à la base de données SQLite
conn = sqlite3.connect('velib_data.db')
cursor = conn.cursor()

# Créer une table pour stocker les données si elle n'existe pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS velib (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id TEXT,
    name TEXT,
    available_bikes INTEGER,
    available_slots INTEGER,
    last_update TEXT
)
''')

# URL de l'API
api_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records"

# Paramètres pour la requête
params = {
    'limit': 100,  # Limite le nombre d'enregistrements par page
    'offset': 0  # Offset pour gérer la pagination
}

# Liste pour stocker toutes les données
all_data = []

while True:
    # Envoyer une requête GET à l'API
    response = requests.get(api_url, params=params)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        data = response.json()

        # Afficher la réponse pour déboguer
        print("Réponse brute de l'API :")
        print(json.dumps(data, indent=4, ensure_ascii=False))  # Afficher la réponse entière

        # Vérifier si la clé 'records' existe dans la réponse
        if 'records' in data:
            records = data['records']
            print(f"Nombre d'enregistrements récupérés : {len(records)}")  # Afficher le nombre d'enregistrements

            for record in records:
                station_data = record['fields']
                print(station_data)  # Afficher les données à insérer

                # Insérer les données dans la base de données
                try:
                    cursor.execute('''
                    INSERT INTO velib (station_id, name, available_bikes, available_slots, last_update)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (station_data.get('station_id'), station_data.get('name'),
                          station_data.get('available_bikes'), station_data.get('available_slots'),
                          station_data.get('last_update')))

                    # Ajouter les données à la collection
                    all_data.append(station_data)

                except Exception as e:
                    print("Erreur lors de l'insertion des données :", e)

        else:
            print("La clé 'records' n'existe pas dans la réponse.")
            break

        # Vérifier si nous avons récupéré tous les enregistrements
        if len(records) < params['limit']:
            break  # Sortir de la boucle si moins d'enregistrements que la limite

        # Mettre à jour l'offset pour la prochaine requête
        params['offset'] += params['limit']
    else:
        print("Erreur lors de la récupération des données:", response.status_code)
        break

# Sauvegarder les changements et fermer la connexion
conn.commit()
conn.close()

# Afficher les données récupérées
print("Données stockées dans la collection :")
print(json.dumps(all_data, indent=4, ensure_ascii=False))
