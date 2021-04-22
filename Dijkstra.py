from myFiboHeap import *

def dijkstra(id_o, id_d):
    # Init
    res = math.inf
    heap = FibonacciHeap()
    # all nodes init to inf
    # build all nodes
    for each in dict.keys():
        fibo_node = Node(each, math.inf)
        heap.insert(fibo_node)
    # decrease id_o to 0
    # print_heap(heap)
    heap.decrease_key(id_o, 0)
    # print_heap(heap)
    while heap.count != 0:
        # print_heap(heap)
        min_node = heap.extract_min()
        heap.popped[min_node.id] = 1
        # print(min_node.id)
        adj_nodes = []  # contains id
        for each in dict[min_node.id].keys():
            if not each in heap.popped:
                adj_nodes.append(each)
        for each in adj_nodes:
            each_fibo_node = heap.find_node(each)
            if each_fibo_node.value > min_node.value + dict[min_node.id][each]:
                new_value = min_node.value + dict[min_node.id][each]
                heap.decrease_key(each, new_value)
                dict_pred[each_fibo_node.id] = min_node.id
                res = new_value if each == id_d else res
                
    
    return res
def print_smallest_path(dict_pred, id_s, id_o):
    pred = id_o
    res = 'the path is '
    while pred is not id_s:
        res += pred
        res += ' <- '
        pred = dict_pred[pred]
    res += pred
    print(res)

class node_in_map:
    def __init__(self, id, adj):
        self.id = id
        self.adj = adj
        self.pred = None


if __name__ == '__main__':
    n1 = node_in_map('0001', {'0002': 1, '0005': 1, '0006': 1})
    n2 = node_in_map('0002', {'0003': 1, '0005': 1, '0001': 1})
    n3 = node_in_map('0003', {'0002': 1, '0004': 1})
    n4 = node_in_map('0004', {'0003': 1, '0005': 10, '0006': 1})
    n5 = node_in_map('0005', {'0004': 10, '0002': 1, '0001': 1})
    n6 = node_in_map('0006', {'0004': 1, '0001': 1})
    dict = {}
    dict[n1.id] = n1.adj
    dict[n2.id] = n2.adj
    dict[n3.id] = n3.adj
    dict[n4.id] = n4.adj
    dict[n5.id] = n5.adj
    dict[n6.id] = n6.adj
    # dict for pred
    dict_pred = {}

    print(f"min cost is {dijkstra('0004', '0001')}")

    # print(dict_pred)
    print_smallest_path(dict_pred, '0004', '0001')





        

