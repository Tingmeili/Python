#coding: UTF-8

import math
import os
import datetime
import re
import json

#used to covert gps to rel in each other
ANG_HUD = 0.0174532925199433
RADIUS = 6378137
HUD_ANG = 57.29577951308233
FEARTH = 0.0033528131778969
ESQUARE = FEARTH * (2 - FEARTH)

def get_gps_distance(gps_coord1, gps_coord2):
    dist = 0.0
    if gps_coord1 and gps_coord2:
        lon_1st, lat_1st, lon_2nd, lat_2nd =  map(math.radians, [float(gps_coord1[0]), float(gps_coord1[1]), float(gps_coord2[0]), float(gps_coord2[1])])
        delta_lon = lon_1st - lon_2nd
        delta_lat = lat_1st - lat_2nd
        delta_change = math.sin(delta_lat / 2) ** 2 + math.cos(lat_1st) * math.cos(lat_2nd) * math.sin(delta_lon / 2) ** 2
        delta_angle = 2 * math.asin(math.sqrt(delta_change))
        dist = delta_angle * RADIUS
    return dist

def gps_covert_to_rel(gps_coords):
    stand_coord, rel_coords = "", []
    if len(gps_coords) >= 1:
        stand_coord = gps_coords[0]
        for gps_coord in gps_coords:
            rel_lon, rel_lat = get_rel_coord(stand_coord, gps_coord)
            rel_coords.append((rel_lon, rel_lat))
    return rel_coords

def gps_covert_to_rel_v2(gps_coords):
    stand_coord, rel_coords = "", []
    if len(gps_coords) >= 1:
        stand_coord = gps_coords[0]
        for gps_coord in gps_coords:
            rel_lon, rel_lat = get_rel_coord(stand_coord, gps_coord)
            rel_coords.append((rel_lon, rel_lat))
    return stand_coord, rel_coords
    # return rel_coords

def get_rel_coord(stand, source_gps):
    dlon = (float(source_gps[0]) - float(stand[0])) * ANG_HUD
    if dlon > math.pi:
        dlon = dlon - 2 * math.pi
    elif dlon < -math.pi:
        dlon = 2 * math.pi + dlon;
    lat = (float(stand[1])) * ANG_HUD
    sin_lat, cos_lat = math.sin(lat), math.cos(lat)
    RM = RADIUS * (1 - ESQUARE) / math.pow(1 - ESQUARE * sin_lat * sin_lat, 1.5)
    RN = RADIUS * cos_lat / math.sqrt(1 - ESQUARE * sin_lat * sin_lat)
    lon_rel = dlon * RN
    lat_rel = (float(source_gps[1]) - float(stand[1])) * ANG_HUD * RM
    return lon_rel, lat_rel

def linear_interpolate(rel_coords):
    step, dense_gps_list = 1.0, []
    threshold = step * 2
    for i, coord in enumerate(rel_coords[1:]):
        first, second = rel_coords[i], coord
        diff_x, diff_y = second[0] - first[0], second[1] - first[1]
        dist = math.sqrt(diff_x ** 2 + diff_y ** 2)
        dense_gps_list.append(first)   
        if dist < threshold:
            continue       
        num = int(dist / step)
        delta_x, delta_y = diff_x / num, diff_y / num  
        for j in range(1, num):
            dense_gps_list.append((first[0] + j * delta_x, first[1] + j * delta_y))          
    dense_gps_list.append(rel_coords[-1])
    return dense_gps_list

def rel_covert_to_gps(standard_gps, rel_coords):
    gps_coords = []
    if rel_coords:
        for rel_coord in rel_coords:
            lon_gps, lat_gps = get_gps_coord(standard_gps, rel_coord)
            gps_coords.append((lon_gps, lat_gps))
    return gps_coords 

def get_gps_coord(standard_gps, rel_coord):
    lat = float(standard_gps[1]) * ANG_HUD
    sin_lat, cos_lat = math.sin(lat), math.cos(lat)
    RM = RADIUS * (1 - ESQUARE) / math.pow(1 - ESQUARE * sin_lat * sin_lat, 1.5)
    RN = RADIUS * cos_lat / math.sqrt(1 - ESQUARE * sin_lat * sin_lat)
    lon_gps = float(standard_gps[0]) + float(rel_coord[0]) / RN * HUD_ANG
    lat_gps = float(standard_gps[1]) + float(rel_coord[1]) / RM * HUD_ANG
    if lon_gps >= 180.0:
        lon_gps -= 360.0
    elif lon_gps <= -180.0:
        lon_gps += 360.0
    return lon_gps, lat_gps

def save_json(json_file, map_divs, map_nodes, iden = ""):
    json_name = os.path.basename(json_file).replace(".json", "_" + iden + ".json")
    json_name = os.path.join(os.path.dirname(json_file), json_name)
    json_data = {}
    json_data["map_div_"] = map_divs
    json_data["map_node_"] = map_nodes
    try:
        with open(json_name, 'w') as writer:
            writer.write(json.dumps(json_data, indent = 4))
        writer.close()
        result = 0
    except e:
        result = 1
    return result

def save_json_to_kml(json_file, map_divs, map_nodes, iden = ""):
    kml_file = os.path.basename(json_file).replace(".json", "_" + iden + ".kml")
    kml_file =  os.path.join(os.path.dirname(json_file), kml_file)
    kml_content = '<Folder xmlns:atom="http://www.w3.org/2005/Atom" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns="http://www.opengis.net/kml/2.2">\n'
    if map_nodes:
        kml_content += get_map_nodes_infos(map_divs, map_nodes)
    if map_divs:
        kml_content += get_map_divs_infos(map_divs)
    kml_content += "</Folder>"
    try:
        with open(kml_file, 'w') as writer:
            writer.write(kml_content)
        writer.close()
        result = 0
    except e:
        result = 1
    return result

def get_map_divs_infos(map_divs):
    div_infos = ""
    for map_div in map_divs:
        div_id = str(map_div["id_div_"])
        name = "    <name>" + div_id + "</name>\n"
        schema_ = map_div["schema_"]
        description = "    <description>"
        description += '{"list_line_type_":' + str(schema_["list_line_type_"]) + ","
        description += '"list_line_group_str_":' + str(schema_["list_line_group_str_"]) + ","
        description += '"type_schema_":"' + str(schema_["type_schema_"]) + '"}'
        description += "</description>\n"
        line_string = "    <LineString>\n      <extrude>1</extrude>\n      <gx:altitudeMode>clampedToSeaFloor</gx:altitudeMode>\n"
        line_string += "      <coordinates>"
        lon_list, lat_list = map_div["list_lon_"], map_div["list_lat_"]
        for i, lon_ in enumerate(lon_list):
            line_string += str(lon_) + "," + str(lat_list[i]) + ",0 "
        line_string += "</coordinates>\n    </LineString>\n"
        div_infos += "  <Placemark>\n" + name + description + line_string + "  </Placemark>\n"
    return div_infos

def get_map_nodes_infos(map_divs, map_nodes):
    node_infos = ""
    for map_node in map_nodes:
        node_id = str(map_node["id_node_"])
        node_gps = [str(map_node["lon_"]), str(map_node["lat_"])]
        if re.match(r'^9\d{4}$', node_id):
            node_value = "newNode"
            node_type = "0"
        else:
            divs = map_node["list_id_div_"]
            node_type = str(map_node["type_node_"])
            if not divs:
                continue
            if 1 == len(divs):
                node_value = get_node_info(node_id, divs[0], map_divs)
            else:
                node_value = "Junction"
        if not node_value:
            continue
        name = "    <name> " + node_value + " " + node_type + " " + node_id + "</name>\n"
        point = "    <Point>\n      <coordinates>" + ",".join(node_gps) + "</coordinates>\n    </Point>\n"
        node_infos += "  <Placemark>\n" + name + point + "  </Placemark>\n"
    return node_infos

def get_node_info(node_id, div_id, map_divs):
    div, value = "", ""
    if map_divs:
        for map_div in map_divs:
            map_div_id = map_div["id_div_"]
            if str(div_id) == str(map_div_id):
                div = map_div
                break
    if div:
        start_id, end_id = div["id_node_s_"], div["id_node_e_"]
        if str(start_id) == str(node_id):
            value = "start"
        elif str(end_id) == str(node_id):
            value = "end"
    return value