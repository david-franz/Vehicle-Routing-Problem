import numpy as np


def load_data(file):

    """
    Read a VRP instance from a .vrp file, and returns the px, py, demand, capacity, depot.

    :param file: the .vrp file.
    :return: px, py, demand, capacity, depot
    """

    f = open(file, "r")

    capacity = 0
    # Skip the first information rows until "NODE_COORD_SECTION" is seen
    line = f.readline()
    while not line.__contains__("NODE_COORD_SECTION"):
        if line.__contains__("CAPACITY"):
            capacity = float(line.split()[-1])
        line = f.readline()

    # Read the coordinate section
    id, px, py = [], [], []

    line = f.readline()
    while not line.__contains__("DEMAND_SECTION"):
        line_elements = line.split()
        id.append(int(line_elements[0]))
        px.append(float(line_elements[1]))
        py.append(float(line_elements[2]))
        line = f.readline()

    # Read the demand section
    demand = np.zeros(len(id))
    line = f.readline()
    while not line.__contains__("DEPOT_SECTION"):
        line_elements = line.split()
        pos = id.index(int(line_elements[0]))
        demand[pos] = float(line_elements[1])
        line = f.readline()

    # Read the single depot
    line = f.readline().rstrip("\n")
    depot = id.index(int(line))

    f.close()

    return np.array(px), np.array(py), demand, capacity, depot


def load_solution(file):

    """
    Read a VRP solution from a .sol file.

    :param file: the .sol file.
    :return: The VRP solution, which is an array of arrays (excluding the depot).
    """

    f = open(file, "r")

    routes = []
    line = f.readline()
    while line.__contains__("Route"):
        a_route_str = line.split(":")[1].lstrip().rstrip()
        a_route = np.array(a_route_str.split()).astype(np.int)
        routes.append(a_route)
        line = f.readline()

    f.close()

    return np.array(routes, dtype=object)
