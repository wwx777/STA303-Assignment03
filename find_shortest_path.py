from typing import List
from plot_underground_path import plot_path
from build_data import Station, build_data
import argparse
import math
from queue import PriorityQueue



# Implement the following function
def get_path(start_station_name: str, end_station_name: str, map: dict[str, Station]) -> List[str]:
    """
    Runs A* on the map, find the shortest path between a and b
    Args:
        start_station_name(str): The name of the starting station
        end_station_name(str): str The name of the ending station
        map(dict[str, Station]): Mapping between station names and station objects of the name,
                                 Please refer to the relevant comments in the build_data.py
                                 for the description of the Station class
    Returns:
        List[str]: A path composed of a series of station names
    """
    start_station = map[start_station_name]
    end_station = map[end_station_name]
    

    open_set = PriorityQueue()
    open_set.put((0, start_station, [start_station]))

    closed_set = set()
    expanded_nodes = 0
    iterations = 0

    while not open_set.empty():
        current_cost, current_station, current_path = open_set.get()
        iterations += 1

        if current_station == end_station:
            # Convert the path to a list of station names
            path_names = [station.name for station in current_path]
            return path_names,expanded_nodes, iterations   # Found the path
        if current_station not in closed_set:
            closed_set.add(current_station)
            expanded_nodes += 1


        for neighbor in current_station.links:
            if neighbor not in closed_set:
                new_cost = current_cost + distance(current_station, neighbor)  # Replace with your distance function
                heuristic = estimate_heuristic(neighbor, end_station)  # Replace with your heuristic function
                total_cost = new_cost + heuristic
                new_path = current_path + [neighbor]

                open_set.put((total_cost, neighbor, new_path))

    return None,expanded_nodes, iterations   # No path found

def distance(station1, station2):
    # 计算两个站点之间的直线距离（欧几里得距离）
    lat1, lon1 = station1.position
    lat2, lon2 = station2.position
    distance_km = math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
    return distance_km

def estimate_heuristic(station, goal_station):
    # 使用直线距离作为启发式（估计）代价
    return distance(station, goal_station)



if __name__ == '__main__':

    # 创建ArgumentParser对象
    parser = argparse.ArgumentParser()
    # 添加命令行参数
    parser.add_argument('start_station_name', type=str, help='start_station_name')
    parser.add_argument('end_station_name', type=str, help='end_station_name')
    args = parser.parse_args()
    start_station_name = args.start_station_name
    end_station_name = args.end_station_name

    # The relevant descriptions of stations and underground_lines can be found in the build_data.py
    stations, underground_lines = build_data()
    path,expanded_nodes,iterations = get_path(start_station_name, end_station_name, stations)
    print(f"Path: {path}")  # Add this line to check the value of path
    
    # Check if a valid path is found
    if path is not None:
    # visualization the path
    # Open the visualization_underground/my_path_in_London_railway.html to view the path, and your path is marked in red
        plot_path(path, 'visualization_underground/my_shortest_path_in_London_railway.html', stations, underground_lines)
    else:
        print("Unable to find a path.")
    # visualization the path
   