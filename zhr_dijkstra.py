import json
import math
import heapq as hq  # using heapq in python

# – Lines 5 to 9 show the initialization. INF is initialized to half of the maximum value of a signed 64 bit integer (a signed 64 bit integer can display integers from -2^{63} to (2^{63} - 1).
# – In lines 9 and 10 we initialize a priority queue and insert the tuple (dist[source], source) since we start with the source node.
# – Lines 12 to 25 implement the repeating loop. In line 13 we try to find the next node with the smallest distance value. We do this with a priority queue. In line 16 we discard “wrong tuples”, see also Part 3a.
# – Lines 17 and 18 are optional. They make the algorithm stop once the minimum distance for the target node has been found. Note though that if you uncomment these lines the distances to other nodes beside the target node are not necessarily found, so uncomment these lines only if you are interested in a particular target node.
# – In line 27 we check whether a path has been found.
# – In lines 30 to 38 we reconstruct the shortest path with the help of the predecessor dictionary.
In particular this is done in lines 32 to 36 where we follow the shortest path backwards from the target to the source. We recognize the source by checking if pred[node] == node, see also the way we initialized the predecessor dictionary in line 6.
# version1:
# input: source and target id
# ouput: null (print out shortest path and distance)
def dijkstra1(adj, source, target):
    # store the predecessor of all nodes, init with itself
    pred = {x: x for x in adj}
    # store the all min distitance of all nodes, init with infinity
    dist = {x: math.inf for x in adj}
    # initialize
    dist[source] = 0
    heap = []
    hq.heappush(heap, [dist[source], source])
    while heap:
        u = hq.heappop(heap)  # u is a list [u_dist, u_id]
        u_dist = u[0]
        u_id = u[1]
        if u_dist == dist[u_id]:
            for v in adj[u_id]:
                v_id = v[0]
                w_uv = v[1]
                if dist[u_id] + w_uv < dist[v_id]:
                    dist[v_id] = dist[u_id] + w_uv
                    hq.heappush(heap, [dist[v_id], v_id])  # decrease key
                    pred[v_id] = u_id
    if dist[target] == math.inf:
        # cannot find path
        print("There is no path between ", source, "and", target)
    else:
        reversed_path = []
        # find predecessor from target
        node = target
        while True:
            reversed_path.append(str(node))
            if(node == pred[node]):
                break
            node = pred[node]
        # reverse
        path = reversed_path[::-1]
        print("The shortest path is " + " ".join(path) + "\n")
        print(
            f"The distance from {source} to {target} is {str(dist[target])}\n")
        # print("distance dictionary: " + str(dist) + "\n")
        # print("predecessor dictionary: " + str(pred))
'''
=======================================================================================================
example output:
The shortest path is 61321094 61326611 2742760181 61329243 
1527349492 61329241 1527349497 1527349495 61326713 327675602 
61325632 1525366585 1525366589 1525366599 278950006 61328210 
1525366587 61331800 278949805 278949806 1525366591 278949808...

The distance from 61321094 to 257734747 is 2.914441255129966
=======================================================================================================
'''
# version2:
# input: source and target address
# ouput: a tuple, contains shortest path and distance
def dijkstra(adj, source_addr, target_addr):
    "compute shortest path an distance from source to target"
    with open("node_all.json") as f:
        all_nodes = json.load(f)
    source = get_id_from_addr(all_nodes, source_addr)
    target = get_id_from_addr(all_nodes, target_addr)
    # store the predecessor of all nodes, init with itself
    pred = {x: x for x in adj}
    # store the all min distitance of all nodes, init with infinity
    dist = {x: math.inf for x in adj}
    # initialize
    dist[source] = 0
    heap = []
    hq.heappush(heap, [dist[source], source])
    while heap:
        u = hq.heappop(heap)  # u is a list [u_dist, u_id]
        u_dist = u[0]
        u_id = u[1]
        if u_dist == dist[u_id]:
            for v in adj[u_id]:
                v_id = v[0]
                w_uv = v[1]
                if dist[u_id] + w_uv < dist[v_id]:
                    dist[v_id] = dist[u_id] + w_uv
                    hq.heappush(heap, [dist[v_id], v_id])  # decrease key
                    pred[v_id] = u_id
    if dist[target] == math.inf:
        # cannot find path
        print("There is no path between ", source, "and", target)
    else:
        reversed_path = []
        # find predecessor from target
        node = target
        while True:
            reversed_path.append(str(node))
            if(node == pred[node]):
                break
            node = pred[node]
        # reverse
        path = reversed_path[::-1]
        '''
        ============================================================================
        uncomment here to have a view about the output
        ============================================================================
        '''
        # print("The shortest path is " + " ".join(path) + "\n")
        # print(
        #     f"The distance from {source} to {target} is {str(dist[target])}\n")
        # print("distance dictionary: " + str(dist) + "\n")
        # print("predecessor dictionary: " + str(pred))
        return " ".join(path), str(dist[target])

def get_adj_from_all_nodes():
    "get adjcent nodes of all nodes"
    with open("node_all.json") as f:
        all_nodes = json.load(f)
    adj = {}
    for node in all_nodes.keys():
        all_neighbors = all_nodes.get(node).get('neighbours')
        neighbors = []
        for each in all_neighbors:
            neigh = []
            neigh.append(each[0][0])
            neigh.append(each[1])
            neighbors.append(neigh)
        adj[node] = neighbors
    return adj
'''
=======================================================================================================
example output:
{'61321094': [['61321106', 0.04903304678254322], ['61326611', 0.052406387249620566]],
'61321106': [['61321094', 0.04903304678254322]],
'61321110': [['1220427140', 0.058206100712086616],['61321112', 0.13077582925865214]],
'61321112': [['61321110', 0.13077582925865214], ['61326606', 0.13838398793677853]],...
...}
=======================================================================================================
'''

def get_id_from_addr(all_nodes, lati_longi):
    "get the node id given addr"
    for id in all_nodes.keys():
        addr_list = all_nodes.get(id).get('address')
        if addr_list[0] == lati_longi[0] and addr_list[1] == lati_longi[1]:
            return id

def main():
    adj = get_adj_from_all_nodes()
    dijkstra1(adj, '61321094', '257734747')
    path, dist = dijkstra(adj, [42.3688772, -71.0797119], [42.355994, -71.0659108])

if __name__ == "__main__":
    main()
