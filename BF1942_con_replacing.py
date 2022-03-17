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
这是战地1942 mod开发工具script,用于替换特定字符串;
"""

# =================  全局参数  =====================
MY_RESOURCE_PATH = "D:/BF1942/Rebuild_XWWII/Historian_WWII/Patch-WF";
THE_MOD_PATH = "D:/BF1942/Rebuild_XWWII/FIN__________RES";
THE_BF1942_PATH = "D:/BF1942/Rebuild_XWWII/bf1942___RES";
THE_XWWII_RES_PATH = "D:/BF1942/Rebuild_XWWII/XWWII_RES";
re_STDMESH = re.compile(r'GeometryTemplate.file (.*)');
re_TEXTURE = re.compile(r'texture "texture/(.*)";');
re_SKESKN = re.compile(r'animations/(.*).ske');
re_NAME_TEXTURE = re.compile(r'(.*)/(.*).dds');
re_OBJECT_NAME = re.compile(r'ObjectTemplate.create PlayerControlObject (.*)');
re_PROJECT = re.compile(r'ObjectTemplate.projectileTemplate (.*)');
re_GEOMETRY = re.compile(r'ObjectTemplate.geometry (.*)');
re_GEOMETRY_DEF = re.compile(r'GeometryTemplate.create StandardMesh (.*)');
re_EFFECT = re.compile(r'ObjectTemplate.lodDistance (.*)');
re_CREAT = re.compile(r'ObjectTemplate.create (.*) (.*)');
re_USED = re.compile(r'ObjectTemplate.addTemplate (.*)');
re_MENU = re.compile(r'ObjectTemplate.setPrimaryAmmoIcon "(.*)"|ObjectTemplate.setSecondaryAmmoIcon "(.*)"|ObjectTemplate.setVehicleIcon "(.*)"');

EFFECTs_OF_XWWII = ['e_20mmcannonFume', 'e_20mmDirtBig', 'e_AA-GunDamage', 'e_AichiValDamage', 'e_AichiValFire', '', 'e_Ammolight', 'e_ATrocketFume', 'e_B17Damage', 'e_B17Fire', 'e_Barbwire', 'e_Bf109Damage', 'e_Bf109Fire', 'e_bigShootTrail', 'e_Blood01', 'e_Blood02', 'e_BuildingDust', 'e_BuildingFire', 'e_BuildingFireBig', 'e_BuildingSmoke', 'e_BuildingSmokeIdleDark', 'e_BuildingSmokeSmall', 'e_bulletsmoke', 'e_collision_debrie_concrete', 'e_collision_debrie_metal', 'e_collision_granade_Concrete', 'e_collision_granade_Metal', 'e_collision_granade_Sand', 'e_collision_granade_Wood', 'e_collision_metal', 'e_collision_Other', 'e_collision_ship', 'e_collision_Soldier', 'e_collision_Stone', 'e_collision_Wood', 'e_CorsairDamage', 'e_CorsairFire', 'Em_DaiHatsuDamage', 'e_damageSmoke', 'e_DefGunDamage', 'e_DryDirtSmoke', 'e_dustWind', 'Em_EnterPriseDamage', 'e_ExFumeFact', 'e_ExFumePanz', 'Em_ExFumePOW', 'e_explAni01', 'e_ExplArmor', 'e_ExplBoatArmor', '', '', 'e_ExplDrySand', 'e_ExplGas', 'e_ExplGranade', 'e_ExplNuke', 'e_ExplSmall2', 'e_ExplWindow', 'e_FireMedPlane', 'e_FireSmallYellow', 'Em_FletcherDamage', 'e_fTouchGround', 'Em_GatoDamage', 'e_GibbPlaneSm', 'e_GibbSmokeMetal', 'e_GibbSmokePlane', 'e_GibbSmokeStone', 'e_GibbSmokeWood', 'e_HanomagDamage', 'e_HanomagFire', 'e_HatsuZukiDamage', 'e_Jumplight', 'e_KatyushaDamage', 'e_KatyushaFire', 'e_KatyushaFume', 'e_KTexhaustSmoke', 'e_KubelDamage', 'e_KubelFire', 'Em_LcvpDamage', 'e_LeafTree', 'e_LeafWind', 'e_M10wreck', 'e_M3a1Damage', 'e_M3a1Fire', 'e_MGDirtBig', 'e_MustangDamage', 'e_MustangFire', 'e_Muzz30mm', 'e_Muzz30mmWC', 'e_Muzz88mm', 'e_muzz88mmpz3', 'e_Muzz8mm', 'e_Muzz8mmWC', 'e_MuzzAAgunB', 'e_muzzaagunpz3', 'e_MuzzB17', 'e_MuzzPanz', 'e_MuzzPanzbig', 'e_MuzzPanzsmall', 'e_muzzpanz_churchill', 'e_muzzpanz_e8', 'e_muzzpanz_m36', 'e_muzzpanz_t34', 'e_MuzzPPSh41', 'e_MuzzPriest', 'e_MuzzRifle', 'e_MuzzSBGun', 'e_MuzztankGun', 'e_MuzztankGun1', 'e_MuzztankGun1small', 'e_MuzztankGun2', 'e_Muzztankgun2small', 'e_MuzztankGunbig1', 'e_MuzztankGunbig1smokeless', 'e_MuzztankGunbig2', 'e_PanzDamage', 'e_PanzFire', 'e_PanzShootTrail', 'Em_PlaneDamage', 'Em_PoWDamage', 'e_richoGHeavy', 'e_RichoGlass', 'e_richoGrass', 'e_richoGround', 'e_richoGrsHvy', 'e_RichoKnifeMetal', 'e_RichoMetal', 'e_RichoMetalHeavy', 'e_richoPHeavy', 'e_richoSand', 'e_richoSandbag', 'e_RichoStone', 'e_RichoStoneHeavy', 'e_RichoWater', 'e_richoWood', 'e_richoWoodHeavy', 'e_rocketFume', 'e_rocketFumeBack', 'e_rocketFumeBackBig', 'e_rocketFumeBackNebelwerfer', 'e_SBD-6Damage', 'e_SBD-6Fire', 'e_Scrap25P', 'e_ScrapAABase', 'e_ScrapAAFlak38', 'e_ScrapFlaK_18', 'e_ScrapMetal', 'e_ScrapMetal_AichiVal', 'e_ScrapMetal_B17', 'e_ScrapMetal_Corsair', 'e_scrapmetal_G4M2', 'e_scrapmetal_Ha_Go', 'e_ScrapMetal_Mustang', '', '', 'e_ScrapMetal_Plane', 'e_ScrapMetal_pzl11', 'e_ScrapMetalSmoke', 'e_ScrapMetal_Spitfire', 'e_ScrapMetal_Willy', 'e_ScrapPak40', 'e_shell1250mm', 'e_shell30cal', 'e_Shell792D', 'e_Shell792mm', 'e_shell9mm', 'e_shellAAgun', 'e_shellAir', 'e_shellplane', 'e_ShellPPSh41', 'e_Shell_37mm', 'e_Shell_88mm', 'e_shell_Thompson', 'Em_ShokakuDamage', 'e_SmokeGrenadeWhite', 'e_SmokeGrenadeYellow', 'e_SmokeMortar', 'e_StukaDamage', 'e_StukaFire', 'Em_Sub7cDamage', 'e_Tracer01', 'e_WaterExplosion', 'e_WaterTouchPlane', 'e_waterTouchVehicles', 'e_wdirtPanz', 'e_wdirtWheel', 'e_wdustPanz', 'e_wdustPanzL', 'e_wdustWheelF', 'e_wdustwheelFL', 'e_WespeDamage', 'e_WespeFire', 'e_WillyDamage', 'e_WillyFire', 'e_wreck_fletcherSmoke', 'e_Yak9Damage', 'e_Yak9Fire', 'Em_YamatoDamage', 'e_ZeroDamage', 'e_ZeroFire'] + ['bullet_m1', 'richo_glintbase_m1', 'Decal_metal_m1', 'decal_scorched_m1', 'Decal_Stone_m1', 'Decal_Wood_m1', 'WindDust_m1', 'Planepart1', 'Richo_meshbrown3_m1', 'shell1250mmHi_m1', 'shell9mmHi_m1', 'shellAAgun_m1', 'shellAirLw_m1', 'shell9mmHi_m1', 'shell_37mmHi_m1', 'shellAAgun_m1', 'Tlight_m1'];
EFFECTs_OF_BF1942 = ['bullet_m1', 'richo_glintbase_m1', 'Decal_metal_m1', 'Decal_Stone_m1', 'Decal_Wood_m1', 'WindDust_m1', 'Planepart1', 'Richo_meshbrown3_m1', 'shell1250mmHi_m1', 'shell9mmHi_m1', 'shellAAgun_m1', 'shellAirLw_m1', 'Tlight_m1']+ ['e_AA-GunDamage', 'e_AichiValDamage', 'e_AichiValFire', 'e_B17Damage', 'e_B17Fire', 'e_Barbwire', 'e_Bf109Damage', 'e_Bf109Fire', 'e_Blood01', 'e_BuildingDust', 'e_BuildingFire', 'e_BuildingFireBig', 'e_BuildingSmoke', 'e_BuildingSmokeIdleDark', 'e_BuildingSmokeSmall', 'e_collision_debrie_concrete', 'e_collision_debrie_metal', 'e_collision_granade_Concrete', 'e_collision_granade_Metal', 'e_collision_granade_Sand', 'e_collision_granade_Wood', 'e_collision_metal', 'e_collision_Other', 'e_collision_ship', 'e_collision_Soldier', 'e_collision_Stone', 'e_collision_Wood', 'e_CorsairDamage', 'e_CorsairFire', 'Em_DaiHatsuDamage', 'e_damageSmoke', 'e_DefGunDamage', 'e_DryDirtSmoke', 'e_dustWind', 'Em_EnterPriseDamage', 'e_ExFumeFact', 'e_ExFumePanz', 'Em_ExFumePOW', 'e_ExplAni01', 'e_Explani02', 'e_ExplArmor', 'e_ExplBoatArmor', '', '', 'e_ExplDrySand', 'e_ExplGas', 'e_ExplGranade', 'e_ExplSmall2', 'e_explWater01', 'e_ExplWindow', 'e_FireMedPlane', 'e_FireSmallYellow', 'e_FlakBig', 'e_FlakSmall', 'Em_FletcherDamage', 'e_fTouchGround', 'Em_GatoDamage', 'e_GibbPlaneSm', 'e_GibbSmokeMetal', 'e_GibbSmokePlane', 'e_GibbSmokeStone', 'e_GibbSmokeWood', 'e_HanomagDamage', 'e_HanomagFire', 'e_HatsuZukiDamage', 'e_HoHaDamage', 'e_HoHaFire', 'e_KatyushaDamage', 'e_KatyushaFire', 'e_KatyushaFume', 'e_KettenKradDamage', 'e_KettenKradFire', 'e_KubelDamage', 'e_KubelFire', 'Em_LcvpDamage', 'e_LeafTree', 'e_LeafWind', 'e_LynxDamage', 'e_M3a1Damage', 'e_M3a1Fire', 'e_MustangDamage', 'e_MustangFire', 'e_MuzzAAgun', 'e_MuzzAAgunB', 'e_MuzzB17', 'e_MuzzDefGun', 'e_MuzzGun', 'e_MuzzPanz', 'e_MuzzPriest', 'e_MuzzSexton', 'e_MuzzThomp', 'e_PanzDamage', 'e_PanzFire', 'e_PanzShootTrail', 'Em_PlaneDamage', 'Em_PoWDamage', 'e_richoGHeavy', 'e_RichoGlass', 'e_richoGrass', 'e_richoGround', 'e_richoGrsHvy', 'e_RichoKnifeMetal', 'e_RichoMetal', 'e_RichoMetalHeavy', 'e_richoPHeavy', 'e_richoSand', 'e_richoSandbag', 'e_RichoStone', 'e_RichoStoneHeavy', 'e_RichoWater', 'e_RichoWaterHeavy', 'e_richoWood', 'e_richoWoodHeavy', 'e_rocketFume', 'e_rocketFumeBack', 'e_SBD-6Damage', 'e_SBD-6Fire', 'e_ScrapAABase', 'e_ScrapAAFlak38', 'e_ScrapMetal', 'e_ScrapMetal_AichiVal', 'e_ScrapMetal_B17', 'e_ScrapMetal_Corsair', 'e_ScrapMetal_Ilyushin', 'e_ScrapMetal_Mustang', 'e_ScrapMetal_Plane', 'e_ScrapMetalSmoke', 'e_ScrapMetal_Spitfire', 'e_ScrapMetal_Willy', 'e_shell1250mm', 'e_Shell792D', 'e_Shell792mm', 'e_shell9mm', 'e_shellAAgun', 'e_shellAir', 'e_shellM1Garand', 'Em_ShokakuDamage', 'e_StukaDamage', 'e_StukaFire', 'Em_Sub7cDamage', 'e_Tracer01', 'e_Water06Dive', 'e_Water06DiveSub7', 'e_Water10BDive', 'e_Water10BDiveBack', 'e_Water510Dive', 'e_waterbackBig', 'e_WaterBackMedium', 'e_WaterBackRaft', 'e_WaterBackSmall', 'e_waterBoatSink', 'e_waterBoatSinkEf', 'e_waterBoatSinkSmall', 'e_WaterBoatSvall', '', '', 'e_WaterExplosion', 'e_WaterFront', 'e_WaterFrontBig', 'e_WaterFrontBigSub', 'e_WaterFrontPTBoat', 'e_waterimpact', 'e_waterimpactSmall', 'e_WaterShoreSvall', 'e_WaterTorpedo', 'e_watertouchGuy', 'e_WaterTouchPlane', 'e_waterTouchVehicles', 'e_wdirtPanz', 'e_wdirtWheel', 'e_wdustfeet', 'e_wdustPanz', 'e_wdustPanzGround', 'e_wdustPanzL', 'e_wDustPlane', 'e_wDustPlaneL', 'e_wdustWheelF', 'e_wdustwheelFL', 'e_WespeDamage', 'e_WespeFire', 'e_WillyDamage', 'e_WillyFire', 'e_Yak9Damage', 'e_Yak9Fire', 'Em_YamatoDamage', 'e_ZeroDamage', 'e_ZeroFire'];

re_EFFECT_STR = "ObjectTemplate.lodDistance (.*)";
re_REMOVE_CROSSHAIR = "ObjectTemplate.setCrossHairType (.*)";
re_ZOOMFOV = "ObjectTemplate.zoomFov (.*)";
re_CROSS = "ObjectTemplate.setCrossHairType CHTCrossHair";

LIST_CON_FILE_PATH = ["D:/BF1942/Rebuild_XWWII/Historian_WWII/Patch/objects/Vehicles/Land",
                      "D:/BF1942/Rebuild_XWWII/Historian_WWII/Patch-WF/objects/Vehicles/Land",
                      "D:/BF1942/cache/objects/Vehicles/Land",
                      "D:/BF1942/Isolate-RFA/objects/Vehicles/Land"];

# =================  文件搜索功能  =====================
"""
迭代地找全当前根目录下所有文件名为 CON_FILE 的文件;
"""
def get_all_files(ROOT_PATH,CON_FILE):
    FILE_PATH_LIST = [];
    LIST_DIR = os.listdir(ROOT_PATH);
    LIST_DIR = [os.path.join(ROOT_PATH,ELEMENT) for ELEMENT in LIST_DIR];
    while LIST_DIR != []:
        if CON_FILE in os.listdir(LIST_DIR[0]):
            FILE_PATH_LIST.append(LIST_DIR[0]+'/'+CON_FILE);
        for ELEMENT in os.listdir(LIST_DIR[0]):
            if os.path.isdir(os.path.join(LIST_DIR[0],ELEMENT)):    
               LIST_DIR.append(os.path.join(LIST_DIR[0], ELEMENT));
        del(LIST_DIR[0]);
    FILE_PATH_LIST = [CON_FILE.replace('\\','/') for CON_FILE in FILE_PATH_LIST];    
    return FILE_PATH_LIST;

# =================  字符串替换功能  =====================
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

if __name__ == '__main__':
    for ROOT_PATH in LIST_CON_FILE_PATH:
        FILE_PATH_LIST = get_all_files(ROOT_PATH,'Objects.con');
        for CON_FILE in FILE_PATH_LIST:
            single_file_replace(CON_FILE, re_CROSS, "ObjectTemplate.setCrossHairType CHTIcon\nObjectTemplate.crossHairIcon \"IronSights/Iron_CrossHair.tga\"");