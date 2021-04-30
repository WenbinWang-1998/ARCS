import json
import xml.dom.minidom
from geopy.distance import geodesic# pip install geopy

dom = xml.dom.minidom.parse('BostonMap.txt')
root = dom.documentElement
nodelist = root.getElementsByTagName('node')
waylist = root.getElementsByTagName('way')
node_dic = {}
for node in nodelist:
    node_id = node.getAttribute('id')
    node_lat = float(node.getAttribute('lat'))
    node_lon = float(node.getAttribute('lon'))
    node_name = 'none'
    node_dic[node_id] = (node_lat, node_lon)

way_node = {}
for way in waylist:
    taglist = way.getElementsByTagName('tag')
    way_id = way.getAttribute('id')
    road_flag = False
    for tag in taglist:
        if tag.getAttribute('k') == 'highway':
            road_flag = True
            #break
    if  road_flag:
        ndlist = way.getElementsByTagName('nd')
        each_way_node = {}
        for nd in ndlist:
            nd_id = nd.getAttribute('ref')
            node_lat = node_dic[nd_id][0]
            node_lon = node_dic[nd_id][1]
            each_way_node[nd_id] = (node_lat, node_lon)
    way_node[way_id] = {
                        'node':each_way_node,
                        }
'''
way_node用于存储所有highway及其经过的node
可以用于查看每个node的neighbour_node
数据结构："8637791": {"61353530": [42.3532505, -71.0788875], "61353260": [42.3538006, -71.0767435]}
表示way_id为'8637791'的路上包含两个点'61353530'和'61353260',并显示他们的lat,lon

with open('way_node.json', 'w') as fout:
    json.dump(way_node, fout, indent = 4)
'''