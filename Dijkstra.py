from RankPNode import RankPNode
from RankPairingHeap import RankPairingHeap
import math
import json
with open("node_all.json") as f:
    result = json.load(f)

#wwb写的rankparingheap，dist是第一个输入参数，id是第二个
def Dijkstra(src,tar): #src和tar必须是list类型的
    #需传入起始点，终点，以及整个图结构
    length=len(result)
    heap=RankPairingHeap (length)
    ###New=find_closest_street(way_dict,src,tar);#接收四个返回值
    ###start=New[0]#新起点
    ###end=New[2]#新终点
    rootnode=RankPNode(0,get_keys(result,src)) #起始点的id的RankPNode
    targetnode=RankPNode(float('inf'),get_keys(result,tar))#终点的id的RankPNode
    #heap.insert((rootnode))
    dist={}#key为id,value为RankPNode类型的node
    for id in result.keys():
        if id==rootnode.id:
            heap.insert((rootnode))

        else:
            node=RankPNode(float('inf'),id) #初始距离声明为无穷大
            dist[id]=node
            heap.insert(node)
    while(True):#始终循环直到找到最终点的id
        node:RankPNode=heap.deletemin() #该Node为RankPNode类型
        if(node==None):
            return
        rnode=result.get(node.id)#获取json中对应的node

        if node.id==targetnode: #一旦弹出target，就结束
            return
        euclidean=math.sqrt((tar[0]-rnode.get('address')[0])**2+(tar[1]-rnode.get('address')[1])**2)#测定当前节点到终点的欧式距离
        neighbors=result.get(node.id).get('neighbours')#从node结构中提取id，利用此id得到图中node的neighbor list。
        nLen=len(neighbors) #共有几个neighbor
        for neighbor in neighbors:
            id=neighbor[0][0]#获取点的id并在dict中查找对应RankPNode
            next=dist.get(id)#得到RankPNode
            if next==None:
                continue
            nnode=result.get(next.id)#获取json中对应的node   rnode和nnode对应
            distance=math.sqrt((nnode.get('address')[0]-rnode.get('address')[0])**2+(nnode.get('address')[1]-rnode.get('address')[1])**2)+node.key
            if next.key>distance:
                result.get(next.id).get('parentnode')[0]=next.id #因为parentnode中预存储了自己，该list中只有一个值，所以是[0]
                heap.decreaseKey(distance,next)#对对应node进行decreasekey



# 该方法用于获取输入latitude与longitude对应的id,返回为str
def get_keys(dic, latlong):
    for key in dic.keys():
        lis = dic.get(key).get('address')
        if lis[0] == latlong[0] and lis[1] == latlong[1]:
            return key


Dijkstra([42.3688772,-71.0797119],[42.3688772,-71.0797119])
print("结束")


