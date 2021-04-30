import json
import math
import heapq as hq  # using heapq in python
import time

def Astar(adj, source_addr, target_addr):
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

    target_coordinate = get_addr_from_id(
        all_nodes, target)  # target node's coordinate

    dist[source] = 0
    heap = []
    hq.heappush(heap, [dist[source], source])  # first is distance, second is id
    while heap:
        u = hq.heappop(heap)  # u is a list [u_dist, u_id] 
        u_dist = u[0]
        u_id = u[1]
        if u_id == target:
            break
        if u_dist == dist[u_id]:
            for v in adj[u_id]:  # finding neighbors
                # if u_id == target:
                #     break
                v_id = v[0]
                w_uv = v[1]  # the distance between node and neighbor
                current = get_addr_from_id(all_nodes, v_id)
                euclidean = math.sqrt(
                    (target_coordinate[0] - current[0]) ** 2 + (target_coordinate[1] - current[1]) ** 2)
                w_uv = w_uv + euclidean
                if dist[u_id] + w_uv < dist[v_id]:
                    dist[v_id] = dist[u_id] + w_uv
                    hq.heappush(heap, [dist[v_id], v_id])  # decrease key
                    pred[v_id] = u_id  
    if dist[target] == math.inf:
        # cannot find path
        print("There is no path between ", source, "and", target)
        return
    else:
        reversed_path = []
        # find predecessor from target
        node = target
        while True:
            addr = get_addr_from_id_reversed(all_nodes, node)
            reversed_path.append(addr)
            if (node == pred[node]):
                break
            node = pred[node]
        # reverse
        path = reversed_path[::-1]
        node_geo = {"type": "FeatureCollection","properties": { "scalerank": 5}, "features": [{ "type": "Feature", "geometry":
                    { "type": "LineString", "coordinates": path}}]}
        with open('a_star_geo_out.json', 'w') as fout:
            json.dump(node_geo, fout, indent = 4)
    return node_geo, str(dist[target])





# input: start and target position [lati, longi]
# output: heuristic estimate of distance h()


def heuristic_estimate_of_distance(start_addr, target_addr):
    return math.sqrt((start_addr[0] - target_addr[0]) ** 2 + (start_addr[1] - target_addr[1]) ** 2)


def get_addr_from_id_reversed(all_nodes, id):
    "get the addr given node id and reverse the lati and longi"
    addr_list = all_nodes.get(id).get('address')
    # lati and longi get reversed
    new_addr = []
    new_addr.append(addr_list[1])
    new_addr.append(addr_list[0])
    return new_addr


def get_addr_from_id(all_nodes, id):
    "get the addr given node id and reverse the lati and longi"
    return all_nodes.get(id).get('address')


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



def get_id_from_addr(all_nodes, lati_longi):
    "get the node id given addr"
    for id in all_nodes.keys():
        addr_list = all_nodes.get(id).get('address')
        if addr_list[0] == lati_longi[0] and addr_list[1] == lati_longi[1]:
            return id


def main():
    adj = get_adj_from_all_nodes()
    start_t = time.time()
    path, dist = Astar(adj, [42.3657714, -71.0510548], [42.3586117, -71.0503471])
    print(f'Time spent: {time.time() - start_t}')  # Time spend
    print(path)



    start_t = time.time()
    path, dist = Astar(adj, [42.3688772, -71.0797119], [42.3638423, -71.0627748])
    print(f'Time spent: {time.time() - start_t}')  # Time spend
    print(path)

if __name__ == "__main__":
    main()
