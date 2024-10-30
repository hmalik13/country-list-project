from flask import Flask, jsonify
from collections import deque

# define the given country borders
edges = [["USA", "CAN"], ["USA", "MEX"], ["MEX", "GTM"], ["MEX", "BLZ"], ["BLZ", "GTM"], ["GTM", "SLV"],
         ["GTM", "HND"], ["SLV", "HND"], ["HND", "NIC"], ["NIC", "CRI"], ["CRI", "PAN"]]

# build the adjacency list
adjList = {}

for src, dst in edges:
    if src not in adjList:
        adjList[src] = []
    if dst not in adjList:
        adjList[dst] = []
    adjList[src].append(dst)

# breadth first search
# find path from USA to given country
def bfs(node, target, adjList):
    visit = set()
    visit.add(node)
    queue = deque()
    # each item in the queue is a tuple, each tuple contains the current node and a list containing the path
    queue.append((node, [node]))

    while queue:
        for i in range(len(queue)):
            cur, path = queue.popleft()
            if cur == target:
                return path
        
            for neighbor in adjList[cur]:
                if neighbor not in visit:
                    visit.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
    return []

# set up flask app
app = Flask(__name__)

@app.route("/")
def root():
    return "Please add a country code to the end of the url"

@app.route("/<country_code>")
def countrylist(country_code):
    path = bfs("USA", country_code, adjList)
    return jsonify(path)

