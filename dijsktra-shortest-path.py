from collections import defaultdict
import heapq
from typing import List, Tuple

class Node:
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self) -> str:
        return self.name
    
    def __lt__(self, node) -> bool: ##for heapq compare
        return self.name < node.name

class Edge:
    def __init__(self, name: str, node1: Node, node2: Node, time: int):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.time = time

class Train:
    def __init__(self, name: str, capacity: int, start: Node):
        self.name = name
        self.capacity = capacity
        self.start = start
        self.currentTime = 0

class Package:
    def __init__(self, name: str, weight: int, start: Node, end: Node):
        self.name = name
        self.weight = weight
        self.start = start
        self.end = end

class Network:
    def __init__(self):
        self.network = defaultdict(list)

    def addEdge(self, name: str, node1: Node, node2: Node, time: int):
        self.network[node1].append((node2, time, name))
        self.network[node2].append((node1, time, name))

    def dijkstra(self, start: Node):
        durations = {node: float('inf') for node in self.network}  # initialize durations as infinity
        durations[start] = 0  # duration from start to start is 0
        
        priorityQueue = [(0, start)] 

        while priorityQueue:
            currentDuration, currentNode = heapq.heappop(priorityQueue)  # pop the smallest duration
            if currentDuration > durations[currentNode]:  # if greater, skip
                continue 
            
            # check neighbors
            for node, time, name in self.network[currentNode]:
                if durations[node] > time + durations[currentNode]:
                    durations[node] = time + durations[currentNode]  # update if found shorter
                    heapq.heappush(priorityQueue, (time + durations[currentNode], node))  # push to queue to find potential shorter path
            
        return durations

def findShortestPath(network: Network, startNode: Node, endNode: Node):
    durations = network.dijkstra(startNode)  # get shortest path from start to all nodes
    path = []
    currentNode = endNode
    
    while currentNode != startNode:
        for neighbor, time, edgeName in network.network[currentNode]:
            if durations[currentNode] - time == durations[neighbor]:  # find the optimal direct connection based on Dijkstra's result
                path.append((neighbor, currentNode, time, edgeName))
                currentNode = neighbor
                break
    
    path.reverse()
    return path

def handleInput() -> Tuple[List[Node], List[Edge], List[Train], List[Package]]:
    try:
        nodes = []
        edges = []
        trains = []
        packages = []
        nodeName = {}

        numNodes = int(input("Enter the number of nodes:"))
        print("Enter the node name:")
        for i in range(numNodes):
            name = input()
            node = Node(name)
            nodes.append(node)
            nodeName[name] = node 
        
        numEdges = int(input("Enter the number of edges:"))
        print("Enter the name,node1,node2,time:")
        for i in range(numEdges):
            inputData = input().split(",")
            if len(inputData) != 4:
                raise Exception("invalid input format")
            name = inputData[0].strip()
            node1 = inputData[1].strip()
            node2 = inputData[2].strip()
            time = int(inputData[3].strip())
            #checking
            if node1 not in nodeName or node2 not in nodeName:
                raise Exception("invalid node")
            
            edge = Edge(name, nodeName[node1], nodeName[node2], time)
            edges.append(edge)

        numPackages = int(input("Enter the number of packages:"))
        print("Enter the name,weight(kg),start,end:")
        for i in range(numPackages):
            inputData = input().split(",")
            if len(inputData) != 4:
                raise Exception("invalid input format")
            name = inputData[0].strip()
            weight = int(inputData[1].strip())
            start = inputData[2].strip()
            end = inputData[3].strip()
            #checking
            if start not in nodeName or end not in nodeName:
                raise Exception("invalid node")
            
            package = Package(name, weight, nodeName[start], nodeName[end])
            packages.append(package)
        
        numTrains = int(input("Enter the number of trains: "))
        print("Enter the name,capacity(kg),start:")
        for i in range(numTrains):
            inputData = input().split(",")
            if len(inputData) != 3:
                raise Exception("invalid input format")
            
            name = inputData[0].strip()
            capacity = int(inputData[1].strip())
            start = inputData[2].strip()
            ##checking
            if start not in nodeName:
                raise Exception("invalid node")
            
            train = Train(name, capacity, nodeName[start])
            trains.append(train)

        return nodes, edges, trains, packages
    except Exception as e:
        print(e)
        return [], [], [], []

def planMoves(network: Network, trains: List[Train], packageGroup: List[Package]):
    moves = []
    
    if not packageGroup:
        return moves

    startNode = packageGroup[0].start
    endNode = packageGroup[0].end

    packageGroup.sort(key=lambda p: p.weight, reverse=True)  # sort packages by weight
    
    while packageGroup:
        optimalTrain = None
        minExtraDistance = float('inf')
        
        # find the optimal train to pick up this group of packages
        for train in trains:
            if train.start == startNode:
                optimalTrain = train
                break
            else:
                pathToPickup = findShortestPath(network, train.start, startNode)
                extraDistance = sum(journeyTime for node1, node2, journeyTime, edgeName in pathToPickup)
                if extraDistance < minExtraDistance:
                    minExtraDistance = extraDistance
                    optimalTrain = train

        if not optimalTrain:
            print(f"No suitable train found for packages {', '.join(p.name for p in packageGroup)}. Skipping.")
            break

        # move optimalTrain to pick up point if it's not already there
        if optimalTrain.start != startNode:
            pathToPickup = findShortestPath(network, optimalTrain.start, startNode)
            for node1, node2, journeyTime, edgeName in pathToPickup:
                if node1 != node2:  # move only if nodes are different
                    moves.append((optimalTrain.currentTime, optimalTrain.name, node1.name, [], node2.name, []))
                    optimalTrain.currentTime += journeyTime
            optimalTrain.start = startNode  # update train start point

        # pick up packages until train capacity is full or no more packages in group
        pickedWeight = 0
        pickedPackages = []
        for package in packageGroup[:]:
            if pickedWeight + package.weight <= optimalTrain.capacity:
                pickedPackages.append(package)
                pickedWeight += package.weight
                packageGroup.remove(package)
            else:
                break

        # move to delivery point
        pathToDeliver = findShortestPath(network, startNode, endNode)
        for i, (node1, node2, journeyTime, edgeName) in enumerate(pathToDeliver):
            if node1 != node2:
                if i == len(pathToDeliver)-1: ##last stop, drop off
                    moves.append((optimalTrain.currentTime, optimalTrain.name, node1.name, [], node2.name, [p.name for p in pickedPackages]))
                else:
                    moves.append((optimalTrain.currentTime, optimalTrain.name, node1.name, [p.name for p in pickedPackages], node2.name, []))
                optimalTrain.currentTime += journeyTime
        optimalTrain.start = endNode  # update train start position after delivery

    return moves


def formatMoves(moves):
    formattedMoves = []
    for move in moves:
        W, T, N1, P1, N2, P2 = move
        formattedMoves.append(f"W={W}, T={T}, N1={N1}, P1={P1}, N2={N2}, P2={P2}")
    return formattedMoves

def main():
    nodes, edges, trains, packages = handleInput()
    if not nodes or not edges or not trains or not packages:
        return
    
    # construct network
    network = Network()
    for edge in edges:
        network.addEdge(edge.name, edge.node1, edge.node2, edge.time)

    # group packages by (start, end) pairs (i made little assumption to simplify question: no pickup in the middle of transit)
    packageGroups = defaultdict(list)
    for package in packages:
        packageGroups[(package.start, package.end)].append(package)

    allMoves = []
    for packageGroup in packageGroups.values():
        moves = planMoves(network, trains, packageGroup)
        allMoves.extend(moves)

    formattedMoves = formatMoves(allMoves)
    for move in formattedMoves:
        print(move)

if __name__ == "__main__":
    main()
