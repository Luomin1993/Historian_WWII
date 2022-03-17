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
这是战地1942 mod开发工具script,用于手持冷兵器的动作创建;
"""

# =================  全局参数  =====================
ANIMATIONS_PATH = "D:/BF1942/cache/animations";
WORK_PATH_LIST = ["D:/BF1942/cache/animations/Crouch/3P",
                  "D:/BF1942/cache/animations/Lie/3P",
                  "D:/BF1942/cache/animations/StandWalkRun/1P",
                  "D:/BF1942/cache/animations/StandWalkRun/3P",
                  "D:/BF1942/cache/animations/WeaponHandling/1p",
                  "D:/BF1942/cache/animations/WeaponHandling/3p"];

"""
复制对应baf文件为新的baf文件;
"""
def copy_baf(NEW_SWORD_NAME):
    for ARCHIVE in WORK_PATH_LIST:
        shutil.copytree(ARCHIVE+"/Katana",ARCHIVE+"/"+NEW_SWORD_NAME);
        BAF_FILES = os.listdir(ARCHIVE+"/"+NEW_SWORD_NAME);
        BAF_FILES = [os.path.join(ARCHIVE+"/"+NEW_SWORD_NAME,ELEMENT) for ELEMENT in BAF_FILES];
        for OLD_NAME in BAF_FILES:
            NEW_NAME = OLD_NAME.replace("Katana",NEW_SWORD_NAME);
            os.rename(OLD_NAME, NEW_NAME);        

"""
替换文件 CON_FILE 中的 re_EFFECT_STR 模式的字符串为 CON_SCRIPT_STRING;
"""
def single_file_replace(CON_FILE,re_EFFECT_STR,CON_SCRIPT_STRING):
    print(CON_FILE);
    FILE_STREAM = open(CON_FILE,'r');
    ALL_LINES = FILE_STREAM.readlines();
    FILE_STREAM.close();
    FILE_STREAM=open(CON_FILE,'w+');
    for THIS_LINE in ALL_LINES:
        SUB_LINE = re.sub(re_EFFECT_STR,CON_SCRIPT_STRING,THIS_LINE);
        FILE_STREAM.writelines(SUB_LINE);
    FILE_STREAM.close();

# ============= main =================
NEW_SWORD_NAME = "china_spear";
# copy_baf(NEW_SWORD_NAME);
re_OLD_WEAPON_NAME = "china_broadsword_mod";
OLD_WEAPON_FILE = "D:/BF1942/cache/animations/AnimationStates_china_broadsword_mod.con";
NEW_CON_FILE = "D:/BF1942/cache/animations/AnimationStates_" + NEW_SWORD_NAME + ".con";
shutil.copyfile( OLD_WEAPON_FILE, NEW_CON_FILE);
single_file_replace(NEW_CON_FILE, re_OLD_WEAPON_NAME, NEW_SWORD_NAME);