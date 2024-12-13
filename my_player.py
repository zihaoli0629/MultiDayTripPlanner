from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver.routing_enums_pb2 import FirstSolutionStrategy

def create_data_model(distance_matrix, num_days, max_distance_per_day):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = distance_matrix
    data['num_days'] = num_days
    data['max_distance_per_day'] = max_distance_per_day
    return data

def solve_itinerary(data):
    """Solves the multi-day trip planning problem."""
    num_locations = len(data['distance_matrix'])
    num_days = data['num_days']
    max_distance_per_day = int(data['max_distance_per_day'] * 10) # [W]

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(num_locations, num_days, 0)

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(data['distance_matrix'][from_node][to_node] * 10) # [W]

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
        return parse_solution(manager, routing, solution, num_days)
    else:
        print("No solution found. Please set a bigger maximum distance per day, or reduce the destination list. ") 

def parse_solution(manager, routing, solution, num_days):
    """Parses the solution into a readable format."""
    routes = []
    for day in range(num_days):
        index = routing.Start(day)
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(node_index)
            index = solution.Value(routing.NextVar(index))
        route.append(0)  # Return to the hotel
        routes.append(route)
    return routes

def main():
    # Example distance matrix (0-th row/column represents the hotel)
    # distance_matrix = [
    #     [0, 10, 7, 7, 3.3],
    #     [11, 0, 5, 3, 10],
    #     [20, 15, 0, 10, 20],
    #     [20, 25, 10, 0, 15],
    #     [20, 20, 20, 15, 0],
    # ]
    distance_matrix = [
        [0, 10.4384, 7.174, 7.2779, 3.1147], 
        [10.937299999999999, 0, 5.5374, 3.625, 10.3047], 
        [7.815, 5.3372, 0, 2.5076, 7.182300000000001], 
        [7.753100000000001, 3.1604, 2.3503000000000003, 0, 7.1205], 
        [3.4558, 10.1965, 6.9321, 7.0361, 0]
        ]

    num_days = 4
    max_distance_per_day = 25

    data = create_data_model(distance_matrix, num_days, max_distance_per_day)
    solution = solve_itinerary(data)

    # Print the solution
    for day, route in enumerate(solution):
        print(f"Day {day + 1}: {' -> '.join(map(str, route))}")
        dist = 0
        for i in range(len(route) - 1):
            dist += distance_matrix[route[i]][route[i+1]]
        print(f"Total distance for day {day} is {dist}")
if __name__ == "__main__":
    main()