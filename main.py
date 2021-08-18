#!/usr/bin/env python
# -*- coding: utf-8 -*-

__ENV__  =  'python3';
__author__ =  'hanss401';

import numpy as np;
import os;
import sys;
import re;
import cache_data as CDAT;
import shutil;

"""
这是战地1942 mod开发工具script,用于自动搜索资源文件;
包括地图、兵人、载具、武器资源文件的检索和归档;
思路:所有脚本资源归根结底是:ske动作文件、模型文件、贴图文件;
"""

# =================  全局参数  =====================
MY_RESOURCE_PATH = "D:/BF1942/Rebuild_XWWII/WWII_Historian/Patch";
THE_MOD_PATH = "D:/BF1942/Rebuild_XWWII/BG42_____RES";
THE_BF1942_PATH = "D:/BF1942/Rebuild_XWWII/bf1942___RES";
THE_XWWII_RES_PATH = "D:/BF1942/Rebuild_XWWII/XWWII_RES";

# =================  基本数据结构 =====================
TYPE_OBJECT = ['Buildings', 'Common', 'Effects', 'HandWeapons', 'Items', 'MOVE_FILES', 'Soldiers', 'Stationary_Weapons', 'Vegetation', 'Vehicles'];
TYPE_GEO = ['StandardMesh', 'TreeMesh'];

class BF1942_GEO(object):
    def __init__(self, GEO_ID):
        super(BF1942_GEO, self).__init__()
        self.GEO_ID = GEO_ID;
        self.TYPE = TYPE_GEO[0];
        self.GEO_DIR = "";
        self.STDMESH = "";
        self.TXTUREs = [];

class BF1942_OBJ(object):
    def __init__(self, NAME_ID):
        super(BF1942_OBJ, self).__init__()
        self.NAME_ID = NAME_ID;
        self.TYPE = TYPE_OBJECT[0];
        self.OBJECT_DIR = "";
        self.GEO_ID = "";
        self.STDMESHs = [];
        self.TXTUREs = [];
        self.DEPENDENT_OBJs = [];

# =================  公用函数功能  =====================
def print_dict(DICT_ZYX_2rd,NAME='DICT TYPE'):
    print('---------------- '+ NAME +' ------------------------------');
    for KEY in DICT_ZYX_2rd.keys():
        print( str(KEY) +' : '+ str(DICT_ZYX_2rd[KEY]) );     

# -------------- 合并已有Dict和实例List -------------------
def combine_dict_and_list(DICT_BG42_OBJs,ALL_OBJs):
    for THIS_OBJ in ALL_OBJs:
        if type(THIS_OBJ)==BF1942_OBJ:
            if THIS_OBJ.NAME_ID in DICT_BG42_OBJs.keys():continue;
            DICT_BG42_OBJs[THIS_OBJ.NAME_ID] = THIS_OBJ;
        if type(THIS_OBJ)==BF1942_GEO:
            if THIS_OBJ.GEO_ID in DICT_BG42_OBJs.keys():continue;
            DICT_BG42_OBJs[THIS_OBJ.GEO_ID] = THIS_OBJ;    
    return DICT_BG42_OBJs;        

# ------------ 返回文件夹下的文件夹名和文件名 --------------
def get_Dirs_and_Files(DIR_NAME):
    LIST_DIR = os.listdir(DIR_NAME);
    DIR_NAME_LIST = [];
    FILE_NAME_LIST = [];
    for ELEMENT in LIST_DIR:
        THIS_PATH = os.path.join(DIR_NAME, ELEMENT);
        if os.path.isdir(THIS_PATH):DIR_NAME_LIST.append(ELEMENT);
        else:FILE_NAME_LIST.append(ELEMENT);
    return (DIR_NAME_LIST,FILE_NAME_LIST);    

# ------------ 返回文件夹下的结构目录(广度优先搜索) --------------
def get_Dirs_All(DIR_NAME):
    # 在这LIST_DIR是一个队列;
    LIST_DIR = os.listdir(DIR_NAME);
    LIST_DIR = [os.path.join(DIR_NAME, ELEMENT) for ELEMENT in LIST_DIR];
    STANDARD_DIRS = [];
    while LIST_DIR != []:
        if not os.path.isdir(LIST_DIR[0]):del(LIST_DIR[0]);continue;
        STANDARD_DIRS.append(LIST_DIR[0]);
        del(LIST_DIR[0]);
        for ELEMENT in os.listdir(STANDARD_DIRS[-1]):
            THIS_PATH = os.path.join(STANDARD_DIRS[-1], ELEMENT);
            if os.path.isdir(THIS_PATH):LIST_DIR.append(THIS_PATH);
    STANDARD_DIRS = [THIS_PATH.replace('\\','/') for THIS_PATH in STANDARD_DIRS];
    return STANDARD_DIRS;

# ------------ 读取Geometries.con中的所有定义 --------------
def get_geos_from_file(GEOMETRY_PATH):
    FILE_GEOS = open(GEOMETRY_PATH, "r"); # 读取"Objects.con";
    RE_MESH_DEF = re.compile(r'GeometryTemplate.create StandardMesh (.*)');
    RE_TREE_DEF = re.compile(r'GeometryTemplate.create TreeMesh (.*)');
    RE_FILE = re.compile(r'GeometryTemplate.file (.*)');
    RE_TEXTURE = re.compile(r'ObjectTemplate.create (.*)');
    ALL_LINEs = FILE_GEOS.readlines();INDEX = 0;
    ALL_GEOs = [];
    while INDEX < len(ALL_LINEs):
        MESH_RES = RE_MESH_DEF.findall(ALL_LINEs[INDEX]);
        TREE_RES = RE_TREE_DEF.findall(ALL_LINEs[INDEX]);
        if MESH_RES==[] and TREE_RES==[]:INDEX+=1;continue;
        if MESH_RES!=[]:THIS_GEO = BF1942_GEO(MESH_RES[0].lower());
        if TREE_RES!=[]:THIS_GEO = BF1942_GEO(TREE_RES[0].lower());
        THIS_GEO.GEO_DIR = GEOMETRY_PATH.replace('\\','/');
        INDEX+=1; # 先增值一次,以防下面的循环直接break;
        while INDEX <len(ALL_LINEs):
            THIS_RES = RE_FILE.findall(ALL_LINEs[INDEX]);
            GEO_DEF_RES = RE_MESH_DEF.findall(ALL_LINEs[INDEX]) + RE_TREE_DEF.findall(ALL_LINEs[INDEX]);
            if GEO_DEF_RES!=[]:break; # geometry没有声明file;
            INDEX+=1; # 增值一定在这,以防漏掉GEO的声明;
            if THIS_RES==[]:continue;
            THIS_GEO.STDMESH = THIS_RES[0];
            break;
        ALL_GEOs.append(THIS_GEO);
        INDEX+=1;
    return ALL_GEOs;            

# ------------ 读取Objects.con中的所有simple实体 --------------
def get_simple_objs_from_file(OBJECT_PATH):
    FILE_OBJECTS = open(OBJECT_PATH, "r"); # 读取"Objects.con";
    RE_SIMPLE_OBJ = re.compile(r'ObjectTemplate.create SimpleObject (.*)');
    RE_GEO = re.compile(r'ObjectTemplate.geometry (.*)');
    RE_OBJ = re.compile(r'ObjectTemplate.create (.*)');
    ALL_LINEs = FILE_OBJECTS.readlines();INDEX = 0;
    ALL_OBJs = [];
    while INDEX < len(ALL_LINEs):
        # print(ALL_LINEs[INDEX]);
        THIS_RES = RE_SIMPLE_OBJ.findall(ALL_LINEs[INDEX]);
        if THIS_RES==[]:INDEX+=1;continue;
        THIS_OBJ = BF1942_OBJ(THIS_RES[0].lower());
        THIS_OBJ.OBJECT_DIR = OBJECT_PATH.replace('\\','/');
        INDEX+=1; # 先增值一次,以防下面的循环直接break;
        while INDEX <len(ALL_LINEs):
            THIS_RES = RE_GEO.findall(ALL_LINEs[INDEX]);
            OBJ_DEF_RES = RE_OBJ.findall(ALL_LINEs[INDEX]);
            if OBJ_DEF_RES!=[]:break; # geometry没有声明;
            INDEX+=1; # 增值一定在这,以防漏掉OBJ的声明;
            if THIS_RES==[]:continue;
            THIS_OBJ.GEO_ID = THIS_RES[0].lower();
            break;
        ALL_OBJs.append(THIS_OBJ);
        INDEX+=1;
    return ALL_OBJs;        

# ------------ 返回文件夹下的Geo --------------
def get_All_GEOs(GEO_PATH):
    # 首次触及到"*.con"的时候,说明这是一个obj单位文件夹;
    LIST_DIR = os.listdir(GEO_PATH);
    LIST_DIR_DICT = {};
    for ELEMENT in LIST_DIR:LIST_DIR_DICT[os.path.join(GEO_PATH, ELEMENT)] = ELEMENT;
    ALL_GEOs = {};
    LIST_DIR = [os.path.join(GEO_PATH, ELEMENT) for ELEMENT in LIST_DIR];
    while LIST_DIR != []:
        # print(LIST_DIR[0]);
        IS_OBJ_DIR = False;
        for ELEMENT in os.listdir(LIST_DIR[0]):
            if not os.path.isdir(os.path.join(LIST_DIR[0],ELEMENT)):
                # 判定LIST_DIR[0]是obj单位文件夹;
                IS_OBJ_DIR = True;
        if IS_OBJ_DIR:
            if "Geometries.con" not in os.listdir(LIST_DIR[0]):del(LIST_DIR[0]);continue; # 没有要读取的定义文件;
            ALL_GEOs = combine_dict_and_list(ALL_GEOs,get_geos_from_file(LIST_DIR[0] + "/Geometries.con"));
            del(LIST_DIR[0]);continue;
        # LIST_DIR[0]下仍然全是文件夹;
        for ELEMENT in os.listdir(LIST_DIR[0]):
            LIST_DIR_DICT[os.path.join(LIST_DIR[0], ELEMENT)] = ELEMENT;
            LIST_DIR.append(os.path.join(LIST_DIR[0], ELEMENT));
        del(LIST_DIR[0]);    
    return ALL_GEOs;

# ------------ 返回文件夹下的Obj实体 --------------
def get_All_Objs(OBJECT_PATH):
    # 首次触及到"*.con"的时候,说明这是一个obj单位文件夹;
    LIST_DIR = os.listdir(OBJECT_PATH);
    LIST_DIR_DICT = {};
    for ELEMENT in LIST_DIR:LIST_DIR_DICT[os.path.join(OBJECT_PATH, ELEMENT)] = ELEMENT;
    ALL_OBJs = {};
    LIST_DIR = [os.path.join(OBJECT_PATH, ELEMENT) for ELEMENT in LIST_DIR];
    while LIST_DIR != []:
        # print(LIST_DIR[0]);
        IS_OBJ_DIR = False;
        for ELEMENT in os.listdir(LIST_DIR[0]):
            if not os.path.isdir(os.path.join(LIST_DIR[0],ELEMENT)):
                # 判定LIST_DIR[0]是obj单位文件夹;
                IS_OBJ_DIR = True;
        if IS_OBJ_DIR:
            if "Objects.con" not in os.listdir(LIST_DIR[0]):del(LIST_DIR[0]);continue; # 这是bf1942中定义过但是这里重载的实体;
            ALL_OBJs = combine_dict_and_list(ALL_OBJs,get_simple_objs_from_file(LIST_DIR[0] + "/Objects.con"));
            del(LIST_DIR[0]);continue;
        # LIST_DIR[0]下仍然全是文件夹;
        for ELEMENT in os.listdir(LIST_DIR[0]):
            LIST_DIR_DICT[os.path.join(LIST_DIR[0], ELEMENT)] = ELEMENT;
            LIST_DIR.append(os.path.join(LIST_DIR[0], ELEMENT));
        del(LIST_DIR[0]);    
    return ALL_OBJs;

# ------------ 初始化MY_RESOURCE_PATH --------------
def init_mkdir():
    if os.listdir(MY_RESOURCE_PATH) != []:return;
    STANDARD_DIRS = get_Dirs_All(THE_XWWII_RES_PATH);
    STANDARD_DIRS = [THIS_PATH.replace(THE_XWWII_RES_PATH,MY_RESOURCE_PATH) for THIS_PATH in STANDARD_DIRS];
    for THIS_PATH in STANDARD_DIRS:
        if not os.path.exists(THIS_PATH):os.makedirs(THIS_PATH)
    # return STANDARD_DIRS;

# =================  资源搜索归档功能  =====================
"""
资源搜索归档基本思路:指定声明文件展开搜索资源;
Fatal Resource:骨骼文件,动作文件;(比如DHSK这种坦克附带的机枪,如若没有也会出错)
Optional Resource:特效文件,贴图文件;
"""

# ------------ 地图归档函数 --------------
def map_resource_place_on_file(MAP_MAIN_PATH):
    """
    Object单元数据结构:
    {ID:Object-Data},Object-Data是一个类,含有文件夹路径,Object类型,依赖的Object,所需Geometry,所需贴图信息;
    Object ---> Geometry ---> Standardmesh文件;
    """
    # ------------- STEP-I : 读取该地图中所有静态实体;
    FILE_STATIC_OBJECTS = open(MAP_MAIN_PATH + "/StaticObjects.con", "r");
    RE_STATIC_OBJ = re.compile(r'Object.create (.*)');
    MAP_STATIC_OBJs = [];
    for THIS_LINE in FILE_STATIC_OBJECTS.readlines():
        THIS_RES = RE_STATIC_OBJ.findall(THIS_LINE);
        if THIS_RES!=[]:
            THIS_RES[0] = THIS_RES[0].lower();
            if THIS_RES[0] not in MAP_STATIC_OBJs:MAP_STATIC_OBJs.append(THIS_RES[0]);
    # ------------- STEP-II : 读取各种资源Mod里的实体字典;
    DICT_BF1942_OBJs = get_All_Objs("D:/BF1942/Rebuild_XWWII/bf1942___RES/objects/Buildings");
    DICT_XWWII_OBJs = get_All_Objs("D:/BF1942/Rebuild_XWWII/XWWII_RES/objects/Buildings");
    # ------------- STEP-III : 查找重复;
    for THIS_OBJ in MAP_STATIC_OBJs:
        if (THIS_OBJ in DICT_BF1942_OBJs.keys()) or (THIS_OBJ in DICT_XWWII_OBJs.keys()):
            del(MAP_STATIC_OBJs[MAP_STATIC_OBJs.index(THIS_OBJ)]);
    #  ------------- STEP-IV : 查看无法找到的OBJ;
    DICT_BG42_OBJs = get_All_Objs("D:/BF1942/Rebuild_XWWII/BG42_____RES/objects/Buildings");
    for THIS_OBJ in MAP_STATIC_OBJs:
        if THIS_OBJ not in DICT_BG42_OBJs.keys():
            print(THIS_OBJ);

if __name__ == '__main__':
    # DIR_NAME = "D:/BF1942/Isolate-RFA";
    # print(get_Dirs_and_Files(DIR_NAME));
    # print(init_mkdir());
    # init_mkdir();
    MAP_MAIN_PATH = "D:/BF1942/Rebuild_XWWII/BG42_____RES/bf1942/levels/3712-fall_of_nanking";
    map_resource_place_on_file(MAP_MAIN_PATH);
    # print_dict(get_All_Objs("D:/BF1942/Rebuild_XWWII/BG42_____RES/objects/Buildings"));
    # ALL_OBJs = get_All_Objs("D:/BF1942/Rebuild_XWWII/BG42_____RES/objects/Buildings");
    # for THIS_OBJ_ID in ALL_OBJs.keys():print(( ALL_OBJs[THIS_OBJ_ID].NAME_ID, ALL_OBJs[THIS_OBJ_ID].OBJECT_DIR, ALL_OBJs[THIS_OBJ_ID].GEO_ID));
    # ALL_GEOs = get_All_GEOs("D:/BF1942/Rebuild_XWWII/BG42_____RES/objects/Buildings");
    # for THIS_GEO_ID in ALL_GEOs.keys():print(( ALL_GEOs[THIS_GEO_ID].GEO_ID, ALL_GEOs[THIS_GEO_ID].GEO_DIR, ALL_GEOs[THIS_GEO_ID].STDMESH));
