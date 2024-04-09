import folium

# Function to create HTML content for the popup
def generate_popup_html(location):
    return f"""
    <html>
        <body>
            <h4 style="margin-bottom:0;">{location['name']}</h4>
            <p style="margin-bottom:0;"><strong>Address:</strong> {location['address']}</p>
            <p style="margin-bottom:0;"><strong>Hours:</strong> {location['operating_hours']}</p>
        </body>
    </html>
    """

def create_folium_map(subway_info_data):
    """_summary_: Create a Folium map with subway locations and a constant 2 km radius 
                  around each location

    Args:
        subway_info_data (_type_): List of subway info data

    Returns:
        _type_: Folium map object
    """
    # Calculate the average latitude and longitude for the initial map center
    average_latitude = sum(location['latitude'] for location in subway_info_data) / len(subway_info_data)
    average_longitude = sum(location['longitude'] for location in subway_info_data) / len(subway_info_data)

    # Create the map object
    map = folium.Map(location=[average_latitude, average_longitude], zoom_start=12)

    # The constant radius for all locations
    constant_radius = 2000  # 2 km in meters

    # Adding markers with styled popups and a constant 2 km radius circle
    for location in subway_info_data:
        iframe = folium.IFrame(generate_popup_html(location), width=200, height=100)
        popup = folium.Popup(iframe, max_width=200)
        folium.Marker(
            [location['latitude'], location['longitude']],
            popup=popup
        ).add_to(map)
        
        # Add a circle to represent the constant 2 km coverage area
        folium.Circle(
            [location['latitude'], location['longitude']],
            radius=constant_radius,
            color='blue',
            fill=True,
            fill_opacity=0.2
        ).add_to(map)

    # # Save the map to an HTML file
    # map.save("sssubway_locations_map_constant_radius.html")
    
    return map