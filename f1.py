import requests
import webbrowser
import folium

# URL de l'API
api_url = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records"

# Faire une requête GET à l'API
response = requests.get(api_url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    data = response.json()
    # Vérifier si 'records' existe dans les données
    if 'records' in data:
        # On récupère les coordonnées du premier enregistrement pour l'exemple
        first_record = data['records'][0]
        coordinates = first_record['fields']['coordonnees_geo']

        # Extraire latitude et longitude
        latitude = coordinates['lat']
        longitude = coordinates['lon']

        # Créer une carte centrée sur la latitude et la longitude
        m = folium.Map(location=[latitude, longitude], zoom_start=15)

        # Ajouter une flèche (marqueur) avec les coordonnées
        folium.Marker(
            location=[latitude, longitude],
            popup=f'Latitude: {latitude}<br>Longitude: {longitude}',
            icon=folium.Icon(icon='arrow-up', color='blue')  # Flèche personnalisée
        ).add_to(m)

        # Enregistrer la carte dans un fichier HTML
        map_file = 'map_with_coordinates.html'
        m.save(map_file)

        # Ouvrir le fichier HTML dans le navigateur par défaut
        webbrowser.open(map_file)

    else:
        print("La clé 'records' n'existe pas dans la réponse.")
else:
    print("Erreur lors de la récupération des données:", response.status_code)
