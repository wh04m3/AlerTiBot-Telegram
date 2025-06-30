from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def obtener_direccion(lat, lon):
    try:
        geolocalizador = Nominatim(user_agent="alertibot")
        ubicacion = geolocalizador.reverse((lat, lon), language='es')
        return ubicacion.address if ubicacion else "Dirección no encontrada"
    except Exception as e:
        return f"Error al obtener dirección: {e}"

# Ejemplo de uso:
#print(obtener_direccion(19.372385, -98.913537))

def obtener_municipio(lat, lon):
  #devuelve unicamente el municipio
    try:
        geolocalizador = Nominatim(user_agent="alertibot")
        ubicacion = geolocalizador.reverse((lat, lon), language='es')

        if ubicacion and ubicacion.raw.get("address"):
            direccion = ubicacion.raw["address"]
            municipio = direccion.get()
            return direccion or "Municipio no encontrado"
        else:
            return "Municipio no encontrado"
    except Exception as e:
        return f"Error: {e}"
    
def obtener_direccion_clave(lat, lon):
    try:
        geolocalizador = Nominatim(user_agent="alertibot")
        ubicacion = geolocalizador.reverse((lat, lon), language='es')

        if not ubicacion or "address" not in ubicacion.raw:
            return {}

        address = ubicacion.raw["address"]

        return {
            "calle": address.get("road"),
            "colonia": address.get("suburb") or address.get("neighbourhood"),
            "municipio": address.get("municipality") or address.get("town") or address.get("city"),
            "estado": address.get("state"),
            "codigo_postal": address.get("postcode"),
            "pais": address.get("country")
        }

    except Exception as e:
        return {"error": str(e)}
    


def esta_a_menos_de_100_m(coord1, coord2):
    distancia_m = geodesic(coord1, coord2).meters
    return distancia_m <= 100

