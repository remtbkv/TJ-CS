import sys
from distanceDemo import calcd
from heapq import heappush, heappop
from time import perf_counter
import tkinter

nodeLocation, nodeConnections, nodeId = {}, {}, {}

starttime=perf_counter()
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
            nodeConnections[first].add((second,d))
        if second not in nodeConnections:
            nodeConnections[second] = {(first, d)}
        else:
            nodeConnections[second].add((first, d))
timetaken = perf_counter()-starttime

def dijkstra(start_node, goal_node):
    start_node, goal_node = nodeId[start_node], nodeId[goal_node]
    closed, fringe, node = set(), [], (0, start_node)
    heappush(fringe, node)
    while fringe:
        length, state = heappop(fringe)
        if state == goal_node:
            return length
        if state not in closed:
            closed.add(state)
            for childState, distance in nodeConnections[state]:
                if childState not in closed:
                    temp = (length+distance, childState)
                    heappush(fringe, temp)
    return None


def taxi(node1, goal_node):
    return calcd(nodeLocation[node1], nodeLocation[goal_node])

def astar(start_node, goal_node):
    start_node, goal_node = nodeId[start_node], nodeId[goal_node]
    closed, fringe, node = set(), [], (taxi(start_node, goal_node), start_node, 0)
    heappush(fringe, node)
    while fringe:
        t, state, length = heappop(fringe)
        if state == goal_node:
            return length
        if state not in closed:
            closed.add(state)
            for childState, distance in nodeConnections[state]:
                if childState not in closed:
                    temp = (length+distance+taxi(childState, goal_node), childState, length+distance)
                    heappush(fringe, temp)
    return None


print("Time to create data structure:",timetaken)

start, end = sys.argv[1], sys.argv[2]
# start, end = "Albuquerque","Atlanta"
s = perf_counter()
d = dijkstra(start, end)
dt = perf_counter()-s

s = perf_counter()
a = astar(start, end)
at = perf_counter()-s

print(f"{start} to {end} with Dijkstra: {d} in {dt} seconds.")
print(f"{start} to {end} with A*: {a} in {at} seconds.")