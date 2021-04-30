# ref: https://blog.csdn.net/ailinyingai/article/details/100523926

class Node:
    def __init__(self, value):
        self.parent = self.children = None
        self.value = value
        self.degree = 0
        self.left = self.right = self
        self.marked = False
        self.vertex = None

    def find_min(self):
        min_node = self
        begin_node = self
        current_node = self.right
        while current_node != begin_node:
            if current_node.value < min_node.value:
                min_node = current_node
            current_node = current_node.right
        return min_node

    def remove_parent(self):
        self.degree = self.parent.degree - 1
        begin_node = self
        self.parent = None
        current_node = self.right
        while current_node != begin_node:
            current_node.parent = None
            current_node = current_node.right
    
class FibonacciHeap:
    def __init__(self):
        self.min = None
        self.count = 0

    def make_heap(self):
        self.min = None
        self.count = 0
        return self

    def insert(self, new_node):
        self.count += 1
        new_node.parent = None
        new_node.left = new_node.right = new_node
        if self.count == 1:
            self.min = new_node
        else:
            temp = self.min.left
            temp.right = new_node
            new_node.left = temp
            new_node.right = self.min
            self.min.left = new_node
        if new_node.value < self.min.value:
            self.min = new_node

    def minimum(self):
        return self.min

    def union(self, h):
        if h.count == 0:
            return
        if self.count == 0:
            self.count = h.count
            self.min = h.min
            return
        left = self.min
        right = h.min
        left.right.left = right.left
        right.left.right = left.right
        left.right = right
        right.left = left
        self.count += h.count
        if h.min.value < self.min.value:
            self.min = h.min

    def link_node(self, link_a, link_b):
        link_a.left.right = link_a.right  # remove link_a, connect its left and right
        link_a.right.left = link_a.left
        link_a.left = link_b  # insert as link_b -> link_a
        link_a.right = link_b.right
        link_b.right.left = link_a
        link_b.right = link_a
        if link_b.value < link_a.value:
            temp = link_a  # link_a is always the parent
            link_a = link_b
            link_b = temp
            link_a.right = link_b.right
            link_b.right.left = link_a
        else:
            link_a.left = link_b.left
            link_b.left.right = link_a
        link_b.marked = False  # remove link_b
        link_b.parent = link_a
        link_b.left = link_b.right = link_b
        if link_a.children is None:
            link_a.children = link_b
        link_b.left = link_a.children.left  # connect link_b with link_a.children
        link_b.right = link_a.children
        link_a.children.left.right = link_b
        link_a.children.left = link_b
        link_a.degree += 1
        return link_a

    def consolidate(self):
        node_array = [None] * self.count
        node_array[self.min.degree] = self.min
        begin_node = self.min
        current_node = self.min.right
        while current_node != begin_node:
            while node_array[current_node.degree] is not None:
                link_a = node_array[current_node.degree]
                link_b = current_node
                if link_a == self.min and link_a.right != link_b:
                    begin_node = link_a.right
                node_array[current_node.degree] = None
                current_node = self.link_node(link_a, link_b)
            node_array[current_node.degree] = current_node
            current_node = current_node.right
    
    # remove the minimum node and return this node
    def extract_min(self):
        min_node = self.min
        if min_node is None:  # no node
            return min_node
        self.count -= 1  # remove min, thus count decreases by 1
        if self.min.left == self.min:  # one node
            if min_node.degree == 0:  # no children
                self.min = None
                self.count = 0  # no node left
                return min_node
            self.min = min_node.children.find_min()  # new minimum is from children
            min_node.children.remove_parent()  # all children become root, keep cycle
            return min_node
        left = min_node.left  # more than one node
        right = min_node.right
        if min_node.children is None:  # no children
            left.right = right  # simply connect min.left and min.right
            right.left = left
            self.min = right  # temporarily set right as min
        else:
            left.right = right
            right.left = left
            begin_node = min_node.children
            current_node = min_node.children.right
            min_node.children.remove_parent()
            self.min = right  # temporarily set right as min, insert nodes between left and right
            self.insert(begin_node)
            self.count -= 1
            while current_node is not None and current_node != begin_node:
                next_node = current_node.right
                self.insert(current_node)
                self.count -= 1
                current_node = next_node
        self.min = self.min.find_min()  # find min for new heap
        # merge
        self.consolidate()  # merge nodes with same degree
        return min_node  # still return the origin min node

    def move_child(self, node):
        node_parent = node.parent
        if node.right == node:  # parent only has one child
            node_parent.children = None
        else:
            if node_parent.children == node:  # node is children
                node_parent.children = node.right
            node.left.right = node.right
            node.right.left = node.left
        node.parent = None
        node.marked = False
        node_parent.degree -= 1
        self.insert(node)
        self.count -= 1

    def decrease_key(self, node, value):
        # node = self.find_node(key)
        if node.value < value:  # increase key, then return
            return
        node_parent = node.parent
        node.value = value
        if node_parent is not None:  # node is not root
            if node.value > node_parent.value:  # obey minimum heap rule
                return
            temp = node  # recursively remove child
            while temp is not None and temp.parent is not None:
                self.move_child(temp)
                temp = temp.parent
                if temp is not None and temp.marked is False:  # parent hasn't lose child
                    temp.marked = True
                    break
        if self.min.value > node.value:
            self.min = node
        # TODO: cause dead endless loop 
        # self.consolidate()
    
    # TODO: cause indexOutOfBound, delete is not a required operation
    def delete(self, key):
        self.decrease_key(key, self.min.value - 1)
        self.extract_min()


# print the whole Fibonacci Heap
def print_heap(h):
    if h.min is None:
        print("Heap is empty")
        return
    print_tree(h.min)
    print(" ")
    temp = h.min.right
    while temp != h.min:
        print_tree(temp)
        print(" ")
        temp = temp.right


# print the tree for one heap
def print_tree(root):
    if root.children is None:
        print("{}: None".format(root.value))
    else:
        c = root.children
        print("{}: {}".format(root.value, c.value), end=" ")
        c = c.right
        while c != root.children:
            print(c.value, end=" ")
            c = c.right
        print(" ")
        print_tree(root.children)
        c = root.children.right
        while c != root.children:
            print_tree(c)
            c = c.right

