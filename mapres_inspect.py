#!/usr/bin/env python
# -*- coding: utf-8 -*-

__ENV__  =  'python3';
__author__ =  'hanss401';

import numpy as np;
import os;
import sys;
import re;
import cache_data as CDAT;
import main as FUNC;
import shutil;

"""
这是战地1942 mod开发工具script,用于自动搜索资源文件;
地图资源收集程序:收集一个模组的静态地图资源(包括Buildings和Treemesh即可),然后就应该可以载入任意一张图了;
"""

# =================  全局参数  =====================
MY_RESOURCE_PATH = "D:/BF1942/Rebuild_XWWII/Historian_WWII/Patch";
THE_MOD_PATH = "D:/BF1942/Rebuild_XWWII/BG42_____RES";
THE_BF1942_PATH = "D:/BF1942/Rebuild_XWWII/bf1942___RES";
THE_XWWII_RES_PATH = "D:/BF1942/Rebuild_XWWII/XWWII_RES";
re_STDMESH = re.compile(r'GeometryTemplate.file (.*)');
re_TEXTURE = re.compile(r'texture "texture/(.*)";');
re_SKESKN = re.compile(r'animations/(.*).ske');
re_NAME_TEXTURE = re.compile(r'(.*)/(.*).dds');

# =================  资源搜索归档功能  =====================
"""
由于是资源收集 因此不必太理解实体 只需要针对sm、ske、skn、贴图文件进行爬取即可;
"""
class ModStaticRes(object):
    """模组静态文件路径的封装类"""
    def __init__(self, MOD_RES_PATH):
        super(ModStaticRes, self).__init__()
        self.MOD_RES_PATH = MOD_RES_PATH;
        self.RES_STDMESHs = [];
        self.RES_TEXTUREs = [];
        self.RES_SKESKNs  = [];        

    def delete_res(self,TEXTURE_RES):
        if ".dds" in TEXTURE_RES:
            del(self.RES_TEXTUREs[ self.RES_TEXTUREs.index(TEXTURE_RES) ]);
        if ".sm" in TEXTURE_RES:
            del(self.RES_STDMESHs[ self.RES_STDMESHs.index(TEXTURE_RES) ]);
        if ".ske" in TEXTURE_RES:
            del(self.RES_SKESKNs[ self.RES_SKESKNs.index(TEXTURE_RES) ]);

    def archive_processing(self,MY_RESOURCE_PATH):
        # using shutil.copyfile("1.txt","3.txt");
        # ----- 归档模型文件 -----
        print("----- 正在归档模型文件 -----");
        for STDMESH_RES in self.RES_STDMESHs:
            ORIGINATING_PATH = self.MOD_RES_PATH + "/standardmesh";
            TARGET_PATH = MY_RESOURCE_PATH + "/standardmesh";
            FILE_NAME = STDMESH_RES.replace(ORIGINATING_PATH+"/","");
            shutil.copyfile(STDMESH_RES,TARGET_PATH + "/" + FILE_NAME);
            shutil.copyfile(STDMESH_RES.replace(".sm",".rs"),TARGET_PATH + "/" + FILE_NAME.replace(".sm",".rs"));
        # ----- 归档贴图文件 -----
        print("----- 正在归档贴图文件 -----");
        for TEXTURE_RES in self.RES_TEXTUREs:
            ORIGINATING_PATH = TEXTURE_RES; # 已经是绝对路径;
            TARGET_PATH = MY_RESOURCE_PATH + "/texture";
            FILE_NAME = re_NAME_TEXTURE.findall(ORIGINATING_PATH)[0][-1]; # "D:/xxx/ssss/ddd/aaa.dds"匹配为:[('D:/xxx/ssss/ddd', 'aaa')];
            print(TARGET_PATH + "/" + FILE_NAME + ".dds");
            shutil.copyfile(ORIGINATING_PATH,TARGET_PATH + "/" + FILE_NAME + ".dds");
        # ----- 归档动作文件 -----
        print("----- 正在归档动作文件 -----");
        for SKESKN_RES in self.RES_SKESKNs:
            ORIGINATING_PATH = self.MOD_RES_PATH + "/animations";
            TARGET_PATH = MY_RESOURCE_PATH + "/animations";
            FILE_NAME = SKESKN_RES.replace(ORIGINATING_PATH+"/","");
            shutil.copyfile(SKESKN_RES,TARGET_PATH + "/" + FILE_NAME);

# -------- 单个贴图寻找 --------
def find_mono_texture_file(MOD_RES_PATH,TEXTURE_RES):
    # 返回形如:"Russia/RussianBuilding/sbclirf_r.dds"
    LIST_DIR = [MOD_RES_PATH+"/texture"];
    while LIST_DIR != []:
        # 检查dds是否在当前文件夹下;
        if (TEXTURE_RES+".dds") in os.listdir(LIST_DIR[0]):
           return (LIST_DIR[0] + "/" + TEXTURE_RES+".dds").replace("\\","/");
        # 不在,若有文件夹,继续加入队列;
        for ELEMENT in os.listdir(LIST_DIR[0]):
            if os.path.isdir(os.path.join(LIST_DIR[0],ELEMENT)):    
               LIST_DIR.append(os.path.join(LIST_DIR[0],ELEMENT));
        del(LIST_DIR[0]);
    return 0;    

# -------- 单个con文件的资源读取 --------
def disposel_mod_res(CON_FILE,MOD_RES):
    FILE_GEOS = open(CON_FILE, "r"); 
    ALL_LINEs = FILE_GEOS.readlines();
    for STR_LINE in ALL_LINEs:
        ADD_TEXTURE = False;
        SKESKN_RES = re_SKESKN.findall(STR_LINE);
        STDMESH_RES = re_STDMESH.findall(STR_LINE);
        if SKESKN_RES!=[]:
            if os.path.exists(MOD_RES.MOD_RES_PATH + "/animations/" + SKESKN_RES[0]+".ske"): # 若不存在,应该是bf1942自带;
                MOD_RES.RES_SKESKNs.append(MOD_RES.MOD_RES_PATH + "/animations/" + SKESKN_RES[0]+".ske");
        if STDMESH_RES!=[]:
            if os.path.exists(MOD_RES.MOD_RES_PATH + "/standardmesh/" + STDMESH_RES[0] +".sm"): # 若不存在,应该是bf1942自带;
                MOD_RES.RES_STDMESHs.append(MOD_RES.MOD_RES_PATH + "/standardmesh/" +  STDMESH_RES[0]);ADD_TEXTURE = True;
        # 贴图文件的收集;
        if ADD_TEXTURE==False:continue;
        FILE_TEXTURE = open(MOD_RES.RES_STDMESHs[-1] + ".rs", "r"); 
        TXT_LINEs = FILE_TEXTURE.readlines();
        for TXT_LINE in TXT_LINEs:
            TEXTURE_RES = re_TEXTURE.findall(TXT_LINE);
            if TEXTURE_RES!=[]:
                # if os.path.exists(MOD_RES.MOD_RES_PATH + "/texture/" +  TEXTURE_RES[0]+".dds"): # 若不存在,应该是bf1942自带;
                #     MOD_RES.RES_TEXTUREs.append(MOD_RES.MOD_RES_PATH + "/texture/" +  TEXTURE_RES[0]+".dds");
                TEXTURE_FIND = find_mono_texture_file(MOD_RES.MOD_RES_PATH,TEXTURE_RES[0]);
                if TEXTURE_FIND!=0:MOD_RES.RES_TEXTUREs.append(TEXTURE_FIND);
        MOD_RES.RES_STDMESHs[-1] += ".sm";    
    return MOD_RES;        

# -------- mod地图资源爬取函数 --------
def is_entangled(STATIC_FOLDER,THIS_PATH):
    if "/" in THIS_PATH.replace(STATIC_FOLDER+"/",""):
        return True;
    return False;    

# -------- mod地图资源爬取函数 --------
def facsimile_mod_mapres():
    MOD_RES = ModStaticRes(THE_MOD_PATH);
    STATIC_FOLDERs = ["/objects/Buildings","/objects/Vegetation",];
    # ---- STEP I: 收集资源路径 ----
    for STATIC_PATH in STATIC_FOLDERs:
        LIST_DIR = os.listdir(THE_MOD_PATH+STATIC_PATH);
        LIST_DIR = [os.path.join(THE_MOD_PATH+STATIC_PATH, ELEMENT) for ELEMENT in LIST_DIR];
        while LIST_DIR != []:
            print(" ------ 当前资源收集路径队列容量:" + str(len(LIST_DIR)));
            # if "AI" in os.listdir(LIST_DIR[0]):
            #     #print(LIST_DIR[0]);
            #     del(LIST_DIR[0]);
            #     continue;
            if "xwwii" in LIST_DIR[0]:
                #print(LIST_DIR[0]);
                del(LIST_DIR[0]);
                continue;
            for ELEMENT in os.listdir(LIST_DIR[0]):
                # 当前ELEMENT是.con文件;
                if not os.path.isdir(os.path.join(LIST_DIR[0],ELEMENT)):
                    if ".con" not in ELEMENT:continue;
                    MOD_RES = disposel_mod_res(os.path.join(LIST_DIR[0],ELEMENT),MOD_RES);
                # 当前ELEMENT是文件夹;
                if os.path.isdir(os.path.join(LIST_DIR[0],ELEMENT)):    
                   LIST_DIR.append(os.path.join(LIST_DIR[0], ELEMENT));
            del(LIST_DIR[0]); 
    # ---- STEP II: 需要手动归档的资源探测 ----
    RES_MANUALLY_OBLIGED = [];
    for SKESKN_RES in MOD_RES.RES_SKESKNs:
        if is_entangled(THE_MOD_PATH+"/animations",SKESKN_RES):
            RES_MANUALLY_OBLIGED.append(SKESKN_RES);
    for STDMESH_RES in MOD_RES.RES_STDMESHs:
        if is_entangled(THE_MOD_PATH+"/standardmesh",STDMESH_RES):
            RES_MANUALLY_OBLIGED.append(STDMESH_RES);
    # for TEXTURE_RES in MOD_RES.RES_TEXTUREs:
    #     if is_entangled(THE_MOD_PATH+"/texture/",TEXTURE_RES): # TEXTURE_RES形如"Russia/RussianBuilding/sbclirf_r.dds";
    #         RES_MANUALLY_OBLIGED.append(TEXTURE_RES); 
    print(" ------ 以下文件需要手动归档 ---------");
    for TEXTURE_RES in RES_MANUALLY_OBLIGED:
        print(TEXTURE_RES);
        MOD_RES.delete_res(TEXTURE_RES);
    # ---- STEP III: 资源的归档 ----
    MOD_RES.archive_processing(MY_RESOURCE_PATH);
        
        
# ============ T E S T  ================
def TEST_facsimile_mod_mapres1():
    MOD_RES = facsimile_mod_mapres();
    print(MOD_RES.RES_SKESKNs);
    print(MOD_RES.RES_STDMESHs);
    print(MOD_RES.RES_TEXTUREs);

def TEST_facsimile_mod_mapres2():
    facsimile_mod_mapres();

if __name__ == '__main__':
    #TEST_facsimile_mod_mapres1();
    TEST_facsimile_mod_mapres2();