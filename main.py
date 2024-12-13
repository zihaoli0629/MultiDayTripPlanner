import argparse
import os

from route_planner import create_data_model, solve_itinerary
from route_visualizer import visualize_routes


def read_place_names(file_path):
    """
    Read hotel name and names of destinations from .txt file. 
    By default the hotel name is the first argument.
    Format: "NAME, CITY, COUNTRY"
    :param file_path: file path
    :return: a list that includes hotel name and destination names
    """
    places = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            name = line.strip()
            places.append(name)
    return places

def main():
    parser = argparse.ArgumentParser(description="Multi-day Trip Planner")

    parser.add_argument("--api_key",required=True, type=str, help="API key for distance calculation")
    parser.add_argument("--place_names",required=True, type=str, default="./places.txt", help="Path to the place_names.txt file")
    parser.add_argument("--max_distance_per_day",required=True, default=50, type=float, help="Maximum distance per day")
    parser.add_argument("--max_place_number",required=True, type=float, default=10, help="Maximum number of places per day")
    parser.add_argument("--num_days",required=True, type=int, help="Number of days for the trip")
    parser.add_argument("--save_map", type=bool, default=True, help="Save .html map")
    parser.add_argument("--save_path", type=str, default="./plan", help="map path")

    args = parser.parse_args()

    api_key = args.api_key
    place_names_file = args.place_names
    max_distance_per_day = args.max_distance_per_day
    max_place_number = args.max_place_number + 1 # include hotel
    num_days = args.num_days
    place_names = read_place_names(place_names_file)
    path = args.save_path

    try:
        data, coordinates = create_data_model(place_names, num_days, max_distance_per_day, max_place_number, api_key)
        solution = solve_itinerary(data, place_names)
        if solution:
            for day, sol in enumerate(solution):
                route, route_index = sol[0], sol[1]
                print(f"Day {day + 1}: {' -> '.join(map(str, route))}")
                dist = 0
                for i in range(len(route) - 1):
                    dist += data['distance_matrix'][route_index[i]][route_index[i+1]]
                print(f"Total distance for day {day+1} is {dist:.2f} km \n")
            routes = [sol[0] for sol in solution]
            visualize_routes(routes, coordinates, output_folder=path)
    except Exception as e:
        print(f"Error: {e}")






if __name__ == "__main__":
    main()

    # # generate a map in .html file
    # visualize_routes(daily_routes, output_folder="./plan")
    # print("Route maps have been saved to ./plan.")
