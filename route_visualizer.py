import folium
from folium import plugins

def visualize_routes(routes, coordinates, output_folder="./plan"):
    """
    visualize route for everyday trip on a map
    args:
    - routes: list of list, route every day
    - coordinates: dict, {name: (longitude, latitude)}
    - output_folder: str, path for saved map
    """
    import os
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for day, route in enumerate(routes, start=1):
        m = folium.Map(location=coordinates[route[0]], zoom_start=13)

        # add location label
        for loc in route:
            folium.Marker(location=coordinates[loc], popup=loc).add_to(m)

        # add route
        for i in range(len(route) - 1):
            start = coordinates[route[i]]
            end = coordinates[route[i + 1]]
            curr_line = folium.PolyLine([start, end], color="blue", weight=1.5)

            # Add an arrow using a Marker with custom icon
            arrow = plugins.PolyLineTextPath(
                curr_line.add_to(m),
                text='→',               # The arrow symbol
                repeat=True,            # Repeat along the line
                offset=10,              # Distance between repeated arrows
                attributes={'font-size': '30px', "fill":"blue"}
            )
            arrow.add_to(m)

        # save the map
        map_path = os.path.join(output_folder, f"day_{day}_route.html")
        m.save(map_path)
        print(f"Day {day} has been saved to {map_path}")

