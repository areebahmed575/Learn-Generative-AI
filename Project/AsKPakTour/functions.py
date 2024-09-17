import os
import requests
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')

if not MAPBOX_ACCESS_TOKEN:
    raise ValueError("Mapbox access token not found in environment variables.")

def geocode_place(place_name: str):
    
    if place_name.strip().lower() == "kashmir":
        query = "Azad Jammu and Kashmir, Pakistan"
    else:
        query = f"{place_name}, Pakistan"
    
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{requests.utils.quote(query)}.json"
    params = {
        'access_token': MAPBOX_ACCESS_TOKEN,
        'limit': 1,
        'country': 'PK',
    }
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code == 200 and data['features']:
        
        longitude, latitude = data['features'][0]['center']
        print(f"Geocoded '{query}': longitude={longitude}, latitude={latitude}")
        return longitude, latitude  
    else:
        
        params.pop('country', None)
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code == 200 and data['features']:
            longitude, latitude = data['features'][0]['center']
            print(f"Geocoded '{query}' without country filter: longitude={longitude}, latitude={latitude}")
            return longitude, latitude
        else:
            raise ValueError(f"Could not geocode place: {place_name}")

def update_map(place_name: str, zoom: int = 12):
    longitude, latitude = geocode_place(place_name)
    return {
        "action": "update_map",
        "longitude": longitude,
        "latitude": latitude,
        "zoom": zoom,
    }

available_functions = {
    "update_map": update_map,
}


INSTRUCTION = (
    "You are a helpful travel assistant specializing in Pakistan's tourism. "
    "When a user asks about places, provide information only about tourist attractions within Pakistan. "
    "Present information in plain text without any Markdown or special formatting. "
    "If the user asks about a specific city or attraction, provide details and use the `update_map` function "
    "to center the map on that place. "
    "If the user asks about Kashmir, provide information only about the Pakistan-administered region known as Azad Jammu and Kashmir. "
    "Do not mention or provide information about places in Indian-administered Kashmir. "
    "Do not provide information about places outside Pakistan. "
    "Always ensure that any place names you mention are accurate and within Pakistan."
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "update_map",
            "description": "Update map to center on a particular place in Pakistan",
            "parameters": {
                "type": "object",
                "properties": {
                    "place_name": {
                        "type": "string",
                        "description": "Name of the place in Pakistan to center the map on"
                    },
                    "zoom": {
                        "type": "integer",
                        "description": "Zoom level of the map",
                        "default": 12
                    }
                },
                "required": ["place_name"]
            }
        }
    }
]
