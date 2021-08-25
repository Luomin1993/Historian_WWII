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
武器/载具资源收集程序:收集一个武器/载具的静态资源(包括.sm文件,贴图文件,动作文件),
提示用户未定义的projectileTemplate/ObjectTemplate.geometry/ObjectTemplate.addTemplate;
"""

# =================  全局参数  =====================
MY_RESOURCE_PATH = "D:/BF1942/Rebuild_XWWII/Historian_WWII/Patch";
THE_MOD_PATH = "D:/BF1942/Rebuild_XWWII/FH________________RES";
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
re_EFFECT = re.compile(r'Template e_(.*)');
re_CREAT = re.compile(r'ObjectTemplate.create (.*) (.*)');
re_USED = re.compile(r'ObjectTemplate.addTemplate (.*)');
re_MENU = re.compile(r'ObjectTemplate.setPrimaryAmmoIcon "(.*)"|ObjectTemplate.setSecondaryAmmoIcon "(.*)"|ObjectTemplate.setVehicleIcon "(.*)"');

EFFECTs_OF_XWWII = ['e_20mmcannonFume', 'e_20mmDirtBig', 'e_AA-GunDamage', 'e_AichiValDamage', 'e_AichiValFire', '', 'e_Ammolight', 'e_ATrocketFume', 'e_B17Damage', 'e_B17Fire', 'e_Barbwire', 'e_Bf109Damage', 'e_Bf109Fire', 'e_bigShootTrail', 'e_Blood01', 'e_Blood02', 'e_BuildingDust', 'e_BuildingFire', 'e_BuildingFireBig', 'e_BuildingSmoke', 'e_BuildingSmokeIdleDark', 'e_BuildingSmokeSmall', 'e_bulletsmoke', 'e_collision_debrie_concrete', 'e_collision_debrie_metal', 'e_collision_granade_Concrete', 'e_collision_granade_Metal', 'e_collision_granade_Sand', 'e_collision_granade_Wood', 'e_collision_metal', 'e_collision_Other', 'e_collision_ship', 'e_collision_Soldier', 'e_collision_Stone', 'e_collision_Wood', 'e_CorsairDamage', 'e_CorsairFire', 'Em_DaiHatsuDamage', 'e_damageSmoke', 'e_DefGunDamage', 'e_DryDirtSmoke', 'e_dustWind', 'Em_EnterPriseDamage', 'e_ExFumeFact', 'e_ExFumePanz', 'Em_ExFumePOW', 'e_explAni01', 'e_ExplArmor', 'e_ExplBoatArmor', '', '', 'e_ExplDrySand', 'e_ExplGas', 'e_ExplGranade', 'e_ExplNuke', 'e_ExplSmall2', 'e_ExplWindow', 'e_FireMedPlane', 'e_FireSmallYellow', 'Em_FletcherDamage', 'e_fTouchGround', 'Em_GatoDamage', 'e_GibbPlaneSm', 'e_GibbSmokeMetal', 'e_GibbSmokePlane', 'e_GibbSmokeStone', 'e_GibbSmokeWood', 'e_HanomagDamage', 'e_HanomagFire', 'e_HatsuZukiDamage', 'e_Jumplight', 'e_KatyushaDamage', 'e_KatyushaFire', 'e_KatyushaFume', 'e_KTexhaustSmoke', 'e_KubelDamage', 'e_KubelFire', 'Em_LcvpDamage', 'e_LeafTree', 'e_LeafWind', 'e_M10wreck', 'e_M3a1Damage', 'e_M3a1Fire', 'e_MGDirtBig', 'e_MustangDamage', 'e_MustangFire', 'e_Muzz30mm', 'e_Muzz30mmWC', 'e_Muzz88mm', 'e_muzz88mmpz3', 'e_Muzz8mm', 'e_Muzz8mmWC', 'e_MuzzAAgunB', 'e_muzzaagunpz3', 'e_MuzzB17', 'e_MuzzPanz', 'e_MuzzPanzbig', 'e_MuzzPanzsmall', 'e_muzzpanz_churchill', 'e_muzzpanz_e8', 'e_muzzpanz_m36', 'e_muzzpanz_t34', 'e_MuzzPPSh41', 'e_MuzzPriest', 'e_MuzzRifle', 'e_MuzzSBGun', 'e_MuzztankGun', 'e_MuzztankGun1', 'e_MuzztankGun1small', 'e_MuzztankGun2', 'e_Muzztankgun2small', 'e_MuzztankGunbig1', 'e_MuzztankGunbig1smokeless', 'e_MuzztankGunbig2', 'e_PanzDamage', 'e_PanzFire', 'e_PanzShootTrail', 'Em_PlaneDamage', 'Em_PoWDamage', 'e_richoGHeavy', 'e_RichoGlass', 'e_richoGrass', 'e_richoGround', 'e_richoGrsHvy', 'e_RichoKnifeMetal', 'e_RichoMetal', 'e_RichoMetalHeavy', 'e_richoPHeavy', 'e_richoSand', 'e_richoSandbag', 'e_RichoStone', 'e_RichoStoneHeavy', 'e_RichoWater', 'e_richoWood', 'e_richoWoodHeavy', 'e_rocketFume', 'e_rocketFumeBack', 'e_rocketFumeBackBig', 'e_rocketFumeBackNebelwerfer', 'e_SBD-6Damage', 'e_SBD-6Fire', 'e_Scrap25P', 'e_ScrapAABase', 'e_ScrapAAFlak38', 'e_ScrapFlaK_18', 'e_ScrapMetal', 'e_ScrapMetal_AichiVal', 'e_ScrapMetal_B17', 'e_ScrapMetal_Corsair', 'e_scrapmetal_G4M2', 'e_scrapmetal_Ha_Go', 'e_ScrapMetal_Mustang', '', '', 'e_ScrapMetal_Plane', 'e_ScrapMetal_pzl11', 'e_ScrapMetalSmoke', 'e_ScrapMetal_Spitfire', 'e_ScrapMetal_Willy', 'e_ScrapPak40', 'e_shell1250mm', 'e_shell30cal', 'e_Shell792D', 'e_Shell792mm', 'e_shell9mm', 'e_shellAAgun', 'e_shellAir', 'e_shellplane', 'e_ShellPPSh41', 'e_Shell_37mm', 'e_Shell_88mm', 'e_shell_Thompson', 'Em_ShokakuDamage', 'e_SmokeGrenadeWhite', 'e_SmokeGrenadeYellow', 'e_SmokeMortar', 'e_StukaDamage', 'e_StukaFire', 'Em_Sub7cDamage', 'e_Tracer01', 'e_WaterExplosion', 'e_WaterTouchPlane', 'e_waterTouchVehicles', 'e_wdirtPanz', 'e_wdirtWheel', 'e_wdustPanz', 'e_wdustPanzL', 'e_wdustWheelF', 'e_wdustwheelFL', 'e_WespeDamage', 'e_WespeFire', 'e_WillyDamage', 'e_WillyFire', 'e_wreck_fletcherSmoke', 'e_Yak9Damage', 'e_Yak9Fire', 'Em_YamatoDamage', 'e_ZeroDamage', 'e_ZeroFire'] + ['bullet_m1', 'richo_glintbase_m1', 'Decal_metal_m1', 'decal_scorched_m1', 'Decal_Stone_m1', 'Decal_Wood_m1', 'WindDust_m1', 'Planepart1', 'Richo_meshbrown3_m1', 'shell1250mmHi_m1', 'shell9mmHi_m1', 'shellAAgun_m1', 'shellAirLw_m1', 'shell9mmHi_m1', 'shell_37mmHi_m1', 'shellAAgun_m1', 'Tlight_m1'];
EFFECTs_OF_BF1942 = ['bullet_m1', 'richo_glintbase_m1', 'Decal_metal_m1', 'Decal_Stone_m1', 'Decal_Wood_m1', 'WindDust_m1', 'Planepart1', 'Richo_meshbrown3_m1', 'shell1250mmHi_m1', 'shell9mmHi_m1', 'shellAAgun_m1', 'shellAirLw_m1', 'Tlight_m1']+ ['e_AA-GunDamage', 'e_AichiValDamage', 'e_AichiValFire', 'e_B17Damage', 'e_B17Fire', 'e_Barbwire', 'e_Bf109Damage', 'e_Bf109Fire', 'e_Blood01', 'e_BuildingDust', 'e_BuildingFire', 'e_BuildingFireBig', 'e_BuildingSmoke', 'e_BuildingSmokeIdleDark', 'e_BuildingSmokeSmall', 'e_collision_debrie_concrete', 'e_collision_debrie_metal', 'e_collision_granade_Concrete', 'e_collision_granade_Metal', 'e_collision_granade_Sand', 'e_collision_granade_Wood', 'e_collision_metal', 'e_collision_Other', 'e_collision_ship', 'e_collision_Soldier', 'e_collision_Stone', 'e_collision_Wood', 'e_CorsairDamage', 'e_CorsairFire', 'Em_DaiHatsuDamage', 'e_damageSmoke', 'e_DefGunDamage', 'e_DryDirtSmoke', 'e_dustWind', 'Em_EnterPriseDamage', 'e_ExFumeFact', 'e_ExFumePanz', 'Em_ExFumePOW', 'e_ExplAni01', 'e_Explani02', 'e_ExplArmor', 'e_ExplBoatArmor', '', '', 'e_ExplDrySand', 'e_ExplGas', 'e_ExplGranade', 'e_ExplSmall2', 'e_explWater01', 'e_ExplWindow', 'e_FireMedPlane', 'e_FireSmallYellow', 'e_FlakBig', 'e_FlakSmall', 'Em_FletcherDamage', 'e_fTouchGround', 'Em_GatoDamage', 'e_GibbPlaneSm', 'e_GibbSmokeMetal', 'e_GibbSmokePlane', 'e_GibbSmokeStone', 'e_GibbSmokeWood', 'e_HanomagDamage', 'e_HanomagFire', 'e_HatsuZukiDamage', 'e_HoHaDamage', 'e_HoHaFire', 'e_KatyushaDamage', 'e_KatyushaFire', 'e_KatyushaFume', 'e_KettenKradDamage', 'e_KettenKradFire', 'e_KubelDamage', 'e_KubelFire', 'Em_LcvpDamage', 'e_LeafTree', 'e_LeafWind', 'e_LynxDamage', 'e_M3a1Damage', 'e_M3a1Fire', 'e_MustangDamage', 'e_MustangFire', 'e_MuzzAAgun', 'e_MuzzAAgunB', 'e_MuzzB17', 'e_MuzzDefGun', 'e_MuzzGun', 'e_MuzzPanz', 'e_MuzzPriest', 'e_MuzzSexton', 'e_MuzzThomp', 'e_PanzDamage', 'e_PanzFire', 'e_PanzShootTrail', 'Em_PlaneDamage', 'Em_PoWDamage', 'e_richoGHeavy', 'e_RichoGlass', 'e_richoGrass', 'e_richoGround', 'e_richoGrsHvy', 'e_RichoKnifeMetal', 'e_RichoMetal', 'e_RichoMetalHeavy', 'e_richoPHeavy', 'e_richoSand', 'e_richoSandbag', 'e_RichoStone', 'e_RichoStoneHeavy', 'e_RichoWater', 'e_RichoWaterHeavy', 'e_richoWood', 'e_richoWoodHeavy', 'e_rocketFume', 'e_rocketFumeBack', 'e_SBD-6Damage', 'e_SBD-6Fire', 'e_ScrapAABase', 'e_ScrapAAFlak38', 'e_ScrapMetal', 'e_ScrapMetal_AichiVal', 'e_ScrapMetal_B17', 'e_ScrapMetal_Corsair', 'e_ScrapMetal_Ilyushin', 'e_ScrapMetal_Mustang', 'e_ScrapMetal_Plane', 'e_ScrapMetalSmoke', 'e_ScrapMetal_Spitfire', 'e_ScrapMetal_Willy', 'e_shell1250mm', 'e_Shell792D', 'e_Shell792mm', 'e_shell9mm', 'e_shellAAgun', 'e_shellAir', 'e_shellM1Garand', 'Em_ShokakuDamage', 'e_StukaDamage', 'e_StukaFire', 'Em_Sub7cDamage', 'e_Tracer01', 'e_Water06Dive', 'e_Water06DiveSub7', 'e_Water10BDive', 'e_Water10BDiveBack', 'e_Water510Dive', 'e_waterbackBig', 'e_WaterBackMedium', 'e_WaterBackRaft', 'e_WaterBackSmall', 'e_waterBoatSink', 'e_waterBoatSinkEf', 'e_waterBoatSinkSmall', 'e_WaterBoatSvall', '', '', 'e_WaterExplosion', 'e_WaterFront', 'e_WaterFrontBig', 'e_WaterFrontBigSub', 'e_WaterFrontPTBoat', 'e_waterimpact', 'e_waterimpactSmall', 'e_WaterShoreSvall', 'e_WaterTorpedo', 'e_watertouchGuy', 'e_WaterTouchPlane', 'e_waterTouchVehicles', 'e_wdirtPanz', 'e_wdirtWheel', 'e_wdustfeet', 'e_wdustPanz', 'e_wdustPanzGround', 'e_wdustPanzL', 'e_wDustPlane', 'e_wDustPlaneL', 'e_wdustWheelF', 'e_wdustwheelFL', 'e_WespeDamage', 'e_WespeFire', 'e_WillyDamage', 'e_WillyFire', 'e_Yak9Damage', 'e_Yak9Fire', 'Em_YamatoDamage', 'e_ZeroDamage', 'e_ZeroFire'];

# =================  资源搜索归档功能  =====================
"""
采用收集+提示的组合,使得用户可以半自动地移植武器/载具;
"""
class Vehicle(object):
    """手持武器实体类"""
    def __init__(self, NameID):
        super(Vehicle, self).__init__()
        self.NameID = NameID;
        self.MOD_PATH = "";
        self.SM_FILEs = [];
        self.SKE_FILEs = [];
        self.TEXTURE_FILEs = [];
        self.MENU_FILEs = [];
        self.EFFECTs = [];
        self.PROJECTILEs = [];
        self.GEOMETRYs_USED = [];
        self.GEOMETRYs_DEF  = [];
        self.CREATEs = [];
        self.TEMPLATEs = [];

    def check_def(self):
        for GEOMETRY in self.GEOMETRYs_USED:
            if GEOMETRY not in self.GEOMETRYs_DEF:
                print(" ******* Not Defined GEOMETRY *******: " + GEOMETRY);
        for TEMPLATE in self.TEMPLATEs:
            IS_DEF = False;
            for CREATE in self.CREATEs:
                if TEMPLATE==CREATE[1]:IS_DEF=True;
            if TEMPLATE in EFFECTs_OF_XWWII:IS_DEF=True;
            if TEMPLATE in EFFECTs_OF_BF1942:IS_DEF=True;    
            if not IS_DEF:print(" ******* Not Defined *******: "+TEMPLATE);                

    def unrepeated(self):
        # 去重操作;
        self.SM_FILEs = list(set(self.SM_FILEs));
        self.SKE_FILEs = list(set(self.SKE_FILEs));
        self.TEXTURE_FILEs = list(set(self.TEXTURE_FILEs));
        self.EFFECTs = list(set(self.EFFECTs));
        self.PROJECTILEs = list(set(self.PROJECTILEs));
        self.GEOMETRYs_USED = list(set(self.GEOMETRYs_USED));
        self.GEOMETRYs_DEF  = list(set(self.GEOMETRYs_DEF));
        self.CREATEs = list(set(self.CREATEs));
        self.TEMPLATEs = list(set(self.TEMPLATEs));
        TEMP_MENU_FILEs = [];
        for MENU_FILE in self.MENU_FILEs:
            for DDS_PATH in MENU_FILE:
                if DDS_PATH!='':TEMP_MENU_FILEs.append(DDS_PATH);
        self.MENU_FILEs = list(set(TEMP_MENU_FILEs))        

    def show_details(self):
        print('>>>>>>>>>>>>>>  '+ self.NameID +'  <<<<<<<<<<<<<<<<');
        print(self.SM_FILEs);
        print(self.SKE_FILEs);
        print(self.TEXTURE_FILEs);
        print(self.MENU_FILEs);
        print(self.EFFECTs);
        print(self.PROJECTILEs);
        print(self.GEOMETRYs_USED);
        print(self.GEOMETRYs_DEF);
        print(self.CREATEs);
        self.check_def();
        print(' --------------- E N D  ---------------')


# -------- 单个objects.con文件的资源读取 --------
def get_obj_vehicle(CON_FILE):
    FILE_GEOS = open(CON_FILE, "r"); 
    ALL_LINEs = FILE_GEOS.readlines();
    for STR_LINE in ALL_LINEs:
        if re_OBJECT_NAME.findall(STR_LINE)!=[]:
            OBJ_VEHICLE = Vehicle( re_OBJECT_NAME.findall(STR_LINE)[0] );
            break;
    for STR_LINE in ALL_LINEs:
        OBJ_VEHICLE.GEOMETRYs_USED += re_GEOMETRY.findall(STR_LINE);
        OBJ_VEHICLE.PROJECTILEs += re_PROJECT.findall(STR_LINE);
        OBJ_VEHICLE.EFFECTs += re_EFFECT.findall(STR_LINE);
        OBJ_VEHICLE.CREATEs += re_CREAT.findall(STR_LINE);
        OBJ_VEHICLE.SKE_FILEs += re_SKESKN.findall(STR_LINE);
        OBJ_VEHICLE.TEMPLATEs += re_USED.findall(STR_LINE);
        OBJ_VEHICLE.MENU_FILEs += re_MENU.findall(STR_LINE);
    # OBJ_VEHICLE.show_details();
    return OBJ_VEHICLE;

# -------- 单个geometries.con文件的资源读取 --------
def process_geometry_file(OBJ_VEHICLE,GEO_FILE):
    FILE_GEOS = open(GEO_FILE, "r"); 
    ALL_LINEs = FILE_GEOS.readlines();
    for STR_LINE in ALL_LINEs:
        OBJ_VEHICLE.GEOMETRYs_DEF += re_GEOMETRY_DEF.findall(STR_LINE);
        OBJ_VEHICLE.SM_FILEs += re_STDMESH.findall(STR_LINE);
    return OBJ_VEHICLE;

# --------- 单个其他.con文件的资源读取 ------------
def process_con_file(OBJ_VEHICLE,CON_FILE):
    FILE_GEOS = open(CON_FILE, "r"); 
    ALL_LINEs = FILE_GEOS.readlines();
    for STR_LINE in ALL_LINEs:
        OBJ_VEHICLE.GEOMETRYs_USED += re_GEOMETRY.findall(STR_LINE);
        OBJ_VEHICLE.PROJECTILEs += re_PROJECT.findall(STR_LINE);
        OBJ_VEHICLE.EFFECTs += re_EFFECT.findall(STR_LINE);
        OBJ_VEHICLE.CREATEs += re_CREAT.findall(STR_LINE);
        OBJ_VEHICLE.SKE_FILEs += re_SKESKN.findall(STR_LINE);
        OBJ_VEHICLE.TEMPLATEs += re_USED.findall(STR_LINE);    
    # OBJ_VEHICLE.show_details();
    return OBJ_VEHICLE;

# ---------- 从单个.rs文件读取.dds文件路径列表 ---------
def get_dds_files(RS_FILE):
    FILE_GEOS = open(RS_FILE, "r"); 
    ALL_LINEs = FILE_GEOS.readlines();
    DDS_LIST = [];
    for STR_LINE in ALL_LINEs:
        DDS_LIST += re_TEXTURE.findall(STR_LINE);
    return DDS_LIST;    

# --------- 贴图路径收集 ---------------
def process_textures(OBJ_VEHICLE):
    for SM_FILE in OBJ_VEHICLE.SM_FILEs:
        RS_FILE = OBJ_VEHICLE.MOD_PATH + "/standardmesh/" + SM_FILE +".rs";
        if not os.path.exists(RS_FILE): continue; # 应该已含有在BF1942原版里;
        DDS_LIST = get_dds_files(RS_FILE);
        for THIS_DDS in DDS_LIST:
            if THIS_DDS not in OBJ_VEHICLE.TEXTURE_FILEs:OBJ_VEHICLE.TEXTURE_FILEs.append(THIS_DDS);
    return OBJ_VEHICLE;    
        
# ================ 手持武器的资源收集  ====================
# -------- 载具资源爬取主函数 --------
def copy_operation(OBJ_VEHICLE):
    print(" ============ 资源文件复制操作 ===========");
    # 复制菜单UI文件;
    for MENU_FILE in OBJ_VEHICLE.MENU_FILEs:
        ORIGINATING_PATH = OBJ_VEHICLE.MOD_PATH + "/menu/Texture";
        TARGET_PATH = MY_RESOURCE_PATH + "/menu/Texture";
        if not os.path.exists(ORIGINATING_PATH + "/" + MENU_FILE):
            # 也可能dds格式:
            if os.path.exists(ORIGINATING_PATH + "/" + MENU_FILE.replace("tga","dds")):
                shutil.copyfile(ORIGINATING_PATH + "/" + MENU_FILE.replace("tga","dds"),TARGET_PATH + "/" + MENU_FILE.replace("tga","dds"));
                continue;
            print("*** File maybe in BF1942 ***: " +MENU_FILE);continue;
        shutil.copyfile(ORIGINATING_PATH + "/" + MENU_FILE,TARGET_PATH + "/" + MENU_FILE);
    # 复制SKE文件;
    for SKE_FILE in OBJ_VEHICLE.SKE_FILEs:
        ORIGINATING_PATH = OBJ_VEHICLE.MOD_PATH + "/animations";
        TARGET_PATH = MY_RESOURCE_PATH + "/animations";
        if not os.path.exists(ORIGINATING_PATH + "/" + SKE_FILE + ".ske"):print("*** File maybe in BF1942 ***: " +SKE_FILE + ".ske");continue;
        shutil.copyfile(ORIGINATING_PATH + "/" + SKE_FILE + ".ske",TARGET_PATH + "/" + SKE_FILE + ".ske");
        if not os.path.exists(ORIGINATING_PATH + "/" + SKE_FILE + ".skn"):print("*** File maybe in BF1942 ***: " +SKE_FILE + ".skn");continue;
        shutil.copyfile(ORIGINATING_PATH + "/" + SKE_FILE + ".skn",TARGET_PATH + "/" + SKE_FILE + ".skn");
    # 复制SM/RS文件;
    for SM_FILE in OBJ_VEHICLE.SM_FILEs:
        ORIGINATING_PATH = OBJ_VEHICLE.MOD_PATH + "/standardmesh";
        TARGET_PATH = MY_RESOURCE_PATH + "/standardmesh";
        if not os.path.exists(ORIGINATING_PATH + "/" + SM_FILE + ".sm"):print("*** File maybe in BF1942 ***: " +SM_FILE + ".sm");continue;
        shutil.copyfile(ORIGINATING_PATH + "/" + SM_FILE + ".sm",TARGET_PATH + "/" + SM_FILE + ".sm");
        shutil.copyfile(ORIGINATING_PATH + "/" + SM_FILE + ".rs",TARGET_PATH + "/" + SM_FILE + ".rs");
    # 复制DDS文件;
    for DDS_FILE in OBJ_VEHICLE.TEXTURE_FILEs:
        ORIGINATING_PATH = OBJ_VEHICLE.MOD_PATH + "/texture";
        TARGET_PATH = MY_RESOURCE_PATH + "/texture";
        if not os.path.exists(ORIGINATING_PATH + "/" + DDS_FILE + ".dds"):
            # 也可能Tga格式:
            if os.path.exists(ORIGINATING_PATH + "/" + DDS_FILE + ".tga"):
                shutil.copyfile(ORIGINATING_PATH + "/" + DDS_FILE + ".tga",TARGET_PATH + "/" + DDS_FILE + ".tga");
                continue;
            print("*** File maybe in BF1942 ***: " +DDS_FILE + ".dds");continue;
        shutil.copyfile(ORIGINATING_PATH + "/" + DDS_FILE + ".dds",TARGET_PATH + "/" + DDS_FILE + ".dds");

# -------- 载具资源爬取主函数 --------
def read_the_vehicle(VEHICLES_OBJ_PATH):
    # 处理 Objects.con:
    OBJ_VEHICLE = get_obj_vehicle(VEHICLES_OBJ_PATH+"Objects.con");
    OBJ_VEHICLE.MOD_PATH = THE_MOD_PATH;
    # 处理 Geometries.con:
    if os.path.exists(VEHICLES_OBJ_PATH + "Geometries.con"):
        OBJ_VEHICLE = process_geometry_file(OBJ_VEHICLE,VEHICLES_OBJ_PATH + "Geometries.con");
    # 处理 Weapons.con:
    if os.path.exists(VEHICLES_OBJ_PATH + "Weapons.con"):
        OBJ_VEHICLE = process_con_file(OBJ_VEHICLE,VEHICLES_OBJ_PATH + "Weapons.con");
    # 处理 Physics.con:
    OBJ_VEHICLE = process_con_file(OBJ_VEHICLE,VEHICLES_OBJ_PATH + "Physics.con");
    OBJ_VEHICLE.EFFECTs = ["e_"+EFFECT for EFFECT in OBJ_VEHICLE.EFFECTs];
    # 处理贴图;
    OBJ_VEHICLE = process_textures(OBJ_VEHICLE);
    OBJ_VEHICLE.TEXTURE_FILEs = list(set(OBJ_VEHICLE.TEXTURE_FILEs));
    OBJ_VEHICLE.unrepeated();
    OBJ_VEHICLE.show_details();
    copy_operation(OBJ_VEHICLE);

# -------- 一次性移植多个武器 --------
def batch_process():
    VEHICLES_LIST = ["Swordfish"];
    for VEHICLE in VEHICLES_LIST:
        read_the_vehicle(THE_MOD_PATH + "/objects/Vehicles/Air/" + VEHICLE +"/");

if __name__ == '__main__':
    # read_the_weapon(THE_MOD_PATH + "/objects/Handweapons/" + "Nambu" +"/");
    batch_process();