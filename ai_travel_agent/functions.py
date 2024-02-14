import streamlit as st


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
                        "description": "List of longitude of the location to each marker"
                    },
                    "latitudes": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        },
                        "description": "List of latitude of the location to each marker"
                    },
                    "labels": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of text to display on the location of each marker"
                    }
                },
                "required": ["longitudes", "latitudes", "labels"]
            }
        }
    },

]



def update_map(longitude: float, latitude: float, zoom: int):
  
    st.session_state["map"] = {
        "latitude": latitude,
        "longitude": longitude,
        "zoom": zoom,
    }

    return "Map updated!"


def add_markers(latitudes: list, longitudes: list, labels: list):
   
    st.session_state["markers_state"] = {
        "latitudes": latitudes,
        "longitudes": longitudes,
        "labels": labels,
    }
    return "Markers added"


available_functions = {
    "update_map": update_map,
    "add_markers": add_markers,
}

INSTRUCTION = "You are a helpful travel assistant that can write and execute code, and has access to a digital map to display information. For any location user asks about or ask to navigate to, you should be able to display the location on the map. You should also be able to display multiple locations on the map. Ass annotations on map for suggestions and trip planning as well"