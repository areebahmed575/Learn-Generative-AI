# functions.py

# Define the functions that will be called by the assistant
def update_map(longitude: float, latitude: float, zoom: int):
    return {
        "action": "update_map",
        "latitude": latitude,
        "longitude": longitude,
        "zoom": zoom,
    }

def add_markers(latitudes: list, longitudes: list, labels: list):
    return {
        "action": "add_markers",
        "latitudes": latitudes,
        "longitudes": longitudes,
        "labels": labels,
    }

# Map function names to actual functions
available_functions = {
    "update_map": update_map,
    "add_markers": add_markers,
}

# Define the instruction for the assistant
INSTRUCTION = (
    "You are a helpful travel assistant that can write and execute code, "
    "and has access to a digital map to display information. For any location "
    "the user asks about or asks to navigate to, you should be able to display "
    "the location on the map. You should also be able to display multiple "
    "locations on the map. Add annotations on the map for suggestions and trip planning as well."
)

# Define the tools (functions) that the assistant can use
tools = [
    {
        "type": "function",
        "function": {
            "name": "update_map",
            "description": "Update map to center on a particular location",
            "parameters": {
                "type": "object",
                "properties": {
                    "longitude": {
                        "type": "number",
                        "description": "Longitude of the location to center the map on"
                    },
                    "latitude": {
                        "type": "number",
                        "description": "Latitude of the location to center the map on"
                    },
                    "zoom": {
                        "type": "integer",
                        "description": "Zoom level of the map"
                    }
                },
                "required": ["longitude", "latitude", "zoom"]
            }
        }
    },
    {
        "type": "function",
        "function":  {
            "name": "add_markers",
            "description": "Add list of markers to the map",
            "parameters": {
                "type": "object",
                "properties": {
                    "longitudes": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "List of longitudes for each marker"
                    },
                    "latitudes": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "List of latitudes for each marker"
                    },
                    "labels": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of labels for each marker"
                    }
                },
                "required": ["longitudes", "latitudes", "labels"]
            }
        }
    },
]
