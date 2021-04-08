class RankPNode:
    def __init__(self,key,id,longitude,latitude):
        self.key = key
        self.id = id
        self.rank = 0
        self.longitude=longitude
        self.latitude=latitude
        self.parent = None
        self.leftChild = None
        self.rightChild = None
    def __repr__(self):
        string=f"distance:{self.key},id:{self.id},longitude:{self.longitude},latitude:{self.latitude}"
        return string
