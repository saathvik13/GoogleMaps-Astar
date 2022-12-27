#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Sai Saathvik Domala, sdomala, 2000915420
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#



# !/usr/bin/env python3
import sys
import math
from math import dist, radians, cos, sin, asin, sqrt

#additonal state tour function(not implemented)
def state(present_city, gps, end_coord, road):
    for city in range(len(road)):
        if city[0] == present_city:
            for city_coord in gps:
                if city[0] == city_coord[0]:
                    gps= (city_coord[1] , city_coord[2])
                    dist = calc_distance(present_city, gps, end_coord, road)
                    return dist


# This function returns the route taken in the required output format
def routing(route_taken_city, road):
    route = []
    for city in range(0,len(route_taken_city)-1):
        for places in range(len(road)):
            if route_taken_city[city] == road[places][0] and route_taken_city[city+1] == road[places][1]:
                highway = road[places][4]
                dist = road[places][2]
                dest = road[places][1]
                string = str(highway) + " for "+ str(dist)+ " miles"
                lines = (dest,string)
                route.append(lines)
    return route


# Calculate the new Delivery Hours after rerouting.
def calc_new_delivery(route_taken_city, visited_places):
    t_trip = 0
    
    for city in range(len(route_taken_city)-1):
        for places in range(len(visited_places)-1):
            l = float(visited_places[places][2])        # store the road segment distance.
            speed = float(visited_places[places][3])    # store the road segment speed.
            t_road = float(l/speed)  # calculate the time taken to traverse the road segment.
            
            if route_taken_city[city] == visited_places[places][0] and route_taken_city[city+1] == visited_places[places][1]:             
                if speed >= 50.0:   # if speed>50 , calculate the extra rerouting distance  with the given probability function.
                    prob = math.tanh(l/1000)
                    t_trip = t_trip+ t_road + prob*(2*(t_trip+t_road))
                    break  
                
                else:   # if speed<50, calculate the total distance without rerouting.
                    t_trip = (t_road) + t_trip
                    break
    return t_trip

# This function calculates the delivery heuristic with rerouting
def calc_delivery(next_time, next_distance, next_speed, total_delivery_hours):
    t_trip = total_delivery_hours - next_time
    l=next_distance
    speed=next_speed
    t_road = float(l/speed)
    t=0
    if speed >= 50.0:   # if speed>50 , calculate the extra rerouting distance  with the given probability function.
        prob = math.tanh(l/1000)
        t = t_trip+ t_road + prob*(2*(t_trip+t_road))  

    elif speed < 50.0:   # if speed<50, calculate the total distance without rerouting.
        t = t_road + t_trip

    return t

# This function is used to find the GPS coordinates of cities with no Latitiude and Longitude.
# Here, we impute the coordinates of the nearest city to the city with no Latitiude and Longitude.
def impute_loc(present_city, gps, road):
    min_dist = 0.0
    min_gps_city = (0,0)
    
    for next_places in road:
        if next_places[0] == present_city:
            if min_dist <= float(next_places[2]):   # Check for the mininum raod segment distance.
                min_dist = float(next_places[2])
                min_gps_city = next_places[1]
    
    return find_coord (gps, min_gps_city)   # Find the GPS coordinate of nearest city and return it.


# This function finds the GPS coordinates by traversing through the GPS file.
def find_coord(gps, city):
    lat,lon = 0.0 , 0.0
    for i in gps:
        if i[0] == city:
            lon=float(i[2])
            lat=float(i[1])
    return (lat,lon)


#This function calculates the Haversine distance from between two cities needed for the Heuristic Function.
#This code below has been refered from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points to calculate Haversine Distance.
def calc_distance(present_city, gps, end_coord, road):
    R = 3959.87433      # The radius of Earth is in miles.
    #R=3956
    loc = find_coord(gps, present_city)
    if loc[0] ==0.0 and loc[1] == 0.0:
        loc = impute_loc(present_city, gps, road)

    lat1 = loc[0]
    lat2 = end_coord[0]
    lon1 = loc[1]
    lon2 = end_coord[1]

    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))

    return R * c


# This function calculates the heuristic depending on the cost function given.
def calc_heuristic(cost, route_taken_city, total_miles, total_segments, total_hours, total_delivery_hours, gps, end_coord, road ,next_distance, max_segment , max_speed, next_speed, next_time):
    present_city = route_taken_city[-1]
    #Returns the appropriate Cost according to Cost function given.
    if cost == "distance":
        distance_to_destination = calc_distance(present_city, gps, end_coord, road)     # Compute the distance between two cities
        d = distance_to_destination + total_miles                           # The cost function for DISTANCE- is the addition of total_miles travelled and estimated Haversine distance to the End city. 
        return d
    
    elif cost == 'time':
        distance_to_destination = calc_distance(present_city, gps, end_coord, road)     # Compute the distance between two cities                    
        t = float(distance_to_destination/float(max_speed)) + total_hours   # The cost function for TIME- is the sum of (Haversine distance to the End City divided by the Maximum speed) to the total_hours. This way we keep the cost function admissable since any speed less than the max speed will give a greater time. We use the same function for delivery and calculate the total delivery time later in a seperate function.
        return t  

    elif cost == 'delivery':
        distance_to_destination = calc_distance(present_city, gps, end_coord, road)     # Compute the distance between two cities           
        t_heur = float(distance_to_destination/float(max_speed))
        t_reroute = calc_delivery(next_time, next_distance, next_speed, total_delivery_hours)   # The cost functon is DELIVERY- it computes the given formula are returns the time.
        t_del = t_heur + t_reroute
        return t_del
    
    elif cost == "segments":
        s = float(next_distance/float(max_segment)) + total_segments       #The cost function for SEGMENTS- is the addition of (length of the particular road segment divided by the maximum segment length) to the total_segments travelled and estimated Haversine distance to the End city. This way we keep the cost function admissable since any segment length will not be greater than the maximum segment length.
        return s
"""   
#add
    elif cost == "statetour" and visited_states[present_city][0]:
        print("State Tour")
        st = 2
        return st
#add
 
    if cost == "statetour":
        if next_state not in visited_explored_states:
            distance_to_destination = calc_distance(present_city, gps, end_coord, road)
            st = total_miles + distance_to_destination
            return st
        else :
            return -1
"""

# This function finds the next cities from the present city.
def next_places(present_city,road):
    next_moves = []
    for i in road:
        if i[0] == present_city:
            next_moves.append(i)
    return next_moves


# Sorts the fringe in Ascending order according to the Cost
def sort_acc_to_cost(fringe):
    return fringe[0]


# Here, we store the GPS file from .txt format to a list of lists
def store_data_gps(filename):
    data=[]
    with open(filename, 'r') as f:
        for line in f.readlines():
            parts=line.split()
            data.append(parts)
    return (data)

# Here, we store the Road Segments file from .txt format to a list of lists.
def store_data_road(filename):
    data=[]
    with open(filename, 'r') as f:
        max_segment = 0.0   
        max_speed = 0.0     
        
        for line in f.readlines():
            parts=line.split()
            data.append(parts)
            ini_city=parts[0]
            final_city=parts[1]
            
            dist=parts[2]
            if float(dist) > float(max_segment):        # To find the maximum segment in the road segment file needed for the segment heuristic
                max_segment = dist
        
            speed=parts[3]
            if float(speed) > float(max_speed):         # To find the maximum speed in the road segment file needed for the time heuristic
                max_speed = speed
            
            highway=parts[4]
            reverse_parts=[final_city, ini_city, dist, speed,highway]
            data.append(reverse_parts)
    return (data , max_segment, max_speed)



def get_route(start, end, cost):
    
    city_gps='city-gps.txt'         
    gps=store_data_gps(city_gps)    # Converts city_gps from .txt format to list of lists
 
    road_segments='road-segments.txt'
    road , max_segment , max_speed = store_data_road(road_segments)     # Converts road-segments.txt from .txt format to list of lists
   
    visited_places=[]       # Store the list of all road segments visited
    route_taken_city = []   # Store the list of city route in the fringe
    route_taken_city.append(start)

    visited = {}
    visited_states = [] #add
    heu_priority = {}
    
    end_coord= find_coord(gps, end)

    heu, total_segments, total_miles, total_segments, total_hours, total_delivery_hours = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    fringe = [[heu, route_taken_city, total_miles, total_segments, total_hours, total_delivery_hours]]    # Initialize the fringe.

    while len(fringe)>0:
        heu, route_taken_city, total_miles, total_segments, total_hours, total_delivery_hours = fringe.pop()

        present_city = route_taken_city[-1] 

        if present_city == end: #Check for Goal
            final_delivery_hours = calc_new_delivery(route_taken_city, visited_places)
            routes = routing(route_taken_city, road)    #Calculates the final route in the required output format
            
            final_dict = {"total-segments" : len(route_taken_city)-1, 
            "total-miles" : total_miles, 
            "total-hours" : total_hours, 
            "total-delivery-hours" : final_delivery_hours, 
            "route-taken" : routes}
            
            #print("route_taken_city={}   Total_Seg={}   Total_Miles={}   Total_Hours={}   Total_Delivery={}".format(route_taken_city, total_segments, total_miles, total_hours, final_delivery_hours))
            return final_dict
        
        visited[present_city] = 1
        curr_state = present_city.split(" ")[0].split(",_")[1] # for statetour
        visited_states.append((curr_state, heu))    #for statetour
        heu_priority[present_city] = heu

        for places in next_places(present_city, road):
            city= places[1]
            visited_places.append(places)

            next_distance = float(places[2])
            next_speed = float(places[3])
            next_time = next_distance/next_speed

            next_heu = calc_heuristic(cost, route_taken_city + [places[1]], total_miles + next_distance, total_segments+1 , total_hours + next_time, total_delivery_hours+ next_time, gps, end_coord, road, next_distance,  max_segment , max_speed, next_speed, next_time)
            check_visited = visited.get(city, 0)

            if check_visited and next_heu < heu_priority[city] :    # Checks if the current place is already visited and if the heuristic value is less than the previous iteration of city's heuristic value according to Search algorithm #3
                visited[city] = 0
                fringe.append((next_heu,route_taken_city + [city], total_miles + next_distance, total_segments+1, total_hours + next_time, total_delivery_hours + next_time))
            elif not check_visited:
                fringe.append((next_heu,route_taken_city + [city], total_miles + next_distance, total_segments+1, total_hours + next_time, total_delivery_hours + next_time))
        fringe.sort(key=sort_acc_to_cost,reverse=True)  # Sorts the fringe according to cost
    return None
    """
    Find shortest driving route between start city and end city
    based on a cost function.
    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route_taken_city
        -"total-miles": a float indicating total number of miles in the route_taken_city
        -"total-hours": a float indicating total amount of time in the route_taken_city
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    route_taken_city = [("Martinsville,_Indiana","IN_37 for 19 miles"),
                   ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
                   ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    """return {"total_segments" : len(route_taken_city), 
            "total_miles" : 51., 
            "total_hours" : 1.07949, 
            "total_delivery_hours" : 1.1364, 
            "route_taken_city" : route_taken_city}"""


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])
