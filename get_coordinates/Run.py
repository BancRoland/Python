import requests

def get_coordinates(location_name: str, api_key: str):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location_name,
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print(f"Error: {data['status']}")
        return None

# Example usage
api_key = "YOUR_API_KEY_HERE"
location = "Statue of Liberty, New York"
coords = get_coordinates(location, api_key)
print(f"Coordinates for '{location}': {coords}")
