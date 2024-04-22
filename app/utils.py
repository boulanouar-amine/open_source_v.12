import requests

def geocode(address):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]  # Return the first result
    return None


def reverse_geocode(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={
        latitude}&lon={longitude}"
    headers = {'Accept-Language': 'fr'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data and 'address' in data:
            # Return the address part of the response
            return data['address']
    return None
