import map
import heapq

edge_cost = {edge: map.length_for_edge(edge, 1000) for edge in map.edges}
graph = {}
for edge, (start, end, _) in map.edges.items():
    if start not in graph:
        graph[start] = {}
    graph[start][end] = sum(edge_cost[edge])

# given two edges, return the shortest path between them
# the path is a list of nodes
# it uses the edge_cost dict from map for evaluation
def plan_route_to(target_node, current_edge):
    start_node = map.edges[current_edge][1]
    
    distance = {node: float('inf') for node in map.nodes.keys()}
    distance[start_node] = 0
    heap = [(0, start_node)]
    previous = {node: None for node in graph}

    while heap:
        dist, current = heapq.heappop(heap)

        if dist > distance[current]:
            continue

        if current == target_node:
            break

        for neighbor, cost in graph[current].items():
            new_distance = dist + cost
            if new_distance < distance[neighbor]:
                distance[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(heap, (new_distance, neighbor))

    # Reconstruct the path
    path = []
    while target_node is not None:
        path.append(target_node)
        target_node = previous[target_node]

    path.reverse()
    return path

    