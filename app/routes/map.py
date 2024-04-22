from flask import Blueprint, request, redirect, url_for, render_template
import folium
import folium.plugins as plugins
from markupsafe import Markup


map_bp = Blueprint('map', __name__)


@map_bp.route('/map', methods=['GET'])
def get_map():
    m = folium.Map()


    wind_locations = [
    [59.35560, -31.992190],
    [55.178870, -42.89062],
    [47.754100, -43.94531],
    [38.272690, -37.96875],
    [27.059130, -41.13281],
    [16.299050, -36.56250],
    [8.4071700, -30.23437],
    [1.0546300, -22.50000],
    [-8.754790, -18.28125],
    [-21.61658, -20.03906],
    [-31.35364, -24.25781],
    [-39.90974, -30.93750],
    [-43.83453, -41.13281],
    [-47.75410, -49.92187],
    [-50.95843, -54.14062],
    [-55.97380, -56.60156],
]
    folium.plugins.AntPath(
        locations=wind_locations, reverse="True", dash_array=[20, 30]
    ).add_to(m)

    m.fit_bounds(m.get_bounds())

    map_html = m._repr_html_()
  
    return render_template('maps/map_template.html', map_html=Markup(map_html))
