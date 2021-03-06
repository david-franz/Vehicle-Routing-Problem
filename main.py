import utility as utility
import loader as loader
import numpy as np

def main():

    # Paths to the data and solution files.
    vrp_file = "data/n80-k10.vrp" # "data/n32-k5.vrp"
    sol_file = "data/n80-k10.sol" # "data/n32-k5.sol"

    # Loading the VRP data file.
    px, py, demand, capacity, depot = loader.load_data(vrp_file)

    # Displaying to console the distance and visualizing the optimal VRP solution.
    vrp_best_sol = loader.load_solution(sol_file)
    best_distance = utility.calculate_total_distance(vrp_best_sol, px, py, depot)
    print("Best VRP Distance = {}".format(round(best_distance, 5)))
    utility.visualise_solution(vrp_best_sol, px, py, depot, "Optimal Solution")

    # Executing and visualizing the nearest neighbour VRP heuristic.
    # Uncomment it to do your assignment!

    nnh_solution = nearest_neighbour_heuristic(px, py, demand, capacity, depot)
    nnh_distance = utility.calculate_total_distance(nnh_solution, px, py, depot)
    print("Nearest Neighbour VRP Heuristic Distance = {}".format(round(nnh_distance, 5)))
    utility.visualise_solution(nnh_solution, px, py, depot, "Nearest Neighbour Heuristic")

    # Executing and visualizing the saving VRP heuristic.
    # Uncomment it to do your assignment!
    
    sh_solution = savings_heuristic(px, py, demand, capacity, depot)
    sh_distance = utility.calculate_total_distance(sh_solution, px, py, depot)
    print("Saving VRP Heuristic Distance = {}".format(round(sh_distance, 5)))
    utility.visualise_solution(sh_solution, px, py, depot, "Savings Heuristic")


def nearest_neighbour_heuristic(px, py, demand, capacity, depot):

    """
    Algorithm for the nearest neighbour heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).z
    """

    routes = list()
    visited_indexes = [False for i in range(len(px))]

    while (not utility.fully_routed(visited_indexes)):
        
        route = list()

        current_index = 0 # the depot
        route.append(current_index)

        next_index = utility.find_nearest_feasible_index(px, py, route, current_index, visited_indexes, capacity, demand)
        while next_index != 0:
            route.append(next_index)
            current_index = next_index
            next_index = utility.find_nearest_feasible_index(px, py, route, current_index, visited_indexes, capacity, demand)

        route.append(0) # to complete the loop

        routes.append(route)
        for index in route:
            if index == 0:
                continue
            visited_indexes[index] = True

    return routes


def savings_heuristic(px, py, demand, capacity, depot):

    """
    Algorithm for Implementing the savings heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """

    index_list = [index for index, x in enumerate(px)]
    available_for_merging = index_list[:] # deep copy
    visited_indexes = [False for i in range(len(px))]

    routes = utility.initialise_routes(index_list)

    savings = utility.calculate_all_savings(px, py, index_list)
    
    while (not utility.fully_routed(visited_indexes)):
        best_i, best_j, best_saving = (-1, -1, 0)
        for i, ith_row in enumerate(savings):
            for j, val in enumerate(ith_row):
                if i == 0 or j == 0:
                    continue

                if (i != j) and (savings[i][j] > best_saving) and (i in available_for_merging and j in available_for_merging): 
                    sublist_num_i = utility.find_sublist_number(routes, i)
                    sublist_num_j = utility.find_sublist_number(routes, j)

                    if sublist_num_i == sublist_num_j:
                        continue

                    if utility.result_list_capacity(demand, routes[sublist_num_i], routes[sublist_num_j]) <= capacity:
                        best_i = i
                        best_j = j
                        best_saving = savings[i][j]

        routes, available_for_merging, visited_indexes = utility.merge_routes(routes, available_for_merging, visited_indexes, best_i, best_j)

    return routes


if __name__ == '__main__':
    main()