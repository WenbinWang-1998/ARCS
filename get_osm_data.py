import matplotlib.pyplot as plt
import json
import xml.dom.minidom
from geopy.distance import geodesic# pip install geopy

dom = xml.dom.minidom.parse('BostonMap.txt')
root = dom.documentElement
nodelist = root.getElementsByTagName('node')
waylist = root.getElementsByTagName('way')
node_dic = {}
node_dic_all = {}
name_dic = {}
node_geo = {}
coordinates = []
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
    if node_name != 'none':
        node_dic_all[node_id] = {
            'address': [node_lat, node_lon],
            'name': node_name,
            'neighbours': [],
            'parentnode': [node_id]
        }
        name_dic[node_name] = [node_id, node_lat, node_lon]
    else:
        node_dic_all[node_id] = {
            'address': [node_lat, node_lon],
            'neighbours': [],
            'parentnode': [node_id]
        }
        
    coordinates.append([node_lat, node_lon])
node_geo = {
        'type':'MultiPoint',
        'coordinates':coordinates
    }


'''
node_name文件只存放所有有name的node
没有name的node不会被保存在这个文件中
可以用于根据name查询node的id,lat,lon
数据结构："Ralph Cook Square": ["61340495", 42.3577809, -71.0702841]
'''
with open('node_name.json', 'w') as fout:
    json.dump(name_dic, fout, indent = 4)
with open('node_geo.json', 'w') as fout:
    json.dump(node_geo, fout, indent = 4)

# get way nodes
#node_dic2 = {}
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
            #break
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
            each_way_node[nd_id] = (node_lat, node_lon)
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
#print (len(node_dic2))
#with open('way_node_all.json', 'w') as fout:
#    json.dump(node_dic2, fout)
'''
way_node用于存储所有highway及其经过的node
可以用于查看每个node的neighbour_node
数据结构："8637791": {"61353530": [42.3532505, -71.0788875], "61353260": [42.3538006, -71.0767435]}
表示way_id为'8637791'的路上包含两个点'61353530'和'61353260',并显示他们的lat,lon
'''
with open('way_node.json', 'w') as fout:
    json.dump(way_node, fout, indent = 4)

'''
node_all文件里存放所有node的id，经纬度，名称和所有的相邻点之间的距离。
如果该node无name，则无此项
可以用于根据id查询所有node的lat,lon,name
还可用于查找每个点的相邻点，包括id,经纬度和距离
数据结构："61340495": {
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