# from math import radians, cos, sin, asin, sqrt, pi
import math
import kdtree
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from Utils import utils
import copy

MIN_DISTANCE = 2   #unit M
SQUARE = MIN_DISTANCE ** 2
MAP_DIV_INDEX = 10000 # used to index new added div
MAP_NODE_INDEX = 90000 #used to index new added node
SEARCH_NODES = 4  #nums for kd tree search

class addCoords(object):
    def __init__(self, source_map_div, source_map_node, add_coords_list):
        self.source_map_div = source_map_div
        self.source_map_node = source_map_node
        self.add_coords_list = add_coords_list

    def add_coords(self):
        if self.add_coords_list:
            for add_coord in self.add_coords_list:
                add_coord.reverse()
            #length equals to 1, means to split the exists trajectory
            if 1 == len(self.add_coords_list):
                print "click coord is :: " + str(self.add_coords_list[0])
                all_map_coords = self.get_all_map_coords()
                # standard_gps, all_coords = utils.gps_covert_to_rel(all_map_coords)
                standard_gps, rel_coords = utils.gps_covert_to_rel_v2(all_map_coords)
                self.get_target_div(standard_gps, rel_coords)
        # print "***"
        # print self.source_map_div
        # print self.source_map_node
        return self.source_map_div, self.source_map_node

    def get_all_map_coords(self):
        '''
        @summary: get all coords in map divs
        '''
        all_coords = []
        for map_div in self.source_map_div:
            if len(map_div["list_lat_"]) == len(map_div["list_lon_"]):
                for i, lon_ in enumerate(map_div["list_lon_"]):
                    coord = (float(map_div["list_lon_"][i]), float(map_div["list_lat_"][i]))
                    if not coord in all_coords:
                        all_coords.append(coord)
            else:
                print "In " + str(map_div["id_div_"]) + " :: 'list_lat_' length is not equal to 'list_lon_'"
        return all_coords

    def get_target_div(self, standard_gps, rel_coords):
        kd_results = self.get_kd_tree_result(standard_gps, rel_coords)
        if kd_results:
            if 1 == SEARCH_NODES:
                pass
            elif SEARCH_NODES >= 2:
                target_div = self.search_target_div(kd_results, standard_gps)
                print "target div is :: " + str(target_div)
                if target_div:
                    first_coord, second_coord = target_div[1], target_div[2]
                    target_div = target_div[0]
                    self.deal_with(target_div, first_coord, second_coord)
                else:
                    "search coords are not in same div"
        return True

    def get_kd_tree_result(self, standard_gps, rel_coords):
        '''
        @summary: get kd tree search results
        '''
        kd_results = ""
        if len(rel_coords) >= SEARCH_NODES:
            click_coord = utils.get_rel_coord(standard_gps, self.add_coords_list[0])
            kd_tree = kdtree.create(rel_coords, 2, 0, 0)
            kd_results = kd_tree.search_knn(click_coord, SEARCH_NODES)
        else:
            print "no enough coords for kd tree search, min = " + str(SEARCH_NODES)
        return kd_results

    def search_target_div(self, kd_results, standard_gps):
        '''
        @combine coords in kd results each other, and search in source_map_div
        if two coords in same div return
        '''
        target_div = []
        for i in range(SEARCH_NODES - 1):
            for j in range(i + 1, SEARCH_NODES):
                first = self.get_coord_from_kdtree(kd_results[i])
                second = self.get_coord_from_kdtree(kd_results[j])
                first_gps = (utils.get_gps_coord(standard_gps, first))
                second_gps = (utils.get_gps_coord(standard_gps, second))
                same_div = self.judge_same_div(first_gps, second_gps)
                if same_div:
                    target_div.append(same_div)
                    target_div.append((first_gps, kd_results[i][1]))
                    target_div.append((second_gps, kd_results[j][1]))
                    break
            if target_div:
                break
        return target_div

    def get_coord_from_kdtree(self, kd_node):
        '''
        @summary: split coord infos from kd_node, such as (coord_info, dist)
        '''
        coord = str(kd_node[0])
        coord = coord[coord.index("-") + 1 : coord.index(">")].strip()[1 : -1].split(",")
        coord = (float(coord[0].strip()), float(coord[1].strip()))
        return coord

    def judge_same_div(self, first_gps, second_gps):
        '''
        @summary: judge those two coords whether in same div
        '''
        same_div = ""
        for map_div in self.source_map_div:
            coords = []
            for i, lon_ in enumerate(map_div["list_lon_"]):
                coords.append((float(lon_), float(map_div["list_lat_"][i])))
            if coords:
                if first_gps in coords and second_gps in coords:
                    same_div = map_div
                    break
        return same_div

    def deal_with(self, target_div, first_coord, second_coord):
        '''
        @summary: according dist to deal with different conditions
        '''
        first_gps, first_dist = first_coord[0], first_coord[1]
        second_gps, second_dist = second_coord[0], second_coord[1]
        print "first gps is :: " + str(first_gps) + "; and dist is :: " + str(math.sqrt(first_dist))
        print "second gps is :: " + str(second_gps) + "; and dist is :: " + str(math.sqrt(second_dist))
        print "first distanc to second is :: " + str(utils.get_gps_distance(first_gps, second_gps))
        if first_dist < SQUARE and second_dist < SQUARE:
            self.split_by_one_coord(first_gps, target_div)
        elif first_dist < SQUARE and second_dist >= SQUARE:
            self.split_by_one_coord(first_gps, target_div)
        elif first_dist >= SQUARE and second_dist < SQUARE:
            self.split_by_one_coord(second_gps, target_div)
        elif first_dist >= SQUARE and second_dist >= SQUARE:
            self.split_by_two_coords(first_gps, second_gps, target_div)
        return True

    def split_by_one_coord(self, close_gps, target_div):
        '''
        @summary: split div using one coord
        '''
        if self.is_node(close_gps, target_div):
            print "click coord is node, no need split"
        else:
            print "split coord is :: " + str(close_gps)
            index = self.get_coord_index(target_div, close_gps)
            print "index is :: " + str(index) 
            print "target div is :: " + str(target_div)
            print "gps coord is :: " + str(close_gps)
            if index:
                self.split_div(target_div, index)

    def is_node(self, gps_coord, target_div):
        '''
        @summary: judge the given coord whether is a node coord in target div
        '''
        is_node = False
        list_lon, list_lat = target_div["list_lon_"], target_div["list_lat_"]
        div_nodes = ((float(list_lon[0]), float(list_lat[0])), (float(list_lon[-1]), float(list_lat[-1])))
        if utils.get_gps_distance(gps_coord, div_nodes[0]) < MIN_DISTANCE or \
        utils.get_gps_distance(gps_coord, div_nodes[-1]) < MIN_DISTANCE:
            is_node = True
        return is_node

    def get_coord_index(self, target_div, close_gps):
        '''
        @summary: get given gps`s index in target div
        '''
        div_coords = []
        index = ""
        for i, lon_ in enumerate(target_div["list_lon_"]):
            div_coords.append((target_div["list_lon_"][i], target_div["list_lat_"][i]))
        for i, coord in enumerate(div_coords):
            if coord == close_gps:
                index = i
        return index

    def split_div(self, target_div, index):
        '''
        @summay: split target div into two divs using given index
        '''
        list_lon_, list_lat_, end_node = copy.deepcopy(target_div["list_lon_"]), copy.deepcopy(target_div["list_lat_"]), copy.deepcopy(target_div["id_node_e_"])
        # print "target div gps :: " + str(list_lon_)
        # print "target div gps :: " + str(list_lat_)
        self.cut_div(target_div, index + 1)
        self.add_div(list_lon_[index:], list_lat_[index:], "", end_node)
        self.add_node(list_lon_[index], list_lat_[index], [target_div["id_div_"], self.source_map_div[-1]["id_div_"]])
        self.modify_end_node(end_node, target_div["id_div_"])
        return True

    def modify_end_node(self, end_node, div_id):
        '''
        @summary: modify affected nodes
        '''
        for map_node in self.source_map_node:
            if str(map_node["id_node_"]) == str(end_node):
                div_list = map_node["list_id_div_"]
                if div_id in div_list:
                    index = div_list.index(div_id)
                    div_list[index] = self.source_map_div[-1]["id_div_"]
                    break
        return True

    def cut_div(self, target_div, index, added_coord = ""):
        '''
        @summary: cut target div by index
        '''
        target_div["list_lon_"] = target_div["list_lon_"][:index]
        target_div["list_lat_"] = target_div["list_lat_"][:index]
        if added_coord:
            target_div["list_lon_"].append(added_coord[0])
            target_div["list_lat_"].append(added_coord[1])
        # print "cutted div :: " + str(target_div["list_lon_"])
        # print "cutted div :: " + str(target_div["list_lat_"])
        target_div["id_node_e_"] = MAP_NODE_INDEX
        return True

    def add_div(self, list_lon = [], list_alt = [], start = "", end = "", added_coord = ""):
        '''
        @summary: add new div using specify infos
        '''
        global MAP_DIV_INDEX
        added_div = {}
        added_div["list_lon_"] = list_lon
        added_div["list_lat_"] = list_alt
        if added_coord:
            added_div["list_lon_"].insert(0, min_coord[0])
            added_div["list_lat_"].insert(0, min_coord[1])
        if start:
            added_div["id_node_s_"] = start
        else:
            added_div["id_node_s_"] = MAP_NODE_INDEX
        if end:
            added_div["id_node_e_"] = end
        else:
            added_div["id_node_e_"] = MAP_NODE_INDEX + 1
        added_div["list_id_geo_"] = []
        added_div["id_div_"] = MAP_DIV_INDEX
        self.add_div_schema(added_div)
        MAP_DIV_INDEX += 1
        print "added div is :: " + str(added_div)
        # print "added div lon is :: " + str(added_div["list_lon_"])
        # print "added div lat is :: " + str(added_div["list_lat_"])
        self.source_map_div.append(added_div)
        return True

    def add_div_schema(self, added_div):
        '''
        @summary: set div schema infos
        '''
        schema = {}
        schema["list_line_group_"] = []
        schema["list_line_group_str_"] = []
        schema["list_line_type_"] = [0, 0, 0, 0, 0, 0]
        schema["type_schema_"] = 0
        added_div["schema_"] = schema
        return True

    def add_node(self, lon, lat, div_list):
        '''
        @summary: add new node
        '''
        global MAP_NODE_INDEX
        added_map_node = {}
        added_map_node["id_node_"] = MAP_NODE_INDEX
        added_map_node["lat_"] = float(lat)
        added_map_node["lon_"] = float(lon)
        added_map_node["type_node_"] = None
        added_map_node["list_id_div_"] = div_list
        MAP_NODE_INDEX += 1
        print "added node is :: " + str(added_map_node)
        self.source_map_node.append(added_map_node)
        return True

    def split_by_two_coords(self, first, second, target_div):
        '''
        @summary: split exists div using two coords
        '''
        near_coord = self.get_near_coord(first, second)
        if not self.is_node(near_coord, target_div):
            index1 = self.get_coord_index(target_div, first)
            index2 = self.get_coord_index(target_div, second)
            if index1 <= index2:
                index = index1
            else:
                index = index2
            #print "index is :: " + str(index)
            # if "" != str(index):
            self.insert_target_div(near_coord, target_div, index)
            self.split_by_one_coord(near_coord, target_div)
        else:
            print "the near coord is node"
        return True

    def get_near_coord(self, first, second):
        '''
        @summary: linear_interpolate in coords and get minest coord
        '''
        standard, rel_coords = utils.gps_covert_to_rel_v2([first, second])
        denst_rels = utils.linear_interpolate(rel_coords)
        #print "after linear, length is :: " + str(len(denst_rels))
        dense_gps = utils.rel_covert_to_gps(standard, denst_rels)
        min_dist = math.pi * 6378137
        near_coord = ""
        for linear_gps in dense_gps:
            dist = utils.get_gps_distance(self.add_coords_list[0], linear_gps)
            if dist < min_dist:
                min_dist = dist
                near_coord = linear_gps
        #print "inserted near cood is :: " + str(near_coord)
        return near_coord

    def insert_target_div(self, near_coord, target_div, index):
        '''
        @summary: insert minest coord to target div
        '''
        list_lon = target_div["list_lon_"]
        if not near_coord[0] in target_div["list_lon_"] and not near_coord[1] in target_div["list_lat_"]:
            if index == len(list_lon) - 1:
                target_div["list_lon_"].insert(index, near_coord[0])
                target_div["list_lat_"].insert(index, near_coord[1])
            else:
                target_div["list_lon_"].insert(index + 1, near_coord[0])
                target_div["list_lat_"].insert(index + 1, near_coord[1])
            print "inserted success"
        else:
            print "inserted coord already exists"
        return True