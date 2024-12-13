# route_planner.py
import openrouteservice
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver.routing_enums_pb2 import FirstSolutionStrategy
from typing import List
from math import radians, sin, cos, sqrt, atan2

def fetch_coordinates(place_names: List[str], api_key: str, client) -> dict:
    """
    Fetch latitude and longitude coordinates for a list of place names using OpenRouteService.
    
    Parameters:
    - place_names: List of str, names of places.
    - api_key: str, OpenRouteService API key.

    Returns:
    - dict: {place_name: (latitude, longitude)}
    """
    coordinates = {}
    for place in place_names:
        try:
            geocode = client.pelias_search(text=place)
            lat = geocode['features'][0]['geometry']['coordinates'][1]
            lon = geocode['features'][0]['geometry']['coordinates'][0]
            coordinates[place] = (lat, lon)
        except Exception as e:
            raise ValueError(f"Failed to fetch coordinates for {place}: {e}")
    print("\nHere are the coordinates:\n")
    for name in coordinates:
        print(name, ", \n", coordinates[name])
    return coordinates

def haversine_distance(coord1, coord2):
    """
    Calculate the Haversine distance between two points on the Earth's surface.
    :param coord1: Tuple (longitude, latitude) of the first point.
    :param coord2: Tuple (longitude, latitude) of the second point.
    :return: Distance in kilometers.
    """
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert coordinates to radians
    lon1, lat1 = map(radians, coord1)
    lon2, lat2 = map(radians, coord2)

    # Differences
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance

def create_distance_matrix(coordinates,places):
    """
    Create a distance matrix using the Haversine distance.
    :param coordinates: List of (longitude, latitude) tuples.
    :return: Distance matrix as a 2D list.
    """
    n = len(places)
    distance_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = haversine_distance(coordinates[places[i]], coordinates[places[j]]) 
    print("\n Check the distance matrix in kilometers:\n")
    print([place.split(",")[0] for place in places])
    for row in distance_matrix:
        formated = [f"{dist :.2f}" for dist in row]
        print("["+ ",  ".join(formated) + "]")
    print("\n")
    return distance_matrix


def create_data_model(places, num_days, max_distance_per_day, api_key):
    client = openrouteservice.Client(key=api_key)
    coordinates = fetch_coordinates(places, api_key, client)
    distance_matrix = create_distance_matrix(coordinates, places)
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_days'] = num_days
    data['max_distance_per_day'] = max_distance_per_day
    return data

def solve_itinerary(data: dict, places: list, scale_factor = 10, penalty = 0):
    """Solves the multi-day trip planning problem."""
    num_locations = len(data['distance_matrix'])
    num_days = data['num_days']
    max_distance_per_day = int(data['max_distance_per_day'] * scale_factor) # scale by 10 to to maintain accuracy

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(num_locations, num_days, 0)

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    
    # Create and register a transit callback.
    def distance_callback(from_index, to_index, penalty = penalty):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int((data['distance_matrix'][from_node][to_node] + penalty) * scale_factor)  # scale by 10 to maintain accuracy

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add distance constraint for each day.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # No slack
        max_distance_per_day,  # Maximum distance per day
        True,  # Start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = FirstSolutionStrategy.PATH_CHEAPEST_ARC

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Parse the solution.
    if solution:
        return parse_solution(manager, routing, solution, num_days, places)
    else:
        print("No solution found. Please set a bigger maximum distance per day, or reduce the destination list. ") 
        return []

def parse_solution(manager, routing, solution, num_days, places):
    """Parses the solution into a readable format."""
    routes = []
    hotel = places[0].split(",")[0]
    
    for day in range(num_days):
        index = routing.Start(day)
        route = []
        route_index = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(places[node_index].split(",")[0])
            route_index.append(node_index)
            index = solution.Value(routing.NextVar(index))
        route.append(hotel)  # Return to the hotel
        route_index.append(0)
        routes.append([route, route_index])
    return routes


if __name__ == "__main__":
    api_key = "5b3ce3597851110001cf624893733cf4b16643ba8a02e4e0ac7fbdec"
    place_names = ["Shinjuku, Tokyo",
                    "Akihabara, Taito City, Tokyo", 
                    "Ginza, Tokyo", 
                    "Imperial place, Chiyoda City, Tokyo, Japan",
                    "Meiji Jingu, Shibuya, Tokyo, Japan",
                    "Tokyo national museum, Tokyo, Japan",
                    "sensoji temple, Tokyo, Japan"
                    ]
    num_days = 4 # Specify the number of depots = days
    max_distance_per_day = 30 # total budget 
    penalty = 2 # penalize multiple visits on the same day
    try:
        data = create_data_model(place_names, num_days, max_distance_per_day, api_key)
        solution = solve_itinerary(data, place_names, penalty = penalty)
        if solution:
            for day, sol in enumerate(solution):
                route, route_index = sol[0], sol[1]
                print(f"Day {day + 1}: {' -> '.join(map(str, route))}")
                dist = 0
                for i in range(len(route) - 1):
                    dist += data['distance_matrix'][route_index[i]][route_index[i+1]]
                print(f"Total distance for day {day+1} is {dist:.2f} km \n")

    except Exception as e:
        print(f"Error: {e}")