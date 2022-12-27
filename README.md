This is a simple dataset of North American (though mostly U.S.) major roads.

city-gps.txt contains one line per city, with three fields per line, 
delimited by spaces. The first field is the city, followed by the latitude,
followed by the longitude.

road-segments.txt has one line per road segment connecting two cities.
The space delimited fields are:

- first city
- second city
- length (in miles)
- speed limit (in miles per hour)
- name of highway


## 1) Abstractions
State Space – Set of all valid cities one can travel from start city to destination city.
Initial States – The initial city before performing A* search.
Successor Function – Set of neighbouring cities one can travel from the previous city.
Goal State – This is the state where we reach the destination city through the given cost function.
Cost Function – The cost function is one of shortest distance, shortest time, shortest segments and shortest delivery.

## 2) Additional Conditions
If a delivery truck travels at a speed >50, there is a chance a package may fall out. Initially, we use the same heuristic as time and later we implement a function to calculate the extra time to deliver including the rerouting to the start city.

## 3) Overview
Our approach uses FRINGE as the data structure with cost, route_taken, total_miles, total_segments and total_hours. We implement Search Algorithm #3 which implements the "cleanup" step.

## 4)Heuristics used:
a) Distance - Haversine Distance is used as the heuristic to calculate the distance between the current city and the destination.
b) Time - The maximum speed of all road segments is found and divided by the distance of the current road segment. 
c) Delivery - The heuristic used for delivery is the same as that of time since we want to find the fastest route for delivery too.
d) Segment - The heuristic for segment is simple. It is just a 1 to every fringe.
 
## 5) The algorithm is given below –
The algorithm used below is the Search Algorithm #3 taught by Prof. David Crandall.
I.	Initialise a FRINGE with 5 values- with cost, route_taken, total_miles, total_segments and total_hours.
II.	Pop the node with the smallest cost value.
III.Find the neighbour cities and check if they are valid.
IV.	Calculate the cost for the neighbour and add it to the fringe if it is not already visited.
    - Cost is found for 4 different cost functions with their respective heuristics.
V. Check if the neighbour city is visited and whether the cost is less than the city cost
    -Append this neighbour city to the fringe.
VI.	Sort the fringe according to the lowest cost.
VII.	Run the search algorithm until it hits a goal, if it doesn’t reach the goal, return Failure.
VIII.If the Goal is hit, find the delivery hours using a seperate function.
IX.  Return the final dictinoary with route-taken, total-miles, total-hours, total-segments, total-delivery hours
