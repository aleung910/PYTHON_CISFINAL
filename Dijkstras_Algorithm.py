import MTAdata

stopGraph = MTAdata.graph_weight(MTAdata.build_graph())
 
def dijkstra(graph,start,goal):
    shortest_distance = {}
    predecessor = {}
    unseenNodes = graph
    infinity = 9999999
    path = []
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0
 
    while unseenNodes:
        minNode = None
        for node in unseenNodes:
            if minNode is None:
                if node[:2] == "N " or node[:2] == "S ":
                    minNode = node[2:]
                else:
                    minNode = node
            elif shortest_distance[node] < shortest_distance[minNode]:
                if node[:2] == "N " or node[:2] == "S ":
                    minNode = node[2:]
                else:
                    minNode = node
 
        for childNode, weight in graph[minNode].items():
            if childNode[:2] == "N " or childNode[:2] == "S ":
                childNode = childNode[2:]
            if weight + shortest_distance[minNode] < shortest_distance[childNode]:
                shortest_distance[childNode] = weight + shortest_distance[minNode]
                predecessor[childNode] = minNode
        unseenNodes.pop(minNode)
 
    currentNode = goal
    while currentNode != start:
        try:
            path.insert(0,currentNode)
            currentNode = predecessor[currentNode]
        except KeyError:
            print('Path not reachable')
            break
    path.insert(0,start)
    if shortest_distance[goal] != infinity:
        print(f'Shortest distance is {shortest_distance[goal] // 60} minutes')
        print(f'And the path is {path}')
 
 
dijkstra(stopGraph, 'Van Cortlandt Park-242 St', '14 St-Union Sq')