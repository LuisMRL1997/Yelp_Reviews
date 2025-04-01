from flask import Flask, render_template, request
import requests
from urllib.parse import quote
from datetime import datetime, timedelta
import time

app = Flask(__name__)

API_KEY = "****"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
SEARCH_URL = "https://api.yelp.com/v3/businesses/search"
REVIEWS_URL = "https://api.yelp.com/v3/businesses/{}/reviews"

def buscar_restaurante(nombre, ubicacion):
    params = {
        "term": nombre,
        "location": ubicacion,
        "limit": 1
    }
    response = requests.get(SEARCH_URL, headers=HEADERS, params=params)
    data = response.json()
    
    if "businesses" not in data or len(data["businesses"]) == 0:
        return None

    negocio = data["businesses"][0]
    business_id = negocio["id"]
    nombre = negocio["name"]
    calificacion = negocio.get("rating", "N/A")
    direccion = ", ".join(negocio["location"]["display_address"])
    url_imagen = negocio.get("image_url", "No disponible")
    url_yelp = negocio["url"]
    cantidad_resenas = negocio.get("review_count", 0)
    menu_url = negocio.get("attributes", {}).get("menu_url", "No disponible")
    
    info = {
        "business_id": business_id,
        "nombre": nombre,
        "calificacion": calificacion,
        "direccion": direccion,
        "url_imagen": url_imagen,
        "url_yelp": url_yelp,
        "cantidad_resenas": cantidad_resenas,
        "menu_url": menu_url
    }
    return info

def obtener_reseñas(business_id, fecha_inicio, fecha_fin):
    safe_business_id = quote(business_id.strip(), safe="")
    url = REVIEWS_URL.format(safe_business_id)
    reviews_data = []
    next_page_token = None

    while True:
        params = {}
        if next_page_token:
            params['page_token'] = next_page_token

        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()

        if response.status_code != 200:
            break

        if "reviews" in data:
            reviews_data.extend(data["reviews"])

        next_page_token = data.get('next_page_token', None)
        if not next_page_token:
            break 
        time.sleep(2)

    reseñas_filtradas = []
    for review in reviews_data:
        review_date = datetime.strptime(review["time_created"], "%Y-%m-%d %H:%M:%S")
        if fecha_inicio <= review_date.date() <= fecha_fin:
            reseñas_filtradas.append({
                "usuario": review['user']['name'],
                "rating": review['rating'],
                "comentario": review['text'],
                "fecha": review_date.strftime('%Y-%m-%d')
            })
    return reseñas_filtradas

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        restaurante = request.form.get("restaurante")
        ubicacion = request.form.get("ubicacion")
        rango = request.form.get("rango")

        hoy = datetime.now().date()
        if rango == "hoy":
            fecha_inicio = hoy
            fecha_fin = hoy
        elif rango == "7dias":
            fecha_inicio = hoy - timedelta(days=7)
            fecha_fin = hoy
        elif rango == "mes":
            fecha_inicio = hoy - timedelta(days=30)
            fecha_fin = hoy
        elif rango == "anio":
            fecha_inicio = hoy - timedelta(days=365)
            fecha_fin = hoy
        elif rango == "todas":
            fecha_inicio = datetime(1970, 1, 1).date()
            fecha_fin = hoy
        else:
            fecha_inicio = hoy
            fecha_fin = hoy

        info_negocio = buscar_restaurante(restaurante, ubicacion)
        if not info_negocio:
            return render_template("review.html", error="No se encontró el restaurante.")

        reseñas = obtener_reseñas(info_negocio["business_id"], fecha_inicio, fecha_fin)
        return render_template("review.html", negocio=info_negocio, reseñas=reseñas,
                               rango=rango, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
