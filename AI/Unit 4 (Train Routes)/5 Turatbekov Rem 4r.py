import sys
from distanceDemo import calcd
from heapq import heappush, heappop
import tkinter as tk
from tkinter import ttk
from collections import deque

nodeLocation, nodeConnections, nodeId, line_connections = {}, {}, {}, {}

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

def create_map():
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
                x1, y1, x2, y2 = size+long1+size*0.7125, size - lat1, size+long2+size*0.7125, size-lat2
                line = canvas.create_line([(x1, y1), (x2, y2)], tag='grid_line')
                canvas.itemconfig(line, fill="black")
                line_connections[(node, node2)] = line
                line_connections[(node2, node)] = line
    root.update()

def change_color(line, color, iddfs=False):
    global count, speed
    canvas.itemconfig(line, fill=color)
    if not iddfs:
        if count % speed == 0:
            root.update()
        count += 1

def make_color(path, color):
    for i in range(len(path)-1):
        canvas.itemconfig(line_connections[(path[i], path[i+1])], fill=color)
    root.update()


def dijkstra(start_node, goal_node):
    start_id, goal_id = nodeId[start_node], nodeId[goal_node]
    closed, fringe, node = set(), [], (0, start_id, [start_id])
    heappush(fringe, node)
    while fringe:
        length, state, path = heappop(fringe)
        if state == goal_id:
            make_color(path, "orange")
            return length
        if state not in closed:
            closed.add(state)
            for childState, distance in nodeConnections[state]:
                if childState not in closed:
                    temp = (length+distance, childState, path+[childState])
                    change_color(line_connections[(state, childState)], "red")
                    heappush(fringe, temp)
    return None


def taxi(node1, goal_node):
    return calcd(nodeLocation[node1], nodeLocation[goal_node])


def astar(start_node, goal_node):
    start_id, goal_id = nodeId[start_node], nodeId[goal_node]
    closed, fringe, node = set(), [], (taxi(start_id, goal_id), start_id, 0, [start_id])
    heappush(fringe, node)
    while fringe:
        t, state, length, path = heappop(fringe)
        if state == goal_id:
            make_color(path, "pink")
            return length
        if state not in closed:
            closed.add(state)
            for childState, distance in nodeConnections[state]:
                if childState not in closed:
                    temp = (length+distance+taxi(childState, goal_id),childState, length+distance, path+[childState])
                    change_color(line_connections[(state, childState)], "blue")
                    heappush(fringe, temp)
    return None


def DFS(start_node, goal_node):
    start_id, goal_id, fringe, ancestors = nodeId[start_node], nodeId[goal_node], deque(), set()
    ancestors.add(start_id)
    fringe.append((start_id, 0, [start_id]))
    while fringe:
        state, length, path = fringe.pop()
        if state == goal_id:
            make_color(path, "orange")
            return length
        for childState, distance in nodeConnections[state]:
            if childState not in ancestors:
                change_color(line_connections[(state, childState)], "blue")
                fringe.append((childState, length+distance, path+[childState]))
                ancestors.add(childState)
    return None


def kDFS(start_id, goal_id, k):
    fringe = []
    ancestors = set()
    ancestors.add(start_id)
    fringe.append((start_id, 0, [start_id]))
    while fringe:
        state, length, path = fringe.pop()
        if state == goal_id:
            make_color(path, "orange")
            return length
        if length < k:
            for childState, distance in nodeConnections[state]:
                if childState not in ancestors:
                    ancestors.add(childState)
                    changed.append(line := line_connections[(state, childState)])
                    change_color(line, "blue", iddfs=True)
                    fringe.append((childState, length+distance, path+[childState]))
    return None


def ID_DFS(start_node, goal_node):
    global changed
    changed = []
    start_id, goal_id = nodeId[start_node], nodeId[goal_node]
    max_depth = 0
    result = None
    while result is None:
        result = kDFS(start_id, goal_id, max_depth)
        root.update()
        if not result:
            while changed:
                change_color(changed.pop(), "black", iddfs=True)
        root.update()
        max_depth += 200
    return result


def reverse_astar(start_node, goal_node):
    start_id, goal_id = nodeId[start_node], nodeId[goal_node]
    closed, fringe, node = set(), [], (-taxi(start_id, goal_id), start_id, 0, [start_id])
    heappush(fringe, node)
    while fringe:
        t, state, length, path = heappop(fringe)
        if state == goal_id:
            make_color(path, "pink")
            return length
        if state not in closed:
            closed.add(state)
            for childState, distance in nodeConnections[state]:
                if childState not in closed:
                    temp = (-(length+distance+taxi(childState, goal_id)),
                            childState, length+distance, path+[childState])
                    change_color(line_connections[(state, childState)], "blue")
                    heappush(fringe, temp)
    return None


def BiDijkstra(start_node, goal_node):
    start_id, goal_id = nodeId[start_node], nodeId[goal_node]
    s_fringe, e_fringe = [], []
    heappush(s_fringe, (0, start_id, [start_id]))
    heappush(e_fringe, ((0, goal_id, [goal_id])))
    s_visit, e_visit = {start_id: 0}, {goal_id: 0}
    s_visitPath, e_visitPath = {start_id: [start_id]}, {goal_id: [goal_id]}

    while s_fringe and e_fringe:
        s_length, s_state, s_path = heappop(s_fringe)
        e_length, e_state, e_path = heappop(e_fringe)

        for c, d in nodeConnections[s_state]:
            if c not in s_visit:
                change_color(line_connections[(s_state, c)], "blue")
                s_visit[c], s_visitPath[c] = s_length+d, s_path+[c]
                heappush(s_fringe, (s_visit[c], c, s_visitPath[c]))
            if c in e_visit:
                make_color(e_visitPath[c]+s_path[::-1], "orange")
                return
                # return s_visit[c] + e_visit[c]

        for c, d in nodeConnections[e_state]:
            if c not in e_visit:
                change_color(line_connections[(e_state, c)], "blue")
                e_visit[c], e_visitPath[c] = e_length+d, e_path+[c]
                heappush(e_fringe, (e_visit[c], c, e_visitPath[c]))
            if c in s_visit:
                make_color(s_visitPath[c]+e_path[::-1], "orange")
                return
                # return s_visit[c] + e_visit[c]
    return None


def BiAstar(start_node, goal_node):
    start_id, goal_id = nodeId[start_node], nodeId[goal_node]
    s_fringe, e_fringe = [], []
    heappush(s_fringe, (taxi(start_id, goal_id), 0, start_id, [start_id]))
    heappush(e_fringe, (taxi(goal_id, start_id), 0, goal_id, [goal_id]))
    s_visit, e_visit = {start_id: 0}, {goal_id: 0}
    s_visitPath, e_visitPath = {start_id: [start_id]}, {goal_id: [goal_id]}

    while s_fringe and e_fringe:
        s_t, s_length, s_state, s_path = heappop(s_fringe)
        e_t, e_length, e_state, e_path = heappop(e_fringe)

        for c, d in nodeConnections[s_state]:
            if c not in s_visit:
                change_color(line_connections[(s_state, c)], "blue")
                s_visit[c], s_visitPath[c] = s_length+d, s_path+[c]
                heappush(s_fringe, (s_visit[c]+taxi(c, goal_id), s_visit[c], c, s_visitPath[c]))
            if c in e_visit:
                make_color(e_visitPath[c]+s_path[::-1], "orange")
                return

        for c, d in nodeConnections[e_state]:
            if c not in e_visit:
                change_color(line_connections[(e_state, c)], "blue")
                e_visit[c], e_visitPath[c] = e_length+d, e_path+[c]
                heappush(e_fringe, (e_visit[c]+taxi(c, start_id), e_visit[c], c, e_visitPath[c]))
            if c in s_visit:
                make_color(s_visitPath[c]+e_path[::-1], "orange")
                return
    return None


def dijkstra_command():
    global speed
    speed = 2000
    dijkstra(start, end)

def astar_command():
    global speed
    speed = 1500
    astar(start, end)

def dfs_command():
    global speed
    speed = 2000
    DFS(start, end)

def iddfs_command():
    global speed
    speed = 4000
    ID_DFS(start, end)

def reverse_astar_command():
    global speed
    speed = 2000
    reverse_astar(start, end)

def bidi_command():
    global speed
    speed = 5000
    BiDijkstra(start, end)

def bia_command():
    global speed
    speed = 250
    BiAstar(start, end)

def reset_command():
    for line in line_connections.values():
        canvas.itemconfig(line, fill="black")
    root.update()

def on_algorithm_select(event):
    selected_algorithm = algorithm_combo.get()
    if selected_algorithm == "Dijkstra":
        dijkstra_command()
    elif selected_algorithm == "A*":
        astar_command()
    elif selected_algorithm == "DFS":
        dfs_command()
    elif selected_algorithm == "ID DFS":
        iddfs_command()
    elif selected_algorithm == "Reverse A*":
        reverse_astar_command()
    elif selected_algorithm == "Bi Dijkstra":
        bidi_command()
    elif selected_algorithm == "Bi A*":
        bia_command()

global count
count = 0
start, end = sys.argv[1], sys.argv[2]

root = tk.Tk()

algorithm_options = ["Dijkstra", "A*", "DFS", "ID DFS", "Reverse A*", "Bi Dijkstra", "Bi A*"]
algorithm_combo = ttk.Combobox(root, values=algorithm_options, state="readonly")
algorithm_combo.set("Select an algorithm")
algorithm_combo.pack(padx=10, pady=10)
algorithm_combo.bind("<<ComboboxSelected>>", on_algorithm_select)

button = tk.Button(root, text='Quit', height=2, width=15, command=root.quit)
button.pack()
reset = tk.Button(root, text='Reset Graph', height=2, width=15, command=reset_command)
reset.pack()

size = 800
canvas = tk.Canvas(root, height=size, width=size, bg='white')
canvas.pack(expand=True)
create_map()

root.mainloop()
