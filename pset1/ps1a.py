###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: David Fox

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cows_file = open(filename, "r")
    cows_dict = {}
    
    for cow in cows_file:
        cow = cow.replace(" ", "")
        key = 0
        while key < len(cow):
            if cow[key] == ",":
                cows_dict[cow[0:key]] = int(cow[key+1])
                break
            else:
                key += 1
    
    return cows_dict

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cow_names = sorted(cows.keys(), key = lambda x: cows[x], reverse = True)
    all_trips = []
    
    while len(cow_names) != 0:
        current_trip = []
        current_weight = 0
        i = 0
        
        
        while current_weight < limit and i < len(cow_names):
            if (cows[cow_names[i]] + current_weight <= limit):
                current_trip.append(cow_names[i])
                current_weight += cows[cow_names[i]]
            i += 1
            
        for cow in current_trip:
            cow_names.remove(cow)
            
        all_trips.append(current_trip)
        
    
    return all_trips
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    all_options = sorted(list(get_partitions(cows.keys())), key = lambda x: len(x))
    ## legal_options = []
    
    ## remove illegal partitions.
    for trans in all_options:
        legal = True
        for trip in trans:
            weight = 0
            ## Sum weights for a single trip. Breaks
            ## loop without adding to legal if too heavy.
            for cow in trip:
                weight += cows[cow]
            if weight > limit:
                legal = False
                break
        if legal:
            return trans

# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows("ps1_cow_data.txt")
    start = time.time()
    greedy_transport_sched = greedy_cow_transport(cows)
    end = time.time()
    greedy_time = end - start
    
    start = time.time()
    brute_transport_sched = brute_force_cow_transport(cows)
    end = time.time()
    brute_time = end - start
    
    print("Greedy algorithm transport schedule:")
    for i in range(len(greedy_transport_sched)):
        print("trip " + str(i + 1) + ": ", end = '')
        for cow in greedy_transport_sched[i]:
            print(cow + ", ", end = '')
        print("\n")
    
    print("Brute force algorithm transport schedule:")
    for i in range(len(brute_transport_sched)):
        print("trip " + str(i + 1) + ": ", end = '')
        for cow in brute_transport_sched[i]:
            print(cow + ", ", end = '')
        print("\n")
    
    print("Greedy transport used " + str(len(greedy_transport_sched)) + " trips", end = " ")
    print(" and took " + str(greedy_time) + " seconds.")
    print("Brute force transport used " + str(len(brute_transport_sched)) + " trips", end = " ")
    print(" and took " + str(brute_time) + " seconds.")
    
compare_cow_transport_algorithms()


