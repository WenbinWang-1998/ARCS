import json
import math
import heapq as hq  # using heapq in python
import time
import queue

def Bellmanford(adj, source_addr, target_addr):
    with open("node_all.json") as f:
        all_nodes = json.load(f)
    source = get_id_from_addr(all_nodes, source_addr)
    target = get_id_from_addr(all_nodes, target_addr)
    # store the predecessor of all nodes, init with itself
    pred = {x: x for x in adj}
    # store the all min distitance of all nodes, init with infinity
    dist = {x: math.inf for x in adj}
    #inqueue used in bellmanford
    inqueue={x: 0 for x in adj}
    q = queue.LifoQueue()
    dist[source] = 0
    inqueue[source]=1
    q.put([dist[source], source]) #q的顺序是先 distance,后id. 和adj正好相反
    while not q.empty():
        u = q.get()  # u is a list [u_dist, u_id] #pop时根据distance大小选最小
        u_dist = u[0]
        u_id = u[1]
        inqueue[u_id]=0
        for v in adj[u_id]:  # 找到neighbor
            v_id = v[0]
            w_uv = v[1]  # 到neighbor之间的距离
            if dist[u_id] + w_uv < dist[v_id]:
                dist[v_id] = dist[u_id] + w_uv
                pred[v_id] = u_id  # predecessor存前驱节点
                if inqueue[v_id]==0:
                    inqueue[v_id]=1
                    q.put([dist[v_id], v_id])
    if dist[target] == math.inf:
        # cannot find path
        print("There is no path between ", source, "and", target)
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
        with open('bellmanford_geo_out.json', 'w') as fout:
            json.dump(node_geo, fout, indent = 4)
    return node_geo, str(dist[target])

# input: start and target position [lati, longi]
# output: heuristic estimate of distance h()

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
    path, dist = Bellmanford(adj, [42.3657714, -71.0510548], [42.3586117, -71.0503471])
    print(f'Time spent: {time.time() - start_t}')
    print(path)


if __name__ == "__main__":
    main()