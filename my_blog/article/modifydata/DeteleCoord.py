import os
import sys
import logging
from ModifyCoord import *
from addCoords import *
from Utils import  run_logging
class DeteleCoord(ModifyCoord):
    def __init__(self, source_map_div, source_map_node, modify_dict, delete_list, add_list):
        '''
        :param source_map_div: The original division coordinates taken from the json file
        :param source_map_node:The original node coordinates taken from the json file
        :param modify_dict: The coordinates and id info after modify the nodes
        :param delete_list: The id of the deleted node
        '''
        super(DeteleCoord, self).__init__()
        self.source_map_div = source_map_div
        self.source_map_node = source_map_node
        self.modify_dict = modify_dict
        self.delete_list = delete_list
        self.add_list = add_list
        self.logs = run_logging.CheckType()
    def modify_coord(self):
        if self.add_list:
            add_nodes = addCoords(self.source_map_div, self.source_map_node, self.add_list)
            self.source_map_div, self.source_map_node = add_nodes.add_coords()
        if len(self.modify_dict) != 0:
            self.source_map_div, self.source_map_node = self.modify_to_update_map(self.source_map_div,self.source_map_node,
                                                                                self.modify_dict)
        if len(self.delete_list) != 0:
            self.delete_to_update_map()


        return self.source_map_div, self.source_map_node

    def delete_to_update_map(self):
        '''
        According deleted node update the skeleton

        :return: new_dic_map_json,new_node_map_json

        '''
        #print "self.delete_list:",self.delete_list
        self.logs.info("IIII2")
        for node in self.delete_list:
            list_id_div = []
            for node_dict in self.source_map_node:
                id_node = node_dict["id_node_"]
                if str(node) == str(id_node):
                    #print "****:",1
                    list_id_div = node_dict["list_id_div_"]
                    #print "list_id_div:",list_id_div
                    #print "list_id_div:",len(list_id_div)
                    if len(list_id_div) == 2:
                        self.source_map_div, self.source_map_node = self.update_two_line_div(node, list_id_div)
                    elif len(list_id_div) == 3:
                        self.source_map_div, self.source_map_node = self.update_more_line_div(node, list_id_div)
                    elif len(list_id_div) == 1:
                        self.source_map_div, self.source_map_node = self.source_map_div, self.source_map_node

    def update_two_line_div(self, node_id, list_div):
        """
        :param node_id: id of deleted node
        :param list_div:div of the deleted node impact (This node affects two division)
        :return: return info of div and node
        """
        new_map_inf_div = []
        new_map_inf_node = []
        impact_div_inf = {}
        new_div_info = {}
        for div_dict in self.source_map_div:
            if div_dict["id_div_"] not in list_div:
                new_map_inf_div.append(div_dict)
            else:
                id_node_e = div_dict["id_node_e_"]
                id_node_s = div_dict["id_node_s_"]
                if str(id_node_e) == str(node_id):
                    impact_div_inf['end'] = div_dict
                elif str(id_node_s) == str(node_id):
                    impact_div_inf['start'] = div_dict
        # modify div
        new_div_info = impact_div_inf["end"]
        new_div_info["id_node_e_"] = impact_div_inf["start"]["id_node_e_"]
        new_div_info["list_lat_"] = new_div_info["list_lat_"] + impact_div_inf["start"]["list_lat_"]
        new_div_info["list_lon_"] = new_div_info["list_lon_"] + impact_div_inf["start"]["list_lon_"]
        new_map_inf_div.append(new_div_info)

        # modify node
        end_node_id = new_div_info["id_node_e_"]
        new_node_dic = {}
        other_id = []
        for node_dict in self.source_map_node:
            if str(node_dict["id_node_"]) == str(end_node_id):
                new_node_dic = node_dict
                for id in node_dict["list_id_div_"]:
                    if str(id) != str(impact_div_inf["start"]["id_div_"]):
                        other_id.append(id)
                new_node_dic["list_id_div_"] = other_id
                new_node_dic["list_id_div_"].append(impact_div_inf["end"]["id_div_"])
            elif str(node_dict["id_node_"]) == str(node_id):
                continue
            else:
                new_map_inf_node.append(node_dict)

        new_map_inf_node.append(new_node_dic)
        return new_map_inf_div, new_map_inf_node

    def update_more_line_div(self, node_id, list_div):
        """
        :param node_id: id of deleted node
        :param list_div: div of the deleted node impact (This node affects more than two division)
        :return:return info of div and node
        """
        print "****"
        new_map_inf_div = []
        new_map_inf_node = []
        impact_div_inf = []
        num = 0
        for div_dict in self.source_map_div:
            if div_dict["id_div_"] not in list_div:
                new_map_inf_div.append(div_dict)
            else:
                id_node_e = div_dict["id_node_e_"]
                id_node_s = div_dict["id_node_s_"]
                if str(id_node_e) == str(node_id):
                    impact_div_inf.append({"end": div_dict})
                    num += 1
                elif str(id_node_s) == str(node_id):
                    impact_div_inf.append({"start": div_dict})

        # modify div dict
        if num == 1:
            new_map_inf_div = self.modify_div1_info(impact_div_inf, new_map_inf_div)
        elif num == 2:
            new_map_inf_div = self.modify_div2_info(impact_div_inf, new_map_inf_div)

        # modify node dict
        other_node = []
        new_node_dict = {}
        move_id = 0
        delete_div_id = 0
        for impact_div_dict in impact_div_inf:
            if num == 1:
                if impact_div_dict.keys()[0] == "end":
                    delete_div_id = str(impact_div_dict.values()[0]["id_div_"])
                    move_id = str(impact_div_dict.values()[0]["id_node_s_"])
                else:
                    other_node.append(impact_div_dict.values()[0]["id_div_"])
            if num == 2:
                if impact_div_dict.keys()[0] == "start":
                    delete_div_id = str(impact_div_dict.values()[0]["id_div_"])
                    move_id = str(impact_div_dict.values()[0]["id_node_e_"])
                else:
                    other_node.append(impact_div_dict.values()[0]["id_div_"])
        for node_dict in self.source_map_node:
            if str(node_dict["id_node_"]) == str(node_id):
                continue
            elif str(node_dict["id_node_"]) == str(move_id):
                new_node_dict = node_dict
                for id in new_node_dict['list_id_div_']:
                    if str(id) != str(delete_div_id):
                        other_node.append(id)
                new_node_dict["list_id_div_"] = other_node
            else:
                new_map_inf_node.append(node_dict)
        new_map_inf_node.append(new_node_dict)
        #print "new_map_inf_div:",new_map_inf_div
        #print "new_map_inf_node:",new_map_inf_node
        return new_map_inf_div, new_map_inf_node

    def modify_div1_info(self, impact_div_info, new_map_inf_div):
        new_div_info = {}
        new_div_info1 = {}
        lat = []
        lon = []
        stop_mark_start = 0
        id_start = 0
        for impact_dict in impact_div_info:
            if impact_dict.keys()[0] == "end":
                lat = impact_dict.values()[0]["list_lat_"]
                lon = impact_dict.values()[0]["list_lon_"]
                id_start = impact_dict.values()[0]["id_node_s_"]
            elif impact_dict.keys()[0] == "start" and stop_mark_start == 0:
                new_div_info = impact_dict.values()[0]
                stop_mark_start += 1
            elif impact_dict.keys()[0] == "start" and stop_mark_start == 1:
                new_div_info1 = impact_dict.values()[0]

        new_div_info["list_lat_"] = lat + new_div_info["list_lat_"]
        new_div_info["list_lon_"] = lon + new_div_info["list_lon_"]
        new_div_info["id_node_s_"] = id_start
        new_div_info1["list_lat_"] = lat + new_div_info1["list_lat_"]
        new_div_info1["list_lon_"] = lon + new_div_info1["list_lon_"]
        new_div_info1["id_node_s_"] = id_start
        new_map_inf_div.append(new_div_info)
        new_map_inf_div.append(new_div_info1)
        return new_map_inf_div

    def modify_div2_info(self, impact_div_info, new_map_inf_div):
        new_div_info = {}
        new_div_info1 = {}
        lat = []
        lon = []
        stop_mark_end = 0
        id_end = 0
        for impact_dict in impact_div_info:
            if impact_dict.keys()[0] == "start":
                lat = impact_dict.values()[0]["list_lat_"]
                lon = impact_dict.values()[0]["list_lon_"]
                id_end = impact_dict.values()[0]["id_node_e_"]
            elif impact_dict.keys()[0] == "end" and stop_mark_end == 0:
                new_div_info = impact_dict.values()[0]
                stop_mark_end += 1
            elif impact_dict.keys()[0] == "end" and stop_mark_end == 1:
                new_div_info1 = impact_dict.values()[0]
        new_div_info["list_lat_"] = new_div_info["list_lat_"] + lat
        new_div_info["list_lon_"] = new_div_info["list_lon_"] + lon
        new_div_info["id_node_e_"] = id_end
        new_div_info1["list_lat_"] = new_div_info1["list_lat_"] + lat
        new_div_info1["list_lon_"] = new_div_info1["list_lon_"] + lon
        new_div_info1["id_node_e_"] = id_end
        new_map_inf_div.append(new_div_info)
        new_map_inf_div.append(new_div_info1)
        return new_map_inf_div
