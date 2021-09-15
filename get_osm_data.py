import json
import xml.dom.minidom
from geopy.distance import geodesic# pip install geopy

dom = xml.dom.minidom.parse('BostonMap.txt')
root = dom.documentElement
nodelist = root.getElementsByTagName('node')
waylist = root.getElementsByTagName('way')
node_dic = {}
node_dic_all = {}
# all nodes
for node in nodelist:
    node_id = node.getAttribute('id')
    node_lat = float(node.getAttribute('lat'))
    node_lon = float(node.getAttribute('lon'))
    node_name = 'none'
    # get node name
    try:
        node_taglist = node.getElementsByTagName('tag')
        for tag in node_taglist:
            if tag.getAttribute('k') == 'name':
                node_name = tag.getAttribute('v')
    except:
        pass
    node_dic[node_id] = (node_lat, node_lon)
    node_dic_all[node_id] = {
        'address': [node_lat, node_lon],
        'neighbours': [],
        'parentnode': [node_id]
    }
# get way nodes
way_node = {}
for way in waylist:
    taglist = way.getElementsByTagName('tag')
    way_id = way.getAttribute('id')
    road_flag = False
    one_way = False
    for tag in taglist:
        if tag.getAttribute('k') == 'oneway':# 考虑单向车道
            if tag.getAttribute('v') == 'yes':
                one_way = True
        elif tag.getAttribute('k') == 'highway':
            road_flag = True
    if  road_flag:
        ndlist = way.getElementsByTagName('nd')
        each_way_node = {}
        j = 0
        a = {}
        for nd in ndlist:
            nd_id = nd.getAttribute('ref')
            node_lat = node_dic[nd_id][0]
            node_lon = node_dic[nd_id][1]
            #node_dic2[nd_id] = (node_lat, node_lon)
            each_way_node[nd_id] = (node_lon,node_lat)
            a[j] = [nd_id,node_lat,node_lon]
            j = j + 1
        for k in range(j):
            if k > 0:
                distance = geodesic((a[k][1],a[k][2]), (a[k-1][1],a[k-1][2])).km# 计算相邻点之间的距离
                if one_way:
                    node_dic_all[a[k-1][0]]['neighbours'].append([a[k],distance])
                else:
                    node_dic_all[a[k-1][0]]['neighbours'].append([a[k],distance])
                    node_dic_all[a[k][0]]['neighbours'].append([a[k-1],distance])
    way_node[way_id] = {
                        'node':each_way_node,
                        'one_Way':one_way
                        }

'''
node_all.json stores all the nodes' id, lon, lat, name(if has), and distance to all the neighbours.
It is the most important file because all the algorithms use node_all to search all the nodes' lat, lon, name and neighbours.
All the neighbours' nod_id, lat and lon are also included.
Situation of 'one_way' street is considered, streets with <tag k="oneway" v="yes"/> are irreversible。
Example of data structure:
    "61340495": {
        "address": [
            42.3577809,
            -71.0702841
        ],
        "name": "Ralph Cook Square",
        "neighbours": [
            [
                [
                    "1038908673",
                    42.3576959,
                    -71.0706028
                ],
                0.027902191198272253
            ],
            [
                [
                    "61510043",
                    42.3577985,
                    -71.0702046
                ],
                0.006835163310998479
            ],
            [
                [
                    "61340491",
                    42.3584617,
                    -71.0706523
                ],
                0.08148039635396587
            ],
            [
                [
                    "61469722",
                    42.357773,
                    -71.070279
                ],
                0.0009729353659836035
            ]
        ],
        "parentnode": []
    }
'''
with open('node_all.json', 'w') as fout:
    json.dump(node_dic_all, fout, indent = 4)

'''
way_node.json stores all the streets(highways) and the nodes on them.
It is used to check whether the start and target nodes are on the street, if not, calculate and find the nearest street.
It also shows whether the streets are one_way.
Example of data structure:
    "48982057": {
        "node": {
            "527724554": [
                -71.055624,
                42.3532558
            ],
            "1545170855": [
                -71.0558854,
                42.3531353
            ],
            "1545170773": [
                -71.0561433,
                42.3530331
            ],
            "1545170829": [
                -71.0565011,
                42.3529136
            ],
            "527724553": [
                -71.0571703,
                42.3527197
            ]
        },
        "one_Way": true
        }
'''
with open('way_node.json', 'w') as fout:
    json.dump(way_node, fout, indent = 4)