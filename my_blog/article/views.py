# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from article import models
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django import forms
import json
from modifydata.DeteleCoord import *
import time
import datetime


reload(sys)
sys.setdefaultencoding('utf8')

JSON_DIR = ""
JSON_FILE = ""


# Create your views here.

# 第一个参数必须是 request，与网页发来的请求有关，request 变量里面包含get或post的内容，用户浏览器，系统等信息在里面

@csrf_exempt
def home(request):
    global JSON_FILE
    if request.method == "POST":
        #print "request.POST:",request.POST["jsondir"]
        # JSON_DIR = str(request.POST["jsondir"])
        JSON_FILE = str(request.POST["jsondir"])

    return render(request,
                      'home.html')

@csrf_exempt
def showmap(request):
    global map_div
    global map_node
    all_div_coord_list = []
    all_node_coord_list = []
    global JSON_DIR
    global JSON_FILE
    if not JSON_DIR or JSON_DIR != JSON_FILE:
        JSON_DIR = JSON_FILE
        fb = open(JSON_DIR, 'r')
        js = json.load(fb)
        map_div = js["map_div_"]
        map_node = js["map_node_"]
    if request.method == "POST":
        status = 0
        result=''
        modify_node_dict={}
        delete_node_dict=[]
        add_node_list = []
        tmp_add_node_dict = {}
        new_node_list = request.POST
        if new_node_list.keys():
            if new_node_list.keys()[0].startswith("save"):
                iden = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
                status = utils.save_json(JSON_FILE, map_div, map_node, iden)
                status = utils.save_json_to_kml(JSON_FILE, map_div, map_node, iden)
                return HttpResponse(json.dumps({
                    "status": status,
                    }))
        for key in new_node_list.keys():
            if key.split('[]')[0].split('[')[0] == "modify":
                modify_node_dict[key.split('[]')[0].split('[')[1].split(']')[0]] = new_node_list.getlist(key)
            elif key.split('[]')[0].split('[')[0] == "delete":
                delete_node_dict.append(key.split('[]')[0].split('[')[1].split(']')[0])
            elif key.startswith("add"):
                index = key[key.index("[") + 1: key.index("]")].strip()
                tmp_add_node_dict[index] = new_node_list.getlist(key)
        if tmp_add_node_dict:
            tmp_keys = sorted(tmp_add_node_dict.keys())
            for key in tmp_keys:
                add_node_list.append(tmp_add_node_dict[key])
        Mcoord = DeteleCoord(map_div,map_node,modify_node_dict,delete_node_dict, add_node_list)
        new_map_div,new_map_node=Mcoord.modify_coord()
        map_div=new_map_div
        map_node=new_map_node
        if len(new_map_div)!=0 and len(new_map_node)!=0:
            for i in range(0, len(new_map_div)):
                if len(new_map_div[i])!=0:
                    coord_dict = {}
                    division_id = new_map_div[i]["id_div_"]
                    coord_dict["lon"] = new_map_div[i]["list_lon_"]
                    coord_dict["lat"] = new_map_div[i]["list_lat_"]
                    all_div_coord_list.append({division_id: coord_dict})
            for j in range(0, len(new_map_node)):
                if len(new_map_node[j]) != 0:
                    coor_node_dict = {}
                    lat = new_map_node[j]["lat_"]
                    lon = new_map_node[j]["lon_"]
                    node_id = new_map_node[j]["id_node_"]
                    list_id_div = new_map_node[j]["list_id_div_"]
                    type_node = new_map_node[j]["type_node_"]
                    coor_node_dict["coord"] = [lat, lon]
                    coor_node_dict["div_id"] = list_id_div
                    coor_node_dict["type_node"] = [type_node]
                    all_node_coord_list.append({node_id: coor_node_dict})
            return HttpResponse(json.dumps({
                "status": status,
                "result": {"div": all_div_coord_list, "node": all_node_coord_list}
            }))
    else:
        #start = datetime.datetime.now()
        for i in range(0, len(map_div)):
            coord_dict = {}
            division_id = map_div[i]["id_div_"]
            coord_dict["lon"] = map_div[i]["list_lon_"]
            coord_dict["lat"] = map_div[i]["list_lat_"]
            all_div_coord_list.append({division_id: coord_dict})
        for j in range(0, len(map_node)):
            coor_node_dict = {}
            lat = map_node[j]["lat_"]
            lon = map_node[j]["lon_"]
            node_id = map_node[j]["id_node_"]
            list_id_div = map_node[j]["list_id_div_"]
            type_node = map_node[j]["type_node_"]
            coor_node_dict["coord"] = [lat, lon]
            coor_node_dict["div_id"] = list_id_div
            coor_node_dict["type_node"] = [type_node]
            all_node_coord_list.append({node_id: coor_node_dict})
        #end = datetime.datetime.now()
        ##print str(end-start)
        return render(request, 'map.html', {"div": json.dumps(all_div_coord_list), "node": json.dumps(all_node_coord_list)})

def save_json_file():
    global JSON_FILE
    now_time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    save_path =  os.path.join(os.path.dirname(JSON_FILE), now_time + ".json")
    json_data = {}
    json_data["map_div_"] = map_div
    json_data["map_node_"] = map_node
    try:
        with open(save_path, 'w') as jsons:
            jsons.write(json.dumps(json_data, indent = 4))
        result = 0
    except e:
        result = 1
    return result
    
