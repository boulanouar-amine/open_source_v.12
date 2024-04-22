from flask import Blueprint, render_template
import overpy

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def home():

    api = overpy.Overpass()

    result = api.query("""
        [out:json];
        (
        way[highway](50.745,7.17,50.75,7.18);
        >;
        );
        out;
    """)
    

    # Prepare data for LeafletJS
    markers = []
    for node in result.nodes:
        markers.append({'lat': node.lat, 'lng': node.lon})

    print(len(markers))
    # Render the map with LeafletJS
    return render_template('map/view_map.html', markers=markers)
