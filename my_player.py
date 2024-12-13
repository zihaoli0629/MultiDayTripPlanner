from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # Distance matrix between locations (example, in kilometers).
    data['distance_matrix'] = [
        [0, 2, 9, 10, 3],
        [2, 0, 8, 9, 4],
        [9, 8, 0, 1, 7],
        [10, 9, 1, 0, 5],
        [3, 4, 7, 5, 0],
    ]
    data['num_vehicles'] = 3  # 3 days or 3 vehicles
    data['depot'] = 0  # Start from location 0 (the depot)
    data['max_visits_per_vehicle'] = 3  # Max places visited per day
    data['max_travel_distance'] = 30  # Max distance traveled per day (in km)
    return data


def main():
    """Solves the problem with constraints on daily visits and travel distance."""
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback (distance function).
    def distance_callback(from_index, to_index):
        # Returns the distance between the two nodes.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc (distance).
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Dimension to limit the number of stops per vehicle.
    dimension_name_visits = 'Visits'
    routing.AddConstantDimension(
        1,  # Add 1 for each location visited.
        data['max_visits_per_vehicle'],  # Maximum visits per day.
        True,  # Start cumul at zero.
        dimension_name_visits
    )
    visits_dimension = routing.GetDimensionOrDie(dimension_name_visits)

    # Add Dimension to limit the travel distance per vehicle.
    dimension_name_distance = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # No slack
        data['max_travel_distance'],  # Maximum distance per day.
        True,  # Start cumul at zero.
        dimension_name_distance
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name_distance)

    # Set search parameters.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution.
    if solution:
        print_solution(manager, routing, solution, visits_dimension, distance_dimension)


def print_solution(manager, routing, solution, visits_dimension, distance_dimension):
    """Prints the solution on the console."""
    total_distance = 0
    for vehicle_id in range(manager.GetNumberOfVehicles()):
        index = routing.Start(vehicle_id)
        route_distance = 0
        route = []
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            # Get cumulative distance and visits for debugging
            distance_cumul = solution.Value(distance_dimension.CumulVar(index))
            visits_cumul = solution.Value(visits_dimension.CumulVar(index))
            print(f"Node {node} (Cumul Distance: {distance_cumul}, Cumul Visits: {visits_cumul})")
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        route.append(manager.IndexToNode(index))
        print(f"Route for vehicle {vehicle_id}: {route}")
        print(f"Distance of the route: {route_distance} km")
        total_distance += route_distance
    print(f"Total distance of all routes: {total_distance} km")


if __name__ == '__main__':
    main()