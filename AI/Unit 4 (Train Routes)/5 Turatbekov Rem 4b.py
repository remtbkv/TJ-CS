import sys
from distanceDemo import calcd
from heapq import heappush, heappop
from time import perf_counter
import tkinter as tk

nodeId, nodeLocation, nodeConnections = {}, {}, {}

starttime = perf_counter()
with open("rrNodeCity.txt") as f:
    for l in f:
        id, city = l[:7], l[8:-1]
        nodeId[city] = id

with open("rrNodes.txt") as f:
    for l in f:
        n, lat, long = l.strip().split(" ")
        nodeLocation[n] = (float(lat), float(long))

with open("rrEdges.txt") as f:
    for l in f:
        first, second = l.strip().split(" ")
        d = calcd(nodeLocation[first], nodeLocation[second])
        if first not in nodeConnections:
            nodeConnections[first] = {(second, d)}
        else:
            nodeConnections[first].add((second, d))
        if second not in nodeConnections:
            nodeConnections[second] = {(first, d)}
        else:
            nodeConnections[second].add((first, d))
timetaken = perf_counter()-starttime

def dijkstra(start_node, goal_node, r, c):
    start_id, goal_id = nodeId[start_node], nodeId[goal_node]
    closed, fringe, node = set(), [], (0, start_id, [start_id])
    heappush(fringe, node)
    while fringe:
        length, state, path = heappop(fringe)
        if state == goal_id:
            make_color(r, c, path, "orange")
            return length
        if state not in closed:
            closed.add(state)
            for childState, distance in nodeConnections[state]:
                if childState not in closed:
                    change_color(c, line_connections[(state, childState)], "red")
                    heappush(fringe, (length+distance, childState, path+[childState]))
    return None


def taxi(node1, goal_node):
    return calcd(nodeLocation[node1], nodeLocation[goal_node])


def astar(start_node, goal_node, r, c):
    start_id, goal_id = nodeId[start_node], nodeId[goal_node]
    closed, fringe, node = set(), [], (taxi(start_id, goal_id), start_id, 0, [start_id])
    heappush(fringe, node)
    while fringe:
        t, state, length, path = heappop(fringe)
        if state == goal_id:
            make_color(r, c, path, "pink")
            return length
        if state not in closed:
            closed.add(state)
            for childState, distance in nodeConnections[state]:
                if childState not in closed:
                    temp = (length+distance+taxi(childState, goal_id),childState, length+distance, path+[childState])
                    change_color(c, line_connections[(state, childState)], "blue")
                    heappush(fringe, temp)
    return None



def create_map(r, c):
    for node, connections in nodeConnections.items():
        for node2, d in connections:
            if (node, node2) not in line_connections and (node2, node) not in line_connections:
                lat1, long1 = nodeLocation[node]
                lat2, long2 = nodeLocation[node2]
                con = size//80
                lat1 *= con
                long1 *= con
                lat2 *= con
                long2 *= con
                x1, y1, x2, y2 = size+long1+size*0.7125, size-lat1, size+long2+size*0.7125, size-lat2
                line = c.create_line([(x1, y1), (x2, y2)], tag='grid_line')
                c.itemconfig(line, fill="black")
                line_connections[(node, node2)], line_connections[(node2, node)] = line, line
    r.update()

def change_color(c, line, color):
    global count
    c.itemconfig(line, fill=color)
    if count%2000==0:
        root.update()
    count+=1

def make_color(r, c, path, color):
    for i in range(len(path)-1):
        c.itemconfig(line_connections[(path[i], path[i+1])], fill=color)
    r.update()

root = tk.Tk()
button = tk.Button(root, text='NEXT', height=2, width=10, command=root.quit)
button.pack()
size = 1000
canvas = tk.Canvas(root, height=size, width=size, bg='white')
line_connections = {}
create_map(root, canvas)
canvas.pack(expand=True)



start, end = sys.argv[1], sys.argv[2]
global count
count = 0
# start, end = "Ciudad Juarez", "Montreal"
s = perf_counter()
d = dijkstra(start, end, root, canvas)
dt = perf_counter()-s
print(f"{start} to {end} with Dijkstra: {d} in {dt} seconds.")
root.mainloop()

s = perf_counter()
a = astar(start, end, root, canvas)
at = perf_counter()-s
print(f"{start} to {end} with A*: {a} in {at} seconds.")
root.mainloop()

