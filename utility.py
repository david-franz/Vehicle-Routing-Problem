import matplotlib.pyplot as plt
import math

def find_nearest_feasible_index(px, py, route, current_index, visited_indexes, capacity, demand):
    nearest_feasible_index = 0 # at the start, the only available option is the depot # make it None?
    dist_to_nearest_feasible_index = float('inf')

    for testing_index, x in enumerate(px):
        if testing_index == current_index:
            continue

        # not visited check
        if visited_indexes[testing_index]:
            continue
        if testing_index in route:
            continue
        
        # distance improvement check
        dist_to_testing_index = calculate_euclidean_distance(px, py, current_index, testing_index)

        #print("--------------------------------------")
        #print("route={}".format(route))
        #print("current_index={}".format(current_index))
        #print("testing_index={}".format(testing_index))
        #print("dist_to_testing_index={}".format(dist_to_testing_index))
        #print("nearest_feasible_index={}".format(nearest_feasible_index))
        #print("dist_to_index_candidate={}".format(dist_to_nearest_feasible_index))
        #print("--------------------------------------")

        if dist_to_testing_index < dist_to_nearest_feasible_index:
            # capacity check
            test_route = route[:]
            test_route.append(testing_index)

            current_demand_used = calculate_current_demand_used(test_route, demand)

            #print("--------------------------------------")
            #print("current_demand_used={}".format(current_demand_used))
            #print("--------------------------------------")

            if current_demand_used <= capacity:
                nearest_feasible_index = testing_index
                dist_to_nearest_feasible_index = dist_to_testing_index

            #if current_demand_used > capacity: # unsure if I need this bit
            #    nearest_feasible_index = 0
            #    dist_to_nearest_feasible_index = float('inf')

#    print("capacity_used={}".format(current_demand_used))

    return nearest_feasible_index

def calculate_current_demand_used(route, demand):
    total = 0
    for index in route:
        total += demand[index]

    return total

def fully_routed(visited_indexes):
    for index, visited in enumerate(visited_indexes):
        if (not visited) and (index != 0):
            return False

    return True

################################################################################

def initialise_routes(index_list):
    routes = list()

    for index in index_list:
        route = list()
        route.append(0)
        route.append(index)
        route.append(0)
        routes.append(route)

    return routes

def calculate_saving(px, py, i, j):
    return (calculate_euclidean_distance(px, py, i, 0)
        + calculate_euclidean_distance(px, py, j, 0) 
            - calculate_euclidean_distance(px, py, i, j))

def calculate_all_savings(px, py, index_list):
    savings = list()

    for i in index_list:
        ith_row = list()
        for j in index_list:
            ith_row.append(calculate_saving(px, py, i, j))
        savings.append(ith_row)

    return savings

def find_sublist_number(routes, index_to_find_sublist_of):
    for number, route in enumerate(routes):
        for index in route:
            if index == index_to_find_sublist_of:
                return number

    return -1

def result_list_capacity(demand, sublist_1, sublist_2):
    result = sublist_1[:-1] + sublist_2[1:len(sublist_2)]

    return calculate_current_demand_used(result, demand)


def merge_routes(routes, available_for_merging, visited_indexes, i, j):
    route_num_i = find_sublist_number(routes, i)
    route_num_j = find_sublist_number(routes, j)

    # do merge
    result = routes[route_num_i][:-1] + routes[route_num_j][1:len(routes[route_num_j])]

    # remove old lists
    for_deletion = list()
    for_deletion.append(routes[route_num_i])
    for_deletion.append(routes[route_num_j])
    for index in sorted(for_deletion, reverse=True): # decrement in reverse order to avoid indexing complications from deletion
        if index in routes:
            routes.remove(index)

    # add new result
    routes.append(result)

    left_most_of_result = result[1]
    right_most_of_result = result[-2]

    # update visted indexes
    visited_indexes[left_most_of_result] = True
    visited_indexes[right_most_of_result] = True

    # update available for merging set
    for index in result:
        if index == 0:
            continue
        try:
            available_for_merging.remove(index)
        except ValueError:
            pass
            
    available_for_merging.append(left_most_of_result)
    available_for_merging.append(right_most_of_result)

    return routes, available_for_merging, visited_indexes

################################################################################

def calculate_euclidean_distance(px, py, index1, index2):

    """
    Calculating the Euclidean distances between two nodes

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param index1: Node 1 index in the coordinate list.
    :param index2: Node 2 index in the coordinate list.
    :return: Euclidean distance between node 1 and 2.
    """

    return math.sqrt(math.pow(px[index1] - px[index2], 2) + math.pow(py[index1] - py[index2], 2))

def calculate_total_distance(routes, px, py, depot):

    """
    Calculating the total Euclidean distance of a solution.

    :param routes: List of routes (list of lists).
    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param depot: Depot.
    :return: Total tour euclidean distance.
    """

    total = 0
    for route in routes:
        prev_index = 0
        for index in list(route):
            total += calculate_euclidean_distance(px, py, prev_index, index)
            prev_index = index

    return total


def visualise_solution(vrp_sol, px, py, depot, title):

    """
    Function for visualise the tour on a 2D figure.

    :param vrp_sol: The vrp solution, which is a list of lists (excluding the depot).
    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param depot: the depot index
    :param title: Plot title.
    """

    n_routes = len(vrp_sol)
    s_vrp_sol = vrp_sol

    # Set axis too slightly larger than the set of x and y
    min_x, max_x, min_y, max_y = min(px), max(px), min(py), max(py)
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    width = (max(px) - min(px)) * 1.1
    height = (max(py) - min(py)) * 1.1

    min_x = center_x - width / 2
    max_x = center_x + width / 2
    min_y = center_y - height / 2
    max_y = center_y + height / 2

    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)

    plt.plot(px[depot], py[depot], 'rs', markersize=5)

    cmap = plt.cm.get_cmap("tab20", n_routes)
    for k in range(n_routes):
        a_route = s_vrp_sol[k]

        # Draw the route: linking to the depot
        plt.plot([px[depot], px[a_route[0]]], [py[depot], py[a_route[0]]], color=cmap(k))
        plt.plot([px[a_route[-1]], px[depot]], [py[a_route[-1]], py[depot]], color=cmap(k))

        # Draw the route: one by one
        for i in range(0, len(a_route)-1):
            plt.plot([px[a_route[i]], px[a_route[i + 1]]], [py[a_route[i]], py[a_route[i + 1]]], color=cmap(k))
            plt.plot(px[a_route[i]], py[a_route[i]], 'co', markersize=5, color=cmap(k))

        plt.plot(px[a_route[-1]], py[a_route[-1]], 'co', markersize=5, color=cmap(k))

    plt.title(title)
    plt.show()
