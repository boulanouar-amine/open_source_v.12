from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        address = request.form['address']
        api_key = 'your_tomtom_api_key_here'
        url = f"https://api.tomtom.com/search/2/geocode/{address}.json?key={BwENUoPMGyzQlUXqnDMN7mdZcoAtSdA7}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            lat = data['results'][0]['position']['lat']
            lon = data['results'][0]['position']['lon']
            return render_template('map.html', latitude=lat, longitude=lon, api_key=api_key)
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
