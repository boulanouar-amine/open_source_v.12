import streamlit as st
import folium
from streamlit_folium import st_folium
import osmnx as ox

# Add a title to the app
st.title("A* Star Parcel Implementation")

# Initialize session state for markers if it doesn't exist
if "markers" not in st.session_state:
    st.session_state["markers"] = []

# Default location: "Khouribga, Morocco"
default_location = ox.geocode("Khouribga, Morocco")

m = folium.Map(location=default_location, zoom_start=13)
fg = folium.FeatureGroup(name="Markers")

# Add existing markers
for marker in st.session_state["markers"]:
    fg.add_child(marker)

m.add_child(fg)

# Display the map and capture the output
map_output = st_folium(m, width=725, height=525)

# Check if there is a lat, lon in the map_output (user clicked on the map)
if map_output:
    clicked_location = map_output.get("last_clicked")
    if clicked_location:
        lat, lon = clicked_location["lat"], clicked_location["lng"]
        # Create a marker for the clicked location
        new_marker = folium.Marker([lat, lon])
        # Add the new marker to the session state and the feature group
        st.session_state["markers"].append(new_marker)
        fg.add_child(new_marker)
        # Save the map object to the session state before rerunning
        st.session_state["map"] = m
        # Refresh the map to show the new marker
        st.experimental_rerun()

# Button for plotting nodes
submit_button = st.sidebar.button("Plot Nodes")
# At the beginning of the file, after initializing session state for markers
if "map2" not in st.session_state:
    st.session_state["map2"] = None
if "map2_data" not in st.session_state:
    st.session_state["map2_data"] = {"nodes": None, "edges": None}

# Replace the "Plot Nodes" button section with the following:
if submit_button:
    # Check if the map and data already exist in the session state
    if st.session_state["map2"] and st.session_state["map2_data"]["nodes"] is not None:
        # Display the existing map
        st_folium(st.session_state["map2"], width=725, height=525)
    else:
        try:
            # Use the default location for demonstration
            location = default_location
            G = ox.graph_from_point(location, dist=500, network_type="drive")
            # Show all the edges of the graph
            nodes, edges = ox.graph_to_gdfs(G, edges=True)

            # Plot edges on the existing map `m`
            for idx, row in edges.iterrows():
                folium.PolyLine(locations=[(row['geometry'].coords[0][1], row['geometry'].coords[0][0]),
                                           (row['geometry'].coords[-1][1], row['geometry'].coords[-1][0])], color="green").add_to(m)

            # Save the updated map to the session state
            st.session_state["map2"] = m

            # Display the updated map
            st_folium(m, width=725, height=525)
        except ValueError:
            st.sidebar.error("Please enter a valid location")
            st.stop()
