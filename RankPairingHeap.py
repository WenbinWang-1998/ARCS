from RankPNode import RankPNode
import math,random
class RankPairingHeap:
    def __init__(self,size): #size should be all the nodes in map
        self.root=[None for x in range(size)] #声明初始全空数组,该数组只放RankPNode的root

    def insert(self,node:RankPNode): #We do insert with merge, not lazy insert (如果用lazy，需要有指针时刻跟随min)
        if self.root[node.rank]==None:  #If the corresponding rank is None, just put the node in without merge
            self.root[node.rank]=node
        else:
            node1=self.root[node.rank]
            self.merge(node1,node)

    def merge(self,node1:RankPNode,node2:RankPNode):
        if node2.key<node1.key:
            save=node2
            node2=node1
            node1=save
        node2.parent=node1
        temp=node1.leftChild
        node1.leftChild = node2
        node2.rightChild=temp
        if temp!=None:
            temp.parent=node2
        self.root[node1.rank]=None
        node1.rank=node2.rank+1
        if self.root[node1.rank]==None:
            self.root[node1.rank]=node1
            return
        else:
            self.merge(node1,self.root[node1.rank])

    def deletemin(self):
        minimum=float('inf')  #the maximum number in float type
        minNode:RankPNode=None
        for i in self.root:
            if i==None:
                continue
            else:
                if i.key<=minimum:####从小于改成小于等于
                    minimum=i.key
                    minNode=i
        self.root[minNode.rank]=None  # we should update the root array,because we already delete the minimum
        if minNode.leftChild==None and minNode.rightChild==None:
            return minNode
        new:RankPNode=minNode.leftChild
        right:RankPNode=new.rightChild
        while(right!=None):
            right.parent=None
            new.parent=None
            new.rightChild=None
            if(new.leftChild!=None):
                new.rank=new.leftChild.rank+1
                self.insert(new)
            else:
                new.rank=0
                self.insert(new)
            new=right
            right=new.rightChild
        if new.parent!=None:
            new.parent.rightChild=None
            new.parent=None
        if new.leftChild==None:
            new.rank=0
            self.insert(new)
        else:
           new.rank=new.leftChild.rank+1;
           self.insert(new)
        return minNode
            
#     def deletemin(self):
#         minimum=float('inf')  #the maximum number in float type
#         minNode:RankPNode=None
#         #print(self.root)
#         for i in self.root:
#             if i==None:
#                 continue
#             else:
#                 if i.key<minimum:
#                     minimum=i.key
#                     minNode=i
#         self.root[minNode.rank]=None  # we should update the root array,because we already delete the minimum
#         if minNode.leftChild!=None:
#             parent:RankPNode=minNode.leftChild
#             rparent:RankPNode=parent.rightChild
#             while parent.rightChild!=None:   #start recursion
#                 parent.parent = None
#                 rparent.parent=None
#                 parent.rightChild=None
#                 if parent.leftChild!=None:
#                     parent.rank=parent.leftChild.rank+1
#                     self.insert(parent)
#                 else:
#                     parent.rank=0
#                     self.insert(parent)
#                 self.insert(parent)
#                 parent=rparent
#                 rparent=rparent.rightChild
#         else:
#             return minNode
#         #dealing with the last node, because the last while loop will left a node
#         if parent!=None:
#             if parent.parent!=None:
#                 parent.parent.rightChild=None  #update the information of last node and second to last(last's parent)
#                 parent.parent=None
#             if parent.leftChild==None:
#                 parent.rank=0
#                 self.insert(parent)
#             else:
#                 parent.rank=parent.leftChild.rank+1
#                 self.insert(parent)
#         return minNode

    def adjustRank(self,node:RankPNode): # Bottom up strategy to update the rank
        lrank=-1
        rrank=-1
        while node.parent!=None:    #Notice:after the while loop, we should also update the node in root
            if node.leftChild==None and node.rightChild==None:
                node.rank=0
                node=node.parent
                continue
            else:
                if node.leftChild!=None:
                    lrank=node.leftChild.rank
                if node.rightChild!=None:
                    rrank=node.rightChild.rank
                if abs(lrank-rrank)>1:
                    node.rank=max(lrank,rrank)
                else:
                    node.rank = max(lrank, rrank)+1
                node=node.parent
            lrank = -1
            rrank = -1
        #now the node should in the root array
        if node.parent==None:
            if node.leftChild==None:
                node.rank=0
            else:
                node.rank=node.leftChild.rank+1


    def decreaseKey(self,newKey,node:RankPNode): #newKey为新的distance，node为所选节点
        node.key=newKey
        if node.parent==None: # if the node is in the root array
            return
        parentx:RankPNode=node.parent
        if parentx.leftChild==node:
            if node.leftChild==None and node.rightChild==None:
                node.parent=None   #grab the node to the root array
                parentx.leftChild=None
                self.adjustRank(parentx)
                node.rank=0
                self.insert(node)
                return
            if node.leftChild!=None:
                node.parent=None
                parentx.leftChild = node.rightChild #change leftchild of parentx, rightchild may be None
                if node.rightChild!=None: #只要rightchild不为none，就把它接到node的parent上
                    node.rightChild.parent=parentx
                node.rightChild=None
                self.adjustRank(node) #必须从node的开始更新（bottom up），node将成为新的root
                self.adjustRank(parentx)#同时要更新的还有parentx
                #rank已经调整无需重新调整
                self.insert(node)
                return
        else:
            if node.leftChild==None and node.rightChild==None:
                node.parent=None   #grab the node to the root array
                parentx.rightChild=None
                self.adjustRank(parentx)
                node.rank=0
                self.insert(node)
                return
            if node.leftChild!=None:
                node.parent=None
                parentx.rightChild = node.rightChild #change leftchild of parentx
                if node.rightChild!=None: #只要rightchild不为none，就把它接到node的parent上
                    node.rightChild.parent=parentx
                node.rightChild=None
                self.adjustRank(node)
                self.adjustRank(parentx)#同时要更新的还有parentx
                #rank已经调整无需重新调整
                self.insert(node)
                return


#TEST
if __name__=='__main__':
    def Order(heap): #测试代码
        for i in heap.root:
            if i!=None:
                preOrder(i)
                print()
            else:
                print(i)
    def preOrder(node:RankPNode): #先序遍历
        if node!=None:
            print(f"key:{node.key} rank:{node.rank}",end=" ")
        if node.leftChild!=None:
            preOrder(node.leftChild)
        if node.rightChild!=None:
            preOrder(node.rightChild)

    heap=RankPairingHeap(20);
    list=[]
    for i in range(0,16):
        x=random.random()*100
        node=RankPNode(i+1,i+1,0,0)
        heap.insert(node)
        list.append(node)


    heap.decreaseKey(-1,list[12])
    heap.decreaseKey(-2,list[10])

    Order(heap)
    print("**************")
    for i in heap.root:
        if i!=None:
            print(i.key,i)
        else:
            print(i)


    print(heap.root)
    print(heap.deletemin().key)
