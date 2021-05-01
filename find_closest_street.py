import json
from geopy import distance

def find_closest_street(src,tar):
    with open("way_node.json") as f:
        way_dict = json.load(f)
    min_src_dist = distance.great_circle((src[0],src[1]),(tar[0],tar[1])).km
    min_tar_dist = min_src_dist
    for streets in way_dict:
        for nodes in way_dict[streets]['node']:
            lat = way_dict[streets]['node'][nodes][0]
            lon = way_dict[streets]['node'][nodes][1]
            src_dist = distance.great_circle((lat,lon),(src[0],src[1])).km
            tar_dist = distance.great_circle((lat,lon),(tar[0],tar[1])).km
            if src_dist < min_src_dist:
                min_src_dist = src_dist
                src_new = [lat,lon]
            if tar_dist < min_tar_dist:
                min_tar_dist = tar_dist
                tar_new = [lat,lon]
    return src_new,tar_new
