import sys
import time
import math
from math import pi , acos , sin , cos
from heapq import heappush, heappop, heapify
import tkinter as tk

dict_city_junction = {}
dict_city_coordinates = {}
dict_node_city = {}
lines = {}

with open("rrEdges.txt") as f:
    edges = [line.strip() for line in f]

with open("rrNodes.txt") as f:
    nodes = [line.strip() for line in f]

with open("rrNodeCity.txt") as f:
    nodeCity = [line.strip() for line in f]

for node in nodes:
    line_split = node.split(" ")
    junct = line_split[0]
    lat = float(line_split[1])
    long = float(line_split[2])
    dict_city_coordinates[junct] = (lat, long)

def create_map(r, c):
    size=800
    for node, connections in dict_city_junction.items():
        for node2, d in connections:
            if (node, node2) not in lines and (node2, node) not in lines:
                lat1, long1 = dict_city_coordinates[node]
                lat2, long2 = dict_city_coordinates[node2]
                con = size//80
                lat1 *= con
                long1 *= con
                lat2 *= con
                long2 *= con
                x1=800-(long1 * -1-600)
                y1=800 - lat1
                x2=800-(long2 * - 1-600)
                y2 = 800 - lat2
                # x1, y1, x2, y2 = size+long1+size*0.7125, size - lat1, size+long2+size*0.7125, size-lat2
                line = c.create_line([(x1, y1), (x2, y2)], tag='grid_line')
                c.itemconfig(line, fill="black")
                lines[(node, node2)], lines[(node2, node)] = line, line
    r.update()

def create_grid(r, c):
    print(edges)
    for line in edges:
        line_split = line.split(" ")
        city1 = line_split[0]
        city2 = line_split[1]
        
        city1lat, city1long = dict_city_coordinates.get(city1)
        city2lat, city2long = dict_city_coordinates.get(city2)

        city1lat *= 10
        city1long *= 10
        city2lat *= 10
        city2long *= 10

        line2 = c.create_line([(800-(city1long * -1-600), 800 - city1lat), (800-(city2long * - 1-600), 800 - city2lat)], tag='grid_line')
        lines[(city1, city2)] = line2
        lines[(city2, city1)] = line2

    r.update()

count2 = 0
def make_red(r, c, state, ch):
    global count2
    count2 = count2 + 1
    line = lines.get((state, ch))
    c.itemconfig(line, fill="red") 

    if(count2 % 1000 == 0):
        r.update()

count6 = 0
def make_blue(r, c, state, ch):
    global count6
    count6 = count6 + 1
    line = lines.get((state, ch))
    c.itemconfig(line, fill="blue") 

    if(count6 % 500 == 0):
        r.update()

count4 = 0
def make_green(r, c, ancestors):
    global count4
    for i in range(len(ancestors) - 1):
        state = ancestors[i]
        ch = ancestors[i + 1]
        count4 = count4 + 1
        line = lines.get((state, ch))
        c.itemconfig(line, fill="green") 

        if(count4 % 50 == 0):
            r.update()
    
count8 = 0
def make_orange(r, c, ancestors):
    global count8
    for i in range(len(ancestors) - 1):
        state = ancestors[i]
        ch = ancestors[i + 1]
        count8 = count8 + 1
        line = lines.get((state, ch))
        c.itemconfig(line, fill="orange") 

        if(count8 % 25 == 0):
            r.update()

root = tk.Tk()

canvas = tk.Canvas(root, height=800, width=800, bg='white')
# create_grid(root, canvas)


start3 = time.perf_counter()

def calcd(node1, node2):
   y1, x1 = node1
   y2, x2 = node2

   if((x1 == x2) and (y1 == y2)):
       return 0.0

   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

for line in edges:
    line_split = line.split(" ")
    city1 = line_split[0]
    city2 = line_split[1]
    
    city1lat, city1long = dict_city_coordinates.get(city1)
    city2lat, city2long = dict_city_coordinates.get(city2)    

    dist = calcd(dict_city_coordinates.get(city1), dict_city_coordinates.get(city2))

    if(city1 in dict_city_junction):
        junct_list = dict_city_junction.get(city1)
        elem = dict_city_junction.pop(city1, "ERROR")
        junct_list.append((city2, dist))
        dict_city_junction[city1] = junct_list

    else:
        dict_city_junction[city1] = [(city2, dist)]
    
    if(city2 in dict_city_junction):
        junct_list = dict_city_junction.get(city2)
        elem = dict_city_junction.pop(city2, "ERROR")
        junct_list.append((city1, dist))
        dict_city_junction[city2] = junct_list

    else:
        dict_city_junction[city2] = [(city1, dist)]

for city in nodeCity:
    cityList = city.split(" ")
    junct = cityList[0]
    cityItself = ' '.join(cityList[1:])
    dict_node_city[cityItself] = junct

end3 = time.perf_counter()
times3 = str(end3 - start3)
print("Time to build backing data structures: " + times3 + " seconds.")


def dijkstra(start_junct, end_junct):
    closed = set()
    fringe = []
    heappush(fringe, (0, start_junct, [start_junct]))

    while fringe:
        depth, state, ancestors = heappop(fringe)

        if(state == end_junct):
            make_green(root, canvas, ancestors)
            return depth
        
        if(state not in closed):
            closed.add(state)
            for c, cDist in dict_city_junction.get(state):
                if c not in closed:
                    make_red(root, canvas, state, c)
                    heappush(fringe, (depth + cDist, c, ancestors+[c]))
    return None

def astar(start_junct, end_junct):
    closed = set()
    fringe = []
    heappush(fringe, (0, 0, start_junct, [start_junct]))

    while fringe:
        heuristic, depth, state, ancestors = heappop(fringe)

        if(state == end_junct):
            make_orange(root, canvas, ancestors)
            return depth
        
        if(state not in closed):
            closed.add(state)
            children_list = dict_city_junction.get(state)
            iter = 0
            for cAll in children_list:
                c, cDist = children_list[iter]
                cLat, cLong = dict_city_coordinates.get(c)
                make_blue(root, canvas, state, c)
                c, cDist = children_list[iter]

                if c not in closed:
                    c_ancestors = ancestors.copy()
                    c_ancestors.append(c)
                    new_f = calcd(dict_city_coordinates.get(c), dict_city_coordinates.get(end_junct))
                    new_depth = depth + cDist
                    heappush(fringe, (new_f + new_depth, new_depth, c, c_ancestors))

                iter = iter + 1

    return None

# city1 = sys.argv[1]
# city2 = sys.argv[2]


city1, city2 = "Ciudad Juarez", "Montreal"

start = time.perf_counter()
create_map(root, canvas)
canvas.pack(expand=True)
coord1 = dict_node_city.get(city1)
coord2 = dict_node_city.get(city2)
dist1 = dijkstra(coord1, coord2)

# end = time.perf_counter()
# times = str(end - start)

# print(city1 + " to " + city2 + " with Dijkstra: " + str(dist1) + " in " + times + " seconds.")
# time.sleep(5)

# start2 = time.perf_counter()
# dist2 = astar(coord1, coord2)
# end2 = time.perf_counter()
# times2 = str(end2 - start2)

# print(city1 + " to " + city2 + " with A*: " + str(dist2) + " in " + times2 + " seconds.")

root.mainloop()