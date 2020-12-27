
import sys
import os
from tools import astar, dijkstra, bfs, dfs

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = LOCAL_PATH + "/../{0}.csv"


def get_route_dfs(map_name, start, end):
    """Execs python file dfs.py and returns the route optimized."""
    try:
        map = dfs.CharMap(FILE_NAME.format(map_name), start, end)
    except UserInputException:
        print("[Error] Exiting..", file=stderr)
        return -1

    sys.stdout = open(os.devnull, 'w')  # silence
    goalParentId = dfs.dfs(map)
    route = dfs.get_route(map.nodes, goalParentId)
    sys.stdout = sys.__stdout__  # back to standar verbosity

    steps = []
    for node in route:
        steps.append([node.x, node.y])
    steps.append(end)

    return steps


def get_route_bfs(map_name, start, end):
    """Execs python file bfs.py and returns the route optimized."""
    try:
        map = bfs.CharMap(FILE_NAME.format(map_name), start, end)
    except UserInputException:
        print("[Error] Exiting..", file=stderr)
        return -1

    sys.stdout = open(os.devnull, 'w')  # silence
    goalParentId = bfs.bfs(map)
    route = bfs.get_route(map.nodes, goalParentId)
    sys.stdout = sys.__stdout__  # back to standar verbosity

    steps = []
    for node in route:
        steps.append([node.x, node.y])
    steps.append(end)

    return steps


def get_route_dijkstra(map_name, start, end):
    """Execs python file dijkstra.py and returns the route optimized."""
    try:
        map = dijkstra.CharMapCost(FILE_NAME.format(map_name), start, end)
    except UserInputException:
        print("[Error] Exiting..", file=stderr)
        return -1

    sys.stdout = open(os.devnull, 'w')  # silence
    goalParentId = dijkstra.dijkstra(map)
    route = dijkstra.get_route(map.closed_nodes, goalParentId)
    sys.stdout = sys.__stdout__  # back to standar verbosity

    steps = []
    for node in route:
        steps.append([node.x, node.y])
    steps.append(end)

    return steps


def get_route_astar(map_name, start, end):
    """Execs python file astar.py and returns the route optimized."""
    try:
        map = dijkstra.CharMapCost(FILE_NAME.format(map_name), start, end)
    except UserInputException:
        print("[Error] Exiting..", file=stderr)
        return -1

    sys.stdout = open(os.devnull, 'w')  # silence
    goalParentId = astar.astar(map)
    route = astar.get_route(map.closed_nodes, goalParentId)
    sys.stdout = sys.__stdout__  # back to standar verbosity

    steps = []
    for node in route:
        steps.append([node.x, node.y])
    steps.append(end)

    return steps

def get_route(map_name, start, end, alg="astar"):
    if alg == "astar":
        return get_route_astar(map_name, start, end)
    elif alg == "dijkstra":
        return get_route_dijkstra(map_name, start, end)
    elif alg == "bfs":
        return get_route_bfs(map_name, start, end)
    elif alg == "dfs":
        return get_route_dfs(map_name, start, end)
    else:
        return None
