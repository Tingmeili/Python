import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from Utils import utils, run_logging
import math


class ModifyCoord(object):
    def __init__(self):
        self.div_list = []
        self.node_list = []
        self.impact_div_inf = []
        self.direction_mark_x = 0
        self.direction_mark_y = 0
        self.dx = 0
        self.dy = 0
        self.new_div_info_list = []
        self.new_node_info_list = []
        self.new_rel_coord_move = []
        self.logs = run_logging.CheckType()

    def check_abs(self, num):
        if num > 0:
            return num
        elif num < 0:
            return -num

    def modify_to_update_map(self, source_div_list, source_node_list, modify_dict):
        '''
        :param:
        :return:
        '''
        self.div_list = source_div_list
        self.node_list = source_node_list
        # print "modify_dict:", modify_dict
        for node_id, value in modify_dict.items():
            self.logs.info("IIIIi")
            test1, test2 = self.calculate_relation_div(node_id, value)
            self.div_list, self.node_list = test1, test2
        return self.div_list, self.node_list

    def calculate_relation_div(self, modify_node_id, modify_node_new_coord):
        """

        :param modify_node_id: The coordinates of the moving node,example:[u'42.63427444824847', u'-83.74986022710802']
        :param modify_node_new_coord:
        :return:
        """
        modify_node_coord = []
        # print "modify_node_id:", modify_node_id
        self.impact_div_inf = []
        self.new_div_info_list = []
        self.new_node_info_list = []
        self.new_rel_coord_move = []
        for info_div in self.div_list:
            if str(info_div["id_node_e_"]) == str(modify_node_id):
                self.impact_div_inf.append({"end": info_div})
            elif str(info_div["id_node_s_"]) == str(modify_node_id):
                self.impact_div_inf.append({"start": info_div})
            else:
                self.new_div_info_list.append(info_div)
        # print "impact div are :: " + str(self.impact_div_inf)
        for info_node in self.node_list:
            if str(info_node["id_node_"]) == str(modify_node_id):
                modify_node_coord.append(info_node["lat_"])
                modify_node_coord.append(info_node["lon_"])
                new_node_info = info_node
                new_node_info["lat_"] = modify_node_new_coord[0]
                new_node_info["lon_"] = modify_node_new_coord[1]
                self.new_node_info_list.append(new_node_info)

            else:
                self.new_node_info_list.append(info_node)
        # print "move node is :: " + str(modify_node_coord)
        # print "modify_node_id:",modify_node_id
        # print "modify_node_coord:",modify_node_coord
        # print "modify_node_new_coord:",modify_node_new_coord
        test = self.calculate_refer_distance(modify_node_coord, modify_node_new_coord)
        return test, self.new_node_info_list

    def calculate_refer_distance(self, stander_node_coord, new_node_coord):
        """
        :param stander_node_coord:
        :param new_node_coord:
        :return:
        """
        all_node_coord = []
        rel_all_node_coord = []
        all_node_coord.append((float(stander_node_coord[1]), float(stander_node_coord[0])))
        all_node_coord.append((float(new_node_coord[1]), float(new_node_coord[0])))
        # print "all_node_coord:", all_node_coord
        rel_all_node_coord = utils.gps_covert_to_rel(all_node_coord)

        # print "rel_all_node_coord:",rel_all_node_coord
        self.new_rel_coord_move.append([rel_all_node_coord[1][0], rel_all_node_coord[1][1]])
        # print self.new_rel_coord_move
        return self.calculate_div_new_coord()

    def calculate_div_new_coord(self):
        """
        :return:
        """
        for div_info in self.impact_div_inf:
            div_info_coord = []
            new_div_info = {}
            d = 0
            L = 0
            new_rel_div_info_coord = []
            new_gps_div_info_coord = []
            div_len = len(div_info.values()[0]["list_lon_"])
            for i in range(0, div_len):
                div_info_coord.append((div_info.values()[0]["list_lon_"][i], div_info.values()[0]["list_lat_"][i]))
            if div_info.keys()[0] == "end":
                div_info_coord.reverse()  # The anchor point is the first point in the array
            rel_div_info_coord = utils.gps_covert_to_rel(div_info_coord)
            # print "**:",self.new_rel_coord_move
            d = (self.new_rel_coord_move[0][0], self.new_rel_coord_move[0][1])
            L = self.caculate_div_length(rel_div_info_coord)
            for i in range(1, div_len - 1):
                lon = rel_div_info_coord[i][0]
                lat = rel_div_info_coord[i][1]
                l = math.sqrt((rel_div_info_coord[-1][0] - lon) * (rel_div_info_coord[-1][0] - lon) + (
                    rel_div_info_coord[-1][1] - lat) * (rel_div_info_coord[-1][1] - lat))
                new_lon, new_lat = self.caculate_div_new_coord(d, l, L, lon, lat)
                new_rel_div_info_coord.append((new_lon, new_lat))
            new_rel_div_info_coord.append((rel_div_info_coord[-1][0], rel_div_info_coord[-1][1]))
            new_rel_div_info_coord.insert(0, (self.new_rel_coord_move[0][0], self.new_rel_coord_move[0][1]))
            if div_info.keys()[0] == "end":
                new_gps_div_info_coord = utils.rel_covert_to_gps(
                    [div_info.values()[0]["list_lon_"][-1], div_info.values()[0]["list_lat_"][-1]],
                    new_rel_div_info_coord)
                new_gps_div_info_coord.reverse()
            elif div_info.keys()[0] == "start":
                new_gps_div_info_coord = utils.rel_covert_to_gps(
                    [div_info.values()[0]["list_lon_"][0], div_info.values()[0]["list_lat_"][0]],
                    new_rel_div_info_coord)
            new_gps_div_lat_coord = []
            new_gps_div_lon_coord = []
            for coords in new_gps_div_info_coord:
                new_gps_div_lat_coord.append(coords[1])
                new_gps_div_lon_coord.append(coords[0])
            new_div_info = div_info.values()[0]
            new_div_info["list_lat_"] = new_gps_div_lat_coord
            new_div_info["list_lon_"] = new_gps_div_lon_coord
            self.new_div_info_list.append(new_div_info)

        return self.new_div_info_list

    def caculate_div_new_coord(self, d, l, L, lon, lat):
        dx = l / L * d[0]
        dy = l / L * d[1]
        new_lon = dx + lon
        new_lat = dy + lat
        return new_lon, new_lat

    def caculate_div_length(self, div_coords):
        sum_L = 0
        refer_coord = div_coords[0]
        for coord in div_coords:
            if refer_coord == coord:
                continue
            else:
                dx = coord[0] - refer_coord[0]
                dy = coord[1] - refer_coord[1]
                l = math.sqrt(dx * dx + dy * dy)
                sum_L += l
            refer_coord = coord
        return sum_L
