import requests
import folium
import webbrowser


url = 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records'

params = {
    'limit': 100
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    m = folium.Map(location=[48.8566, 2.3522], tiles="OpenStreetMap", zoom_start=13)

    if 'results' in data:
        for result in data['results']:
            station = result['stationcode']
            name = result['name']
            capacity = result['capacity']
            available_bikes = result['numbikesavailable']
            geo = result['coordonnees_geo']

            lat = geo['lat']
            lon = geo['lon']

            popup_text = f"""
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h3 style="color: #2c3e50; font-size: 18px; font-weight: 800;">{name}</h3>
                <p style="font-size: 14px;"><strong>Capaciaté :</strong> <span style="color: #2980b9;">{capacity}</span></p>
                <p style="font-size: 14px;"><strong>Bikes Disponibles :</strong> <span style="color: #e74c3c;">{available_bikes}</span></p>
            </div>
            """
            folium.Marker([lat, lon], popup=popup_text).add_to(m)

        m.save("velib_map.html")

        webbrowser.open('velib_map.html')

    else:
        print("Aucun enregistrement trouvé dans l'API Velib.")
else:
    print(f"Erreur lors de la requête : {response.status_code}")