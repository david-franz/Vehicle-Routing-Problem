import utility as utility
import loader as loader
import numpy as np

def main():

    # Paths to the data and solution files.
    vrp_file = "vrp-data/n32-k5.vrp"  # "data/n80-k10.vrp"
    sol_file = "vrp-data/n32-k5.sol"  # "data/n80-k10.sol"

    # Loading the VRP data file.
    px, py, demand, capacity, depot = loader.load_data(vrp_file)

    # Displaying to console the distance and visualizing the optimal VRP solution.
    #vrp_best_sol = loader.load_solution(sol_file)
    #best_distance = utility.calculate_total_distance(vrp_best_sol, px, py, depot)
    #print("Best VRP Distance = {}".format(round(best_distance, 3)))
    #utility.visualise_solution(vrp_best_sol, px, py, depot, "Optimal Solution")

    # Executing and visualizing the nearest neighbour VRP heuristic.
    # Uncomment it to do your assignment!

    #nnh_solution = nearest_neighbour_heuristic(px, py, demand, capacity, depot)
    #nnh_distance = utility.calculate_total_distance(nnh_solution, px, py, depot)
    #print("Nearest Neighbour VRP Heuristic Distance = {}".format(round(nnh_distance, 3)))
    #utility.visualise_solution(nnh_solution, px, py, depot, "Nearest Neighbour Heuristic")

    # Executing and visualizing the saving VRP heuristic.
    # Uncomment it to do your assignment!
    
    sh_solution = savings_heuristic(px, py, demand, capacity, depot)
    # sh_distance = utility.calculate_total_distance(sh_solution, px, py, depot)
    # print("Saving VRP Heuristic Distance:", sh_distance)
    # utility.visualise_solution(sh_solution, px, py, depot, "Savings Heuristic")


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

    # increment all by 1 to match input indexing
    #return [[x+1 for x in route] for route in routes]

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

    routes = utility.initialise_routes([index for index, x in enumerate(px)])

    print(routes)



    # TODO - Implement the Saving Heuristic to generate VRP solutions.

    return None


if __name__ == '__main__':
    main()