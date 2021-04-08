class RankPNode:
    def __init__(self,key,id,longitude,latitude):
        self.key = key  #distance
        self.id = id    #对应id
        self.rank = 0   #rank-pairing heap特有rank
        self.longitude=longitude
        self.latitude=latitude
        self.parent = None  #以树的结构存储，最后组成森林
        self.leftChild = None
        self.rightChild = None
    def __repr__(self):
        string=f"distance:{self.key},id:{self.id},longitude:{self.longitude},latitude:{self.latitude}"  
        return string
