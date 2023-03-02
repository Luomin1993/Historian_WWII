# XWWII2.7补丁包(完美整合版)开发日志
>这个高温假的时间花在了给我最喜欢的二战单机游戏:战地1942模组XWWII制作历史真实化补丁;

XWWII-2.7_setup_pack_full

![在这里插入图片描述](https://img-blog.csdnimg.cn/14582def3e714b44992098baef5a4942.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hhbnNzMg==,size_16,color_FFFFFF,t_70#pic_center)


-------------------------------------------------------

>我将记录一切开发流程和开发技术总结;

-----------------------------------------------
### 预备工作

预备工作如下:

- 安装XWWII2.6安装包(最终原始版本,不是2020夏开发的版本);  FINISHED
- 打上修改人数补丁;   FINISHED
- 尝试独立rfa是否生效;   FINISHED

tips:

- 无论打包出的名字为何,原名必须吻合规范(example:你可以把打包出的结果命名为 menu001.rfa 但是被打包文件一定叫menu);

-----------------------------------------------
### 载具加入

- 调研载具加入方法的教程资料;    FINISHED
- 尝试加入一辆装甲车到ICHI-GO地图中;    FINISHED

tips:

- 复制Objects\Vehicles\Land\下的对应文件夹到XWWII,然后从Objects.con开始修改,思路是着重补全资源文件即可(移植或改用本mod的);
- 似乎Geometries.con已声明引入所有需要的.sm文件;(注意file关键字后)
- 地图的载具重生点详情在singleplayer/ObjectSpawnTemplates.con和ObjectSpawns.con中修改(似乎要直接改Conquest下的);
- 导入载具还是不能分割rfa文件;
- 对于sound资源文件来说,我将其打包后放在XWWII2.7/Archieves文件夹下,并且在XWWII主文件夹下的init.con里声明读取它,导入成功;

-----------------------------------------------
### 导入坦克T-26(仍然是分离rfa实验)

- 导入T-26无贴图到Ichi-Go地图! Failed
- 现在导入FT-17做一组对照试验; Failed

tips:

- 通过反复的对照实验,结论如下:202008的放入T26是分离rfa但是在achieves文件夹下,sys并未真正读入其objects对应文件,因此现象是可载入地图但是载具不出现;
当我们把分离rfa放入XWWII2.7下时,系统读入了它但是载入失败;
- 现象:当T26对应的objects文件被sys读入时,无论是否调用T26,无论什么地图,都无法载入;当T26的仅.sm或贴图存在时无妨;
- 基本验证"ObjectTemplate.XXX"语句都是原版自带的,但是,语句的参数需要排查(特别是涉及调用资源的);
- 我把一些语句加入到安全的.con中,然后检测是否能载入,也是一个试错办法;
- 接近22:00的小实验:纯净XWWII加入T26的Objects文件夹后,CAEN地图也在加载初始跳出;说明并非是除Objects外的文件使全局出错(那么推断sys在加载任意一张map时都会遍历读取所有object!);
- 散步conjecture:越是底层的内容越可能被预先遍历读取:因此很可能是比objects.con底层的code出错; 
- 通过反复对照实验,结果规律吻合上述猜想;

------------------------------------------------
### 找到导入坦克/履带车辆出错的原因

- 对比T34/76和T26的代码来找不同,为T34/76添加可能出错代码来试错(是否任意地图弹出);     FINISHED
- 解决坦克瞄具和炮弹效果的问题;     FINISHED
- 验证是否是weapons.con里"Projectile"部分的"objectTemplate.addTemplate e_PanzShootTrail"决定了炮弹烟火效果;     FINISHED
- 建立一种套用音频文件的方法;     FINISHED

tips:

- 确定就是履带ske的问题;
- 关于坦克瞄具的问题:"objects.con"中的"T26CockPitInternel"的对应sm文件附带的rs文件脚本里提到了的瞄准"texture"文件缺失;
- 可以用已有类似物件的音频给对应的导入物件部分使用:例如给T26使用"../T34-76/Sounds/T34-85TrackR.ssc"来替代;
- weapons.con里"Projectile"部分的"objectTemplate.addTemplate e_PanzShootTrail"去除后,炮弹烟火效果仍然正常;

------------------------------------------------
### 导入轻机枪zb26来替换掉China军队的白朗宁

- 添加zb26到XWWII并找到对应军队的武器定义处修改;     FINISHED
- zb26的动作修改;     FINISHED
- 武器栏的问题修正;     FINISHED    

tips:

- 枪械修改点:音频"../BrenMK1/Sounds/BrenMK1.ssc";以及对应"ske"修改;
- 枪械和部队的绑定(声明Madsen轻机枪装备了中国补给兵),objects.rfa中(前两行是修改,后两行是添加一个code区段):

```
./Items/China/Support/Objects.con:ObjectTemplate.geometry Kit_Madsen
./Items/China/Support/Objects.con:ObjectTemplate.addTemplate Madsen
./Items/ClassKits/Geometries.con:GeometryTemplate.create StandardMesh Kit_Madsen
./Items/ClassKits/Geometries.con:GeometryTemplate.file Madsen_Kit
```

- 要在"animations/multiShotWeaponsMod.inc"中写入"AnimationStateMachine.copyState Madsen v_arg1 Type99 1.0 Type99 1.0";
- 在"/Items/China/Support/Objects.con"的"ObjectTemplate.addWeaponIcon "Weapon/Icon_bar1918.dds""修改;

------------------------------------------------
### 在地图导入建筑物

- 替换单机地图""中的建筑物

Battlecraft1942基础教程:https://tieba.baidu.com/p/3196362759
地图编辑器editor42入门教程:https://tieba.baidu.com/p/1534810509

tips:

- 应该在"XWW2_Ichi-go/StaticObjects.con"中增删;
- Battlecraft1942看不见场景,先打开Berlin,并且移动一下MiniMap即可;

------------------------------------------------
### 修改China军队军服

- 找到定义兵人模型对应的军服.dds文件的地方;完成一个替换中国军服从British到German的实验;

tips:首先"objects/Soldiers"中的定义很重要;

- 脸部贴图文件:"objects/Soldiers"中的"ChineseSoldier/Objects.con"中的"JapSoldierComplexHead"处-引用了-"JapaneseSoldier/Geometries.con"中"GeometryTemplate.file Jap1Face"-引用了-Jap1Face.sm文件(对应的Jap1Face.rs)-引用了-贴图"texture/face_jap1_h.dds";
- 衣服贴图文件:找到了一个直接套用服装的方法,在"ChineseSoldier/Objects.con"直接改"ObjectTemplate.addTemplate BritSoldier3PBody"为"ObjectTemplate.addTemplate GerSoldier1PBody";
- 帽子定义文件:"./Items/China/Support/Objects.con"中声明即可:"ObjectTemplate.addTemplate M1943_Field_Cap"(增添山地帽);
- 其他装备定义:
- 特别注意:有个设置地图特别涂装的文件夹:"textureManager.alternativePath  ../../bf1942/levels/XWW2_Ichi-go/China/"在地图主文件夹的"Init.con"下声明;


------------------------------------------------
### 增强子弹效果

- 可能要从枪械的"e_XXX"对应寻找特效文件修改;

tips:

- 建立Alpha通道教程:https://jingyan.baidu.com/article/ac6a9a5ede8d952b653eacac.html
- PS技巧:用左3快速选择工具去除黑色部分!


------------------------------------------------
### "历史学家"自动搜索程序

- Problem-1:每个Object单元文件夹里,Objects.con可能声明的不止一个Object,而它所对应的Geometry(声明了所需的Standardmesh文件)不一定在同一个文件夹下!
- Problem-1:重载问题,比如"BG42_____RES\objects\Effects\Common"下的Effect.con会不会替换掉XWWII的这个文件?


注意以下定义:"telemark_building_m1"和"telemark_building_death_m1"都是Obj,而"telemark_building_m1"还依赖"telemark_building_death_m1";

```
ObjectTemplate.create Bundle telemark_building_m1
ObjectTemplate.geometry telemark_building_m1
ObjectTemplate.setHasCollisionPhysics 1
ObjectTemplate.addtemplate telemark_building_death_m1
ObjectTemplate.setposition 0/2/0

ObjectTemplate.create SimpleObject telemark_building_death_m1
ObjectTemplate.geometry telemark_building_death_m1
ObjectTemplate.setHasCollisionPhysics 1
```

总而言之,我必须重写"get_All_Objs(OBJECT_PATH)"函数!并且还必须有一个"get_All_GEOs(OBJECT_PATH)"函数;
另外我需要先简单地完成地图资源搜索任务:仅仅加载作为"SimpleObject"的物体:
这样的物体没有Object依赖,并且对应的geometry也就在声明的后行;

我突然想到一个办法可以快速替换国家,只是装备改不了...那就是利用地图文件夹重载换脸部贴图和服装贴图;
也可以试一下,objects文件夹是否可以重载!

我宣布上述idea奏效了,实验是将瓜岛日军补给兵的枪械换成了Bar1918,但是记得在Init.con中定义军队前加入运行语句:

```
run Objects/Items/Japanese/Support/Objects
```

------------------------------------------------
### 新增地图

这里是地图制作流程:

- 解压,修改阵营信息等等,修改载入图片可运行;
- 兵模资源重载/修改;贴图/旗帜进一步修改;
- 载具进一步修改等等;

tips:

- 设置载入图/载入UI等等:./Menu/Init.con:"game.setLoadPicture ../../bf1942/levels/XWW2_Ichi-go/textures/load.tga";

```
game.setLoadPicture ../../bf1942/levels/XWW2_Benghazi/Menu/XWW2_Benghazi.tga
game.setMapId "XWWII"
game.setServerInfoIcon ../../bf1942/levels/XWW2_Market_Garden/menu/serverInfo.dds
```

- 需要修改地图名字的地方:

```
PS D:\BF1942\Rebuild_XWWII\bf1942(maps_of_XWWII)\XWW2_Ichi-go> grep -r  "XWW2_Ichi-go" .
./Init.con:textureManager.alternativePath  ../../bf1942/levels/XWW2_Ichi-go/China/
./Init.con:water.texLayer1 bf1942/levels/XWW2_Ichi-go/texture/water01
./Menu/Init.con:game.setLoadPicture ../../bf1942/levels/XWW2_Ichi-go/textures/load.tga
./Objects/clouds/Geometries.con:GeometryTemplate.file ../bf1942/levels/XWW2_Ichi-go/StandardMesh/cloudbit_m1
./StandardMesh/cloudbit_m1.rs:  texture "bf1942/levels/XWW2_Ichi-go/customtextures/cloudbit_m1";
```

- 关于TGA载入图格式:只需要在PS里保存为32位Tga即可;

我刚刚完成了法军军帽的地图重载载入,关键是记得几何脚本也要run,而静态装备只需导入对应的模型/贴图即可(无需再声明):

```
run objects/Items/Canadian/Common/Geometries
run objects/Items/Canadian/Common/Objects
run objects/Items/Canadian/Engineer/Objects
...
```

加载重载贴图的语句:

```
textureManager.alternativePath  ../../bf1942/levels/XWW2_Poznan/Textures/
```

- 关于如何更改菜单旗帜,我的idea是重载在地图主目录下重载Menu文件夹的对应文件(同理Objects的重载):
只能通过把菜单旗帜贴图放入"textureManager.alternativePath"的文件夹才能重载选兵种目录的旗帜;

**task**:修改八月风暴的交战方为伪满洲国;

头盔这种装备也可以在Objects.rfa的"Items/Equipment/Geometries.con"中预先声明!

```
./Items/Equipment/Geometries.con:GeometryTemplate.create StandardMesh Jap_Helmet
./Items/Equipment/Geometries.con:GeometryTemplate.file Jap_Helmet_m1
```
然后还是得写个Items/Equipment/Objects.con下的声明:

```
ObjectTemplate.create KitPart Manzu_cap
ObjectTemplate.geometry Manzu_cap
ObjectTemplate.setBoneName A
ObjectTemplate.setCopyLinksCount 0
```

够折腾的,还是用老办法做完的(但是若是为了全局共享,可以用上述方法);

找到了一个XWWIIX模组,里面有些好东西,并且它是XWWII基础上构建的mod,也许可以将其容纳进来;
今天我要确定要加入的阵营,武器的加强随后到来:

- 要加入的阵营:伪满洲国、中国八路军、自由法国、意大利、波兰; [Finished]
- 然后就是为每个阵营新增载具和武器;
- 最后就是添加一些公共的载具;

------------------------------------------------
### 新增阵营意大利

这里是新增思路:

- 对应的objects下文件的复制粘贴;
- 脸模、骨骼、动作skn文件乃至静态装备的文件移植(还有旗帜文件、语言语音文件);

注意下Soldiers/ItalianSoldier/Geometries.con既有skn又有sm文件需要导入:

```
GeometryTemplate.create AnimatedMesh Soldier/3PItBody
GeometryTemplate.setSkin animations/ItBody.skn
GeometryTemplate.file ItBody
... ...
```

在明确绝对没有资源问题后仍然反复载入地图出错:放弃,尝试微改操作,从澳大利亚模板改;
怀疑的问题:重定义??我发现本来有ItalianSoldier在XWWII下定义;

感悟:一蹴而就的方法不一定是好方法,能一步步挖掘问题的方法才是;

Ok,试了改定义名仍然不行,那么设计以下对照实验:
- 去掉定义,仅仅留下资源文件,载入任意地图; [Failed]
- 去掉定义,去掉资源文件,载入任意地图; [Failed]
- 去掉资源文件,仅仅留下定义,载入任意地图;

我现在重新版本回滚然后再重做以上实验!一点点改变添加,先添加贴图,然后菜单、sm、ske文件;
原因似乎是因为animations的解压打包**又一次**漏掉了T-26的履带动作导致!
即使加入定义也没问题了...小结论:兵人模型的文件缺失不会导致无关地图载入错误;

下面我要做一张测试地图以方便测试阵营!选择:Berlin;

- 法军移植载入问题:兵种文件夹应为"XXXKit",然后在其他兵种里通过Common声明的资源一定要再声明下;

研究如何控制头戴帽子的位置定义;猜想与下列代码有关:

```
GeometryTemplate.create StandardMesh Frz_Helmet
GeometryTemplate.file Frz_Helmet
GeometryTemplate.scale 1/1/4 // 分别控制(面朝人脸)纵向/来向/横向;
GeometryTemplate.setLodDistance 0 0
GeometryTemplate.setLodDistance 1 30  // 好像没用;
GeometryTemplate.setLodDistance 2 100
```

OK,现在开始可能要移植不少的武器和载具,目前为阵营要补充的武器载具如下(准备XWWII的模板文件用VSCODE打开):

手持武器4步走修改:收集文件(别漏Kit)/改脚本(特效音效等)/注册(Kit声明/动作copy)/测试;
(换弹速度等在1pAnimationsTweakingMod.con中设置)

- 武器:WZ39-Mors冲锋枪;Breda轻机枪;Bereta冲锋枪;Carcano步枪;
- 载具:7TP战车;m13-40轻型坦克;as37breda装甲车;

定时清理文件夹的RFA解压文件以保证在RFA内部的修改总是有效的!

移植载具的步骤:收集文件(别漏ske)/改脚本(特效音效等)(注意ObjectTemplate.addTemplate后的资源是否包含)/测试;

- 另外关于人物中弹的烟雾效果(Inspired by the movie <<拯救大兵瑞恩>>);

- 在BC42里查看地图坐标,然后在StaticObjects.con中添加Building object成功,但是winrfa修改会内存溢出,所以只能先修改再打包(Y控制高度);

7tpTwin移植的矩形模具/冒烟问题:Tank的ske不能冒用/开头定义的那几个"e_XXX"不能随意篡改(冒烟由e_PanzerFire引起吧);

地图资源收集程序:收集一个模组的静态地图资源(包括Buildings和Treemesh即可),然后就应该可以载入任意一张图了;

完成了上述程序,现在用BG42开始测试,首先完成归档后,测试XWWII本来的地图,看是否正常运行;

ok,测试记录如下:
所有资源未加载时,能载入XWWII地图联机/单机,和BG42联机(无BG42建筑物);
所有资源加载时,能载入XWWII地图联机,不能载入单机,和BG42联机;
猜测是因为Object资源确实造成的;现在分别添加进去Objects下的文件,看看有什么情况;

- 仅添加Buildings,能载入XWWII地图联机/单机,和BG42联机/单机(BG42建筑物无贴图);

现在发现BG42的地图建筑物贴图的载入逻辑:它不会直接写"Texture/Chinese/XXX.dds":
而是在地图的声明文件里通过"textureManager.alternativePath Texture/Chinese"来直接可以调用;
所以直接遍历Texture中任意一个文件夹来实现复制即可!

程序改写之前,依赖贴图为664个;另外如果MOVE_FILES有AI文件夹,则不读取其资源!
修改之后的测试:
所有资源加载时,能载入XWWII地图联机/单机,BG42联机无法载入(看来MOVE_FILES似乎并不只是AI文件的影响);
现在再次去掉MOVE_FILES文件夹尝试:

(以上这个问题的结论貌似不应该下结论"看来MOVE_FILES似乎并不只是AI文件的影响",因为似乎也是因为抛弃了读取所有含AI文件夹的依赖资源但是在rfa打包时仍然涵盖了这些含有AI文件夹的Buildings的声明,最后应该是**文件缺失**导致的载入失败!)

BG42单机无法载入但联机可以,现在不去除Objects的Buildings内含AI的物体再尝试(只是移除MOVE_FILES文件夹);
BG42联机/单机(BG42建筑物无贴图)可载入了;

我发现所有复制的.rs文件是二进制的!而且所有对应的sm文件和rs文件一模一样大小;似乎是将.sm当成了.rs文件;
修改后测试不再有任何问题;

----------------------------------------------------------------------------
## 关于自动化手持武器和载具的移植过程(也许是自动化一部分)

- 问题描述:考虑现在有一个文件夹含有若干待移植的武器/载具的Objects文件夹集合;
还有已知的资源文件夹B以及一个目标补丁文件夹T含有模型和贴图等等文件夹,
问题是如何尽可能自动化移植过程;

**思路**:我们已知移植修改的基本流程是:文件收集文件(别漏Kit)/改脚本(特效音效等)/注册(Kit声明/动作copy);
那么这里面比较好自动化的步骤无疑是第一步;那么可以:

- 用正则表达式去完成模型、贴图、动作文件的探测和收集;
- 关于音频文件、特效文件的部分,可以探测并将它们的情况写入一个报告文件:比如音频声明在哪一行,特效文件有哪些以及在哪,以及在原版和XWWII是否存在等等(这可以预先够造一个表来判断);
- 因此综上,后两步可以手动完成;

今晚又移植了几张地图,均没有什么问题(除了个别物体不出现);
下面开始添加人物中弹的烟雾效果(Inspired by the movie <<拯救大兵瑞恩>>);

最终方案 改写Fx_BloodSmoke的对应贴图色彩来实现的,它引用的是4个渐变的烟团贴图;


### 2021/08/19 特殊元素的加入
今天的任务是尽可能给XWWII2.7加入更多的特殊元素,在广度上可能难以一时超越,计划加入:

- 战马,自行车,三轮摩托;喇叭,旗子;日军军帽,盒子炮(连发);苏军军帽,...;   <完成!>
(看来后期的程序还得再加一个探测未知的addTemplate资源的警报)

自行车导入后老是倒下 解决问题的过程中发现"ObjectTemplate.geometry"的缺失不会导致载入错误 
另外 我发现缺失的"invisible_wheel_small_m1"可能与其倒下有关(是的已解决)

Horn的导入后 载入地图失败 后来发现Kit_XXX是与它绑定的 导入后载入成功(下面修改动作) 那么问题是什么样的手持武器必须由Kit_XXX绑定?
动作问题的修正:原来动作文件夹下有两个"StandWalkRun"和"WeaponHandling"需要在"multiShotWeaponsMod.inc"中用"AnimationStateMachine.copyState2 Vuvuzela v_arg1"调用!

按下吹号就跳出的问题;怀疑和"ObjectTemplate.projectileTemplate WhistleProjectile"有关!
验证一下是否和WhistleProjectile有关:
去掉WhistleProjectile定义,把WhistleProjectile赋给WZ冲锋枪看看会不会跳出:结果并不会,说明不是它的问题,应该还是文件缺失之类的问题;
之前动作没有时摁下开火键并未出错(甚至有声音),但是加入"StandWalkRun"动作文件后反而出错;
将"StandWalkRun"的Aim动作文件删除后测试:吹号时动作错乱但是不跳出,切武器回Horn一瞬间拿对了但是跳出;
加载整个Soccermod的动作包试试;加载无效,难道是含.con的文件作怪?
去除冲突声明文件尝试:仍然跳出;难道是因为.baf文件之间存在依赖?
去除1PFireVuvuzela.baf尝试:单机可以 多人跳出;
删除1PLieFireVuvuzela再尝试:均正常了;(那为何它在Soccermod里的表现并没问题?)

在控制Horn大小时:"GeometryTemplate.scale 1/号角的粗细/长度" 但是它的相对位置没变
尝试位置可以用如下代码调节:
```
ObjectTemplate.addTemplate VuvuzelaComplex
ObjectTemplate.setPosition 0/0.0/-0.5  // 后移
ObjectTemplate.addTemplate VuvuzelaSimple
ObjectTemplate.setPosition 0/0.0/-0.5  // 后移
```

下面要解决武器选项图片显示问题:先实验是不是定义军种数量超过五个导致的,将STEN_MKI替换为Horn试试;(成功)

导入旗子,在选择兵种时跳出.改变为"ObjectTemplate.addTemplate RefereeFlasssssss"未载入即跳出,说明原本加载RefereeFlag实体成功了的;
注意到ObjectTemplate.setAnimationState RefereeFlagBlow 加入"RefereeFlagBlow.baf"再尝试:在选择兵种时跳出;
发现Geometries.con有"GeometryTemplate.setSkin animations/refereeflaganim.skn",打包后:在选择兵种时跳出;

注意,Horn的Fire动作和Flag的加载跳出似乎有相似之处,现在我假设它们的跳出原因是一样的,那么按照这个思路(以下陈述均为假设):
- Horn的Fire动作加载时,由于关联了另一个动作文件,于是跳出;
- Flag的文件没有缺失(否则无法载入地图),但是在加载时就关联了另一个动作文件以至于跳出;

现在我要试下"Flag的文件缺失"会发生什么(写错Objects里的某个.ske):在地图载入一半时跳出;
(写错Geometries里的某个.ske):在地图载入完成后选完武器才跳出;

以上事实可以推知:手持武器的加载具有yard属性,那么同理,合理猜测之前Horn/Flag的跳出也是每个延迟加载的资源不存在;

注释掉AnimatedRefereeFlag(动态)相关部分:在选择兵种时跳出;
修改animations/RefereeFlag.ske为animations/KnifeAllies.ske:在选择兵种时跳出;
注释掉RefereeFlagComplex的ske部分:载入兵种成功但是只有旗帜没有旗杆;(另外发现ObjectTemplate.lodselector CardLodSelector处未定义,补全了定义)
关于ObjectTemplate.lodselector缺失会不会引起错误的实验(改错WZ冲锋枪的一处lodselector):尚未载入地图即跳出;
改错(副武器)Colt的一处lodselector:尚未载入地图即跳出;

将"GeometryTemplate.create AnimatedMesh refereeflaganim"改为"GeometryTemplate.create StandardMesh refereeflaganim"就也载入了旗帜;
并且用如下语句完成姿势修正:
```
ObjectTemplate.addTemplate RefereeFlagComplex
ObjectTemplate.setRotation 0/0/90
ObjectTemplate.addTemplate RefereeFlagSimple
ObjectTemplate.setRotation 0/0/90
```

- 修正国军军帽后即完成2.7版性能部分;开始美工和地图设置处理;

还差这几样实体导入:Bereta冲锋枪;Carcano步枪;m13-40轻型坦克;
为避免rfa打包错误,只能每次实验无误才可以解包覆盖!!!!!

- 导入手动单发武器后 拉栓动作没有的问题:原来单发武器比连发多更多动作声明代码在"1pAnimationsTweaking.con"和"3pAnimationsTweaking.con"里(大概40 lines);
导入后仍然无效

另有意大利兵种菜单IT_1不显示问题:兵种编码和格栏对应,"ObjectTemplate.create Kit IT_1"对应
```
ObjectTemplate.setKitIcon 1 "kits/Canadian_engineer.tga" // 用哪个图随意;
ObjectTemplate.setKitName 1 "Engineer"
ObjectTemplate.setKitActiveName 1 "Active Engineers"
``` 

总结:步枪的动作修正是非常复杂的:

**i)**:"1pAnimationsTweakingMod.con"和"3pAnimationsTweakingMod.con"内做动作速度修正;
**ii)**:"AnimationStatesShoot.con"内做动作声明:
```
AnimationStateMachine.setActiveState Ub_FireCarcano
AnimationStateMachine.addTransitionWhenDone Ub_StandReloadCarcano
AnimationStateMachine.setActiveState Ub_LieFireCarcano
AnimationStateMachine.addTransitionWhenDone Ub_LieReloadCarcano
```
**iii)**:"singleShotWeaponsMod.inc"内声明模板复制"AnimationStateMachine.copyState Type38Carbine v_arg1 No4 1.0 K98 1.0";
**iv)**:两大段动作声明代码在"1pAnimationsTweaking.con"和"3pAnimationsTweaking.con"里;

替换当前目录下所有文件中的"3712-fall_of_nanking"为"XWW2_Nanking":
sed -i "s/3712-fall_of_nanking/XWW2_Nanking/g" `grep -r "3712-fall" ./`

Sancantan地图的载入问题无疑和设置的Objects重生模板有关,但是具体是什么问题还待研究;
(另外 地图一定要改mapID)

那么接下来依托地图对游戏继续进行真实性修改:
- XWW2_Ichi-go:加入马匹,T26的贴图;  √
- XWW2_Manzhouli:载具修正;  √
- XWW2_Nanking:载具修正;旗帜修正;载入图;  √
- XWW2_Poznan:载具修正,装备修正;  √
- XWW2_Rostov:苏军军帽及装备修正;载入图; √

当前问题:
- 加入XWW2,战地1942自己的原版地图就无法载入;去掉后即可;(原来是bf1942下声明了"game.addModPath Mods/XWWII/");
- XWW2自行车加入前,Kubel车轮存在;(那么猜测和这个有关);
"ObjectTemplate.invisible 1"这句很关键!那么试试"ObjectTemplate.invisible 0"(修改无效)
看看改变 GeometryTemplate.file Kubel_Hul_M1 为 Willy_WheL_M1 有没有用;(无效,看来是其他定义语句的问题!)

我已经通过对照实验确定了最接近的两个有轮/无轮版本之间的差异在XWWII_2.7下的几个文件,那么现在要对比:
逐渐删去出问题的元素然后找到变化即问题所在;

- 删除自行车定义:无轮;
- 删除自行车的sm模型:却发现Horse调用了kubel_wheell_m1.sm(作为隐形轮??),删掉后:有了;
已按照这个思路解决;

Flag无法装备苏军 此时需要先再尝试装备自由法国试试; 没有问题;
再按照原法军的格式进行 完成没有问题;

未作地图的载入封面:XWW2_Nanking,XWW2_Neringa,XWW2_Rostov,XWW2_Sancantan,XWW2_Volturno;

地图XWW2_Neringa单机无法载入/联机可以的问题;
去掉单机/联机的if/else兵种生成语句后:单机无法载入/联机可以,且选遍兵种;

回滚版本发现哪一版开始不能载入XWW2_Neringa:XWWII-完成子弹烟雾
(和BG42的地图实体加入有关吗?但是地图实体似乎又和AI无关,难道是类似的MOVE_FILES问题?)
确实 注释掉 game.addModPath Mods/XWWII/XWWII_Patch/ 即可;

声明载入图的语句:"game.setLoadPicture ../../texture/load_img/XWW2_Volturno.tga"

为中国军队制作吹号兵种;Kit_Vuvuzela只能单独存在,不能搭配其他武器;

Pegasus Bridge似乎也使用了BG42的地图元件;(确实)
(为了解决这个问题,仅仅在来自BG42的地图加上"game.addModPath Mods/XWWII/XWWII_Patch/"岂不更合理?)

添加特殊兵种:飞行员(英德日美),装甲兵(德:参照FH兵种"4TankCommanderLuger");
(兵种文件夹下可以有许多兵种,但是必须是每5个一组声明的)
制作"icon_axis_pilot.tga"和"icon_allied_pilot.tga"的UI图标

突然明白Kit_XXX是什么了 就是摁下G之后在地面上的那个装备包;

加入英德飞行员后,在载入一半多时候失败;发现兵种命名编码是1~5而非0~4修改后:在载入一半多时候失败;
修改为5个一组的文件夹格式:在载入一半多时候失败;
将飞行员武器全部调整为法军已有:在载入一半多时候失败;
更换掉飞行员帽子(为 Jpnryakubou):在载入一半多时候失败;
换回正常兵种之后:正常载入;为正常兵种EBA_0添加飞行员帽子Brit_Pilot_Helmet:成功...;
对英伦空战的地图实施飞行员兵种重载:成功;

XWW2X地图新增计划:加入Pacific贴图补充; 发现一个问题:当XWWIIX不在Mods时,加载不出来部分地图(加入的太平洋两张);
而从之前Berlin的开发看出,确实会去引用XWWIIX的资源!
加入XWWIIX的Achieves资源仍然无用("game.addmodPath Mods/Patch_from_XWWIIX/");
加回XWWIIX仍然无用(但英伦空战可以载入 载入图却遗失/路径没改 但是又证明了XWWII里也会去引用XWWIIX的资源)
"XWWII/init"改为"game.customGameFlushArchives 1":仍然无用;
"XWWII/init"增加"game.addmodPath Mods/XWWIIX/":恢复正常

小技巧:查找含有"Forager"但是不含有"rem"的字段:
```
grep -r "Forager" . | grep -v "rem"
```

发现XWW2_Tinian下定义Geometries的语句有路径问题,改正后载入正常:但是又证明了XWWII之前去引用XWWIIX的资源;但是为何现
在剪切XWWIIX文件夹再放回后不再读取?奇怪;
所有地图修改后载入成功;

探究同名资源使用优先顺序的规则:
"game.addModPath Mods/XWWII/Patch_from_XWWIIX/"在最前时候:有效;
"game.addModPath Mods/XWWII/Patch_from_XWWIIX/"在最后时候:无效;(MP18的声音也证实这个顺序的影响结论;)

不调用就没有影响的资源有:aimeshes.rfa,menu.rfa,sound.rfa,standardmesh.rfa,texture.rfa;(FH的必要资源大小不超过1G;)
那么通过将FH的必要资源打包放在Mods/XWWII/Patch_from_FH/下是否就能调用了呢?
0.加入卡累利阿图载入失败;在TEST_BERLIN加入BT7不出现;
1.路径修正后:载入地图立即跳出(此时含整个Objects); 
2.仅仅加入Vehicles文件夹(也加入了Common):载入地图立即跳出;
3.仅仅加入Vehicles/Land文件夹(也加入了Common):载入地图立即跳出;
4.仅仅加入Vehicles/Land/BT7 文件夹(也加入了Common):载入地图立即跳出;
5.去掉整个Objects:载入地图立即跳出;
6.去掉整个Animations:载入地图即将完成时候跳出;Animations,aimeshes,menu和textures存在时:载入不到一半时候跳出;
7.去掉整个aimeshes:载入地图即将完成时候跳出;aimeshes,menu和textures存在时:载入成功;
8.去掉整个menu:载入地图即将完成时候跳出;(此时只剩下sm文件和textures);仅menu和textures存在时:载入成功;
9.去掉整个standardmesh.rfa:载入成功;
10.去掉声明的Animations加入(还存在aimeshes,menu和textures):载入地图即将完成时候跳出;
11.Patch_from_FH顺序调整到"game.addModPath Mods/BF1942/"之后重做10:载入成功;
12.Patch_from_FH顺序调整到"game.addModPath Mods/BF1942/"之后重做8:载入成功;(此时也含有去掉声明的 Animations)
13.再次尝试加入整个Objects(时间戳最新的那个):载入地图即将完成时候跳出;(刚开始的加载明显慢了很多);
14.同13设置,在载入Fall_of_Carantan单机时不到一半跳出;
15.缩减Objects只含武器和载具(含有Common):载入地图即将完成时候跳出;
16.仅仅包含Handweapons:载入成功;
17.在16基础上加上 StationaryWeapons:载入地图即将完成时候跳出; 只留下8种武器StationaryWeapons:载入成功;
18.在地图中加入 Stationary_wz30:载入地图即将完成时候跳出;
19.删掉Animations下所有baf文件:载入地图即将完成时候跳出;(检查了一下应该是wz30引用了mg42的部件后者没有定义)
20.试用另一个定义完全的 Flak37_2Fach_BaseWithCamera:载入地图即将完成时候跳出;
21.调用Mas38给意大利军队:载入成功,只是没有开枪和正确持枪动作;

猜想:
- **5和6的差异的原因**:Animations中含有找不到的文件,因此,刚开始载入就跳出(Found_ERR);
(Animations必然有些关于实体的声明,找不到时肯定会跳出)
- **8和9的差异的原因**:需要知晓地图加载的最后在干什么才能判断;
- **10和8的类似的原因**:需要知晓地图加载的最后在干什么才能判断;
- **10和11的差异的原因**:原版和FH的动作定义存在重复,这里优先使用原版的,不再载入FH的;
- **12和8的差异的原因**:原版和FH的sm文件存在重复,这里优先使用原版的,不再载入FH的;
- **17和18的类似的原因**:地图中含有FH-Patch中存在的物品时候,就会跳出;(也就是说地图加载的最后在加载含有的物件)
- 假设"载入地图即将完成时候跳出"的原因就是少定义:那么18,19就是缺少依赖部件的定义;17的原因是Berlin_TEST里本来就含FH定义的固定武器,
但是这部分却存在缺少定义,因此跳出;

# -------------------------------------------------------------------------------------
尝试为FH加上XWWII的烟火和音效;(加入FH_Steel_Cross后无效)

重新看看所需的增强元素,也就是:
- 手持武器:py程序已完成;
- 兵人模型:
- 载具武器:py程序已完成;
- 地图包:py程序已完成;

"game.addModPath Mods/XWWII/Patch_from_FH/"调整到最后也无法遏制其载入立陶宛地图失败;
看见XWWII本来定义的JohnsonLMG:查看是什么;是美军M1942约翰逊轻机枪;

完成XWWII2.7-Beta:还差:意大利和伪满洲国的UI; <Finished>

处理去重形式:"[('', '', 'Vehicle/Icon_panzer38.dds'), ('Ammo/Icon_cannon.tga', '', ''), ('', 'Ammo/Icon_bullet.tga', ''), ('', '', 'Vehicle/Icon_panzer38.tga'), ('Ammo/Icon_bullet.tga', '', '')]"

(WarFront链接补一个:https://www.moddb.com/mods/warfront1/downloads/warfront-35-full;)

在BERLIN_TEST测试用python程序移植的38t坦克:炮弹类型不对,缺少瞄准贴图;
修正py程序之后(考虑贴图可能有tga格式):瞄准贴图有了,但是炮弹类型仍然不对(更是少了发射烟雾);
按照III号坦克weapons.con修改后:正常;

使用载具武器-py程序导入Air/Sea武器各一个:
剑鱼战斗机后侧机枪烟火/子弹定义错误:修正projectileTemplate后无误;

py程序报告的"******* Not Defined *******: Air_Spotter"确实是WZ29所在地图无法载入的原因!
WZ29主炮开火类型不对;复制II号坦克的"ObjectTemplate.create Projectile 20mm_KwK_30_L55"的定义给
"ObjectTemplate.create Projectile wz29_35mm_Projectile"尝试:正常;

TO DO LIST:
移植2门早期火炮(来自盟军和轴心国军):Wz36,SA37;迫击炮;
SA37炮弹效果无:直接改成其他炮里定义的"75mm_KwK_37_L24_APCProjectile"后正常;
导入迫击炮载入BERLIN_TEST跳出:e_MuzzMortar的定义不对也会导致错误;
炮弹无效,改成"wz29_35mm_Projectile"尝试:无效;
控制打出去的炮火爆炸效果的部分在哪,仍然值得探究;

今日贴图修正:满洲军服装;WZ29涂装;修正Ehrhardt机枪声音;

--------------------------------------------------
### 模型编辑尝试
流程是:.mdl(Half-Life model) ---> .smd ---> .3ds(3dsmax model) ---> .sm(然后再用bfview看看);
失败:.3ds->.sm的这一步失败了;
尝试Blender的插件:安装Blender的插件还是到其C盘目录下手动安装靠谱;
在"C:\Users\luomi\AppData\Roaming\Blender Foundation\Blender\2.91\scripts\addons";
```
line 43 of standard_mesh.py:
return(f.write(struct.pack('f'*len(val), *val)))
struct.error:required argument is not a float
```

流程法可行:参见论坛的"Hooray!!! It works now!!! :D After renaming the object inside 3ds Max 2013 to "LOD01" ONLY, it works!!!"
同理在milkshape3d里重命名那个组即可转换,但是模型转成.sm后是旋转颠倒的;(在转换为3ds前的最后设置绕X旋转90即可摆正)

尝试将其导入bf1942的ichi-go地图:导入成功,但是属性不对,大小大概是正常建筑3倍大(scale 0.3很合适,最后再move到地面);Review一下:
```
LOD01    Highest detail visible model
LOD02
LOD03
...    Lowest detail visible model
COL01    Low detail collision model
COL02    High detail collision model
SHADOW    Real time shadow model
```
应该属性是COL01才对(碰撞类实体):BfMeshView打开后无,结果点Collision Mesh才出现,原来纯碰撞实体不可见;
解决思路:导入同样的俩3ds,分别命名为LOD01,COL01(再删掉下边那个贴图文件)再导出:游戏中碰撞效果有了,但枪弹打上去没反应;
注意bfmods的教程的如下说明:
> Material ID spinner: Sets the material ID value to use for the entire hitbox mesh. These values are used for different armor types and different effects. Only active if Force MatID is checked.
但是到底和MatID有关还是和COL的个数有关?我们做实验:
- 在Blender里读出China_Temple的MatID=45;而Carentan_m1的MatID=45;(似乎是Blender默认45)
- 为China_Temple再加一组COL02:仍然没有;
- 直接在Objects.con中声明:"ObjectTemplate.material 45":仍然无用;

找到了rfa命令行工具;
```
PS D:\BF1942\Rebuild_XWWII\XWWII_RES\objects> rfaPack.exe
-- RFA Pack 1.5 --
 Usage examples:
   ProgramName [sourceDir] [PackDirName] [Archive.rfa] [ -u update existing .rfa ]   RfaPack.exe d:/menu menu menu.rfa
   RfaPack.exe d:/menu menu menu.rfa -u

例如: $ RfaPack.exe D:/BF1942/Isolate-RFA/objects objects D:/BF1942/Mods/XWWII/XWWII2.7/Archives/objects.rfa -u
```

原来在Blender里选全Box/COL/LOD信息即可导出成功;另附常用材料ID:
```
Material 80= Solid Wood
Material 81= Wood
Material 82= Thin Wood
Material 83= Hollow Wood
Material 84= Solid Metal
Material 85= Metal
Material 86= Thin Metal
Material 87= Hollow Metal
Material 88= Solid Stone (Rock)
...
Material 0 = Default (used on wheels a lot) 最早没反应的那种;Material 1 = Water;Material 2 = Dry grass;Material 3 = Juicy grass;Material 4 = Dry dirt;Material 5 = Wet dirt;Material 6 = Mud;Material 7 = Reserved (Outside map);Material 8 = Gravel;Material 9 = Frozen ground;Material 10= Dry sand (El Alamein);Material 11= Wet sand;Material 12= Rock (Omaha beach);Material 13= Sand Road;Material 14= Dirt road;Material 15= Paved road
```

实体添加进地图的坐标语句:
```
Object.absolutePosition 1155.22/71.52/703.89  // 地图X正向/高度/地图Y
// 高度比房子高个1.3合适; 0.3大概是人物小腿长度;
在milkshape3d里,wwii_sandbags的宽度大概是4格;
```

milkshape3d 里绑定贴图:select group然后assign;

-----------------------------------------------------------------
### 地图制作
将现在XWWII的所有素材解压到移动硬盘以支持地图制作(使用ED42);

另外需修改的武器的声音:ppsh41/pps43/Ehrhardt机枪;
一些手持武器的Objects代码含义:
```
ObjectTemplate.roundOfFire 8 ======射速,上限1800
ObjectTemplate.addTemplate ======可以在武器上添加任何一个模型(加一艘大和都行)
ObjectTemplate.setPosition ======添加模型的坐标
```
贴吧内搜索:战地1942 修改武器威力 site:tieba.baidu.com
威力在Handweapons/Common/Weapons里修改子弹类型的伤害:
```
ObjectTemplate.create Projectile PPSh43Projectile
...
ObjectTemplate.invisible 1
ObjectTemplate.material 381
```
再根据381去game里找定义语句改:
```
rem *** PPSh41 ***
MaterialManager.material 381
...
MaterialManager.materialDamage 3
```

bfmods论坛提到了一种用于debug的bf1942_r.exe;
(在bf1942下的settings/VideoDefault下修改renderer.setFullScreen 0来调试实在是太好使了!!!)

XWWII现在所有单机地图无法载入,得卸载昨天加入的地图元素定义,看看是不是原因:仍然无法载入;
注释掉XWWII2.7这个模块载入XWWII2.6的地图:仍然无法载入;
去掉加入的地图元素的AI定义:没有影响;

**Notice!!!!**:RFA自动打包程序,如果原RFA文件里本来有的文件,打包后会依然在,最后删掉那个RFA再打包;

bf1942_r.exe要在iso加载在磁盘时才能使用!日志地址是"D:\BF1942\Mods\XWWII\Logs";

我删掉了BG42-Patch下Buildings的所有AI文件夹,然后之前不能载入的单机图和BG42移植图:均能载入;
我现在要debug一下珍珠港那张图为什么跳出;

用PS CS6做DDS:做成TGA+Alpha通道后,存储为DXT3|显式Alpha即可;

M&B中的模型转换为3ds时大小的变换倍数:似乎不需要改变;

先保存加了地图城墙之类的不跳出的rfa,再加入剑鱼、村门、删20mmAT、换菜单DDS;
stebarbwire_m1 antiaircraft Swordfish
反复实验后觉得是Swordfish造成的问题;
将SwordFish的AI全部引用修改为Mutsang之后:无报错快载入时跳出;
将第二架SwordFish开出去,绝不会跳出;(和打包工具也没有关系);

检查FH和XWWII的四号、虎式涂装是否一样:格式布局是一样的;
另外尝试在XWWII中引用XWWIIX的objects(加 GerOfficerCap):成功;
在中途岛修改日军兵种为XWWIIX的日军海军:除了大正十一年机枪动作有问题其余正常;
修正大正11年机枪动作:持枪还是朝天;(并制作机械瞄准) type11LMG

音效的替换:似乎加入44Hz的爆炸声,无声音;
尝试Type96LMG:没有出现,只有一把小刀;
加入GoldWave制作的44kHz的Garand枪声,即使setFullScreen 0也无报错载入地图跳出;

查看SwordFish的脚本搜索其材质不受损的原因:
```
ObjectTemplate.addArmorEffect XXX
```
套用Ki61的,没有出错但是也没修正;再套用原来的位置参数;还是没用;
又去参考: https://bfmods.com/mdt/Tutorials/index.html
以及: https://bfmods.com/mdt/scripting/Intro.html
那么参考: https://bfmods.com/mdt/scripting/ObjectTemplate/Properties/AddArmorEffect.html 谈到: 
>The AddArmorEffect property allows you to choose an effect when the objects drops below a certain number of hitpoints. The effect will stay on until it reaches the next armor effect.
将setVehicleType改成VTFighter后仅仅是用自己炸弹炸会掉HP;
我突然想起 Material是写入到.sm文件里的,可能和这个有关系;

BINK是命令行的用法:(一些更细致的参数调节选项也可以加上,输出 W=800,H=600 的bik视频);
```
./bink .\XWWII.avi XWWII.bik ?????
```
尝试压缩一下AVI背景视频再转BIK,是否播放无噪音:;

移植BG42的音频更加高效:同为44kHz,并且也是BFmod;
不要用多声Mono替换单声的;

关于游戏Coop设置(在 ServerAutoexec.con):
```
admin.setTicketRatio 1.00 // 兵力值调节
game.enableFreeCamera 1 // 自由查看
```
给Aden加Tiger-II:居然本来就有?已加入;

------------------------------------------------------------------
### 随机化同一张Map士兵穿着的研究

idea:参考FH里的随机枪械写法,看看能否将textureManager写入Kit的定义;
事实上应该参照脸部定义写法:"ObjectTemplate.setRandomGeometries ...";
请参考:https://bfmods.com/mdt/scripting/ObjectTemplate/Properties/SetRandomGeometries.html;
FH已经在 FMGermanSoldier 的定义里实现!只需要参考它的写法即可!!!(经过验证我确定它是work的)
事实上SetRandomGeometries不仅仅用在了Soldier的脸部随机化部分,也在bfmods上可见FH还把它用在了载具的部件随机化部分;
仔细思考,SetRandomGeometries 其实比贴图的随机化要好,因为它封装了贴图的随机化,还涵盖了形态的随机化;

----------------------------------------------------------------
### 自顶向下的map开发
事实上正确的思路是你想到了某个战役需要表达,那么随之而来的就是寻找合适的地图模板(因为省去了AI路径的编写)
接下来就是兵模、装备、载具、环境真实化(加入标志性的静态SimpleObject),最后再修改一些texture细节即可;
那么这就是模块化的开发思路,以地图为单位的封装开发,在这个过程中必然会去除2.7版本里的一些没有必要的劣质地图;
在这个过程中几个Patch文件夹的功能分工也逐渐确认:

- Patch_of_FH:载具以及手持武器的封装;
- XWWII2.7:兵种兵模/环境建筑等的定义,模型及其贴图;

引擎的优化在后期仍然是非常重要的,尤其是步战的"重量感",这在原版和很多mod里给人的感觉都是人体太轻了;
关于实体的绑定(比如加刺刀,思路是给刺刀绑定步枪(而不是给步枪加刺刀)):
```
ObjectTemplate.create AnimatedBundle SpringfieldBayonetComplex
ObjectTemplate.geometry Springfield // 模型的引用;
ObjectTemplate.hasDynamicShadow 1 // 动态模型;
ObjectTemplate.createSkeleton animations/No4Bayonet.ske // 动作绑定;
ObjectTemplate.addTemplate SpringBayonetObject // 加载刺刀;
rem ObjectTemplate.bindToSkeletonPart bayonet
ObjectTemplate.setPosition 0.0025/-0.015/0.08 // 加载位置;
```

然后再加装给主体模型SpringfieldBayonetLod:
```
ObjectTemplate.create LodObject SpringfieldBayonetLod
ObjectTemplate.lodselector HandWeaponLodSelector 
ObjectTemplate.addTemplate SpringfieldBayonetComplex
ObjectTemplate.addTemplate SpringfieldSimple
```

.inc文件的用途:a few script files having the suffix ".inc", as these files are included and shared by a number of .con files using the "include" keyword directive.(公有的script声明文件;),对Objects文件夹分工的介绍:

- Vehicles/    - All the cars, jeeps, tanks, planes, and boats.
- Common/    - a few very common items.
- Buildings/    - static building objects, with the decoration layout information.
- Effects/    - explosion, dust, water ripples, and other cosmetic effects.
- Handweapons/    - weapons that the player carries with them and keeps in their inventory
- Items/    - flag and kit (weapons per class) information.(Kit就是装备的意思;)
- MOVE_FILES/    - static scenery pieces, chairs, tables, pipes, logs, signs, etc...
- Soldiers/    - soldier properties, sounds, parts (hands, heads, body's)
- Stationary_weapons/    - mounted machine guns.
- Vegitation/    - trees and bushes. 

对每种.con语句的快速index: https://bfmods.com/mdt/scripting/AllProperties.html

这样的写法会出现奇怪的rfa错误(应该是"objects"而不能是"objects/",可能是文件夹识别问题):
"RfaPack.exe D:/BF1942/Isolate-RFA/objects/ objects D:/BF1942/Mods/XWWII/XWWII2.7/Archives/objects.rfa -u"

控制StationaryMG42机械瞄准视角的代码(还有设置"ObjectTemplate.setCrossHairType CHTNone"):
```
ObjectTemplate.addTemplate StationaryMG42Camera
ObjectTemplate.setPosition 0/0.239/-0.080
ObjectTemplate.setRotation 0/0/0
```

尝试在插入(无用):
```
ObjectTemplate.setFireCameraShakeAnimationState SmallExplosion
ObjectTemplate.setFireCameraShakeAnimationState BigExplosion
ObjectTemplate.setAnimationState BigExplosion
```
更全的MDT DOC: http://www.realtimerendering.com/erich/bf1942/mdt/MDTDOC/

用一个奇怪的思路实现了手雷爆炸的震颤(写在"e_ExplGranade"里,模仿营房火堆的伤害):
```
ObjectTemplate.addTemplate Shake_FireDamage
ObjectTemplate.timeToLive CRD_NONE/0.8/0/0
... ...
ObjectTemplate.create SupplyDepot Shake_FireDamage
ObjectTemplate.radius 100 // 效应半径;
ObjectTemplate.team 0
ObjectTemplate.workOnVehicles 0
ObjectTemplate.workOnSoldiers 1
ObjectTemplate.setHealth -1 -0.02 0 // 第二个就是伤害大小,0.02合适;
```

----------------------------------------------------
### Request-Processing 模式的改进
20210831-Request:德军船型帽;英伦空战德军随机化服装;

接下来可能会开发的战场/阵营(由于XWWII主要偏重的还是西欧的晚期战斗以及太平洋澳大利亚的战斗,因此需要加强的是二战早期战斗以及被遗忘的国家参加的战斗):
- 北欧:挪威 vs 德国;
- 北欧:瑞典/芬兰 vs 苏联;
- 东亚:伪蒙古国 vs 伪满洲国;
- 东亚:八路军 vs 日本(反扫荡);
- 西欧:德国 vs 比利时;
- 南欧:希腊 vs 意大利;
- 东欧:罗马尼亚 vs 苏联;
- 北非:自由法国 vs 德国;
- 东南亚:中国远征军 vs 日本(反攻缅甸);
- 珍珠港:日本海军 vs 美国海军;

不断做减法:删掉受BG42支持的所有地图,专心完成自己的一系列地图;

### 载具导入问题解决
- BA-64:材质没有反应;枪弹没有效果;没有载具icon; (通过在Blender中修改BA-64_Hull_m1.sm的材质 ID=45 解决;)
- BT7:材质没有反应;枪弹没有效果;没有载具icon;外加:1.e_MuzzPanzSml;2.Coaxial_DT; (通过在Blender中修改BT7_Hull_L1.sm的材质ID=50解决;)
- M3Stuart:材质没有反应;枪弹没有效果;没有载具icon;外加:1.Hull_bren;2.Coaxial_besa; (类似上述方法解决;)
- sFH18:材质没有反应;枪弹没有效果;没有载具icon; (类似上述方法解决;)
- SdKfz222:材质没有反应;枪弹没有效果;没有载具icon; (类似上述方法解决;)
- SU76:材质没有反应;枪弹没有效果;没有载具icon;外加:1.e_MuzzPanzSml; (类似上述方法解决;)
- SU122:侧面材质没有反应(前后有);枪弹没有效果;没有载具icon; (类似上述方法解决;)
- Zis3:材质没有反应;枪弹效果类似子弹;没有载具icon;外加:1.e_MuzzPanzSml; (类似上述方法解决;)
- OpelBlitz:材质没有反应;枪弹没有效果;没有载具icon; (类似上述方法解决;)
- Horch:没有载具icon; (类似上述方法解决;)
- Ferdinand:枪弹没有效果;没有载具icon; (类似上述方法解决;)
- M3GMC:材质没有反应;枪弹没有效果;没有载具icon; (类似上述方法解决;)
- CoastalGun:材质没有反应;枪弹没有效果;没有载具icon; (类似上述方法解决;)

(还都有个冒紫烟的问题;)
下一步移植的目标是法国和意大利载具,飞机;

玩coop时候用的是conquest模式的ObjectsTemplate;

在Blender里修改SwordFish的材质=60:有效了;

### 地图制作: 意大利进攻法国(1940):Mentone
意军部队还在cote dAzur一带作战(法国南部的海岸地区).在这里,意军的进展也不大,他们的目标是在法国人投降之前占领尼斯城.
但直到停战前,意军也只占领了芒通镇2/3的地区,距离边境仅8公里.

法国军队武器:
- FN1922 手枪:机瞄;枪声;
- Mas36 步枪:换弹动作;
- Mas38 冲锋枪:机瞄;换弹动作;

意大利军队武器:
- BerettaM1934 手枪:
- Beretta 冲锋枪:枪声;机瞄;

步枪复制直接复制Carcano并替换字段Carcano即可;
只需改的地方:AnimationStatesShoot.con,1pAnimationsTweakingMod.con,singleShotWeaponsMod.inc;

### 地图背景音效
套用XWW2奥马哈海滩Enviroment.con及其Enviroment.ssc的写法即可(.wav可以就存在本地);
```
load @ROOT/bf1942/levels/XWW2_Mentone/sounds/44kHz/dodambience6.wav
```

### 二战比利时军队装备(https://www.junpin360.com/html/2015-04-06/4068.html)
步兵武器:Mauser1889;FN1922手枪;Maxim1908;47mm反坦克炮;
装甲兵:T-13型坦克;
空军武器:


### 尝试导入自己外部制作的帽子:苏军冬季帽/日军防毒面具;
1.导入类似的BF1942的.sm文件到Blender;
2.导入外部塑形完毕的.obj文件到Blender;
3.在Blender内对.obj缩小(100倍)到.sm文件大小,重叠;
4.删去原.sm,删去.obj放缩前的模型,导出为新的.sm;
5.进入游戏查看,再用如下语句调节:
```
GeometryTemplate.scale 1.0/1.0/1.0 // Geometries.con内(脑袋的 上下/前后/左右)
ObjectTemplate.setPosition 0.13/-0.13/-0.5  // 正看他的脸 往下/往后/左移(写在有"ObjectTemplate.addTemplate XXX"的Objects.con内的后一句)
ObjectTemplate.setPosition 0/-0.2/0 // 背包:前后/左右/上下
```

而setPosition唯一可行的写法:
```
ObjectTemplate.create simpleObject jpa_mask_helmet_Obj
ObjectTemplate.geometry jpa_mask_helmet
ObjectTemplate.setHasCollisionPhysics 1
rem --------------------------------------
ObjectTemplate.create KitPart jpa_mask_helmet
ObjectTemplate.addTemplate jpa_mask_helmet_Obj
ObjectTemplate.setPosition 0/0.0/-0.5
ObjectTemplate.setBoneName A
ObjectTemplate.setCopyLinksCount 0
```
(2021/09/06)找到了FH的写法:
```
ObjectTemplate.create KitPart polish_Officer_cap
ObjectTemplate.geometry 
ObjectTemplate.setBoneName A
ObjectTemplate.setCopyLinksCount 0
ObjectTemplate.addTemplate polish_Officer_capHolder
ObjectTemplate.setPosition -0.035/0/-0.015

ObjectTemplate.create SimpleObject polish_Officer_capHolder
ObjectTemplate.geometry polish_Officer_cap
```

### 尝试给FH加上XWWII的枪械特效;
失败...

给苏联和德国早期地图加上Neringa的载具试错:Zis3的炮弹无伤害(仅仅对己方坦克);
"ObjectTemplate.projectilePosition 0/-0.1/3.5"不准确会被沙袋挡住;

### 比利时/丹麦/荷兰(西欧三国) - 希腊/匈牙利/罗马利亚(东欧三国) - 挪威/瑞典/芬兰(北欧三国) - 印度/新西兰/尼泊尔(英联邦三国) - 满/蒙/蒙(东亚三伪)
关于T13坦克的参考:https://m.sohu.com/a/119608383_550331;
今日任务,尝试从一辆坦克开始为基础,制作T13:
- 选择:Chi-Ha中型坦克;
- 修改:调高/缩短底座,去除机枪,炮塔变形;

基于已有载具修改时,主要自顶向下的组件命名更替(否则会默认引用已有的定义指定的组件);
修改贴图信息时候,如下.rs内代码部分不能修改:
```
subshader "Chi-Ha_Hull_m1_Material1" "StandardMesh/Default"
```

- 在Blender中:进入Modeling->点选择模式(左上角),和Milkshape3d类似;
正对着坦克方向:
```
ObjectTemplate.setPosition -0.236/1.223/0.294  // 向右移动炮塔/上(正)下/..
```
武器展示图顶部字体:Cooper Black;

关于在 Blender 中全流程化建模的设置:
- 我需要设定和Milkshape3d类似的4视图; (Blender切换四视图和透视视图的快捷键是"Ctrl + Alt + Q")
- 点选择模式是透视的,和Milkshape3d类似; (似乎没有,但是可以摁住shift来多选)
- 模型边线上添加点; (选择模型的一条边线,按W键,选择"细分",然后切换到"点选择工具",然后我们就可以编辑这个新添加的点)

### 制作"西欧:德国 vs 比利时"的地图:XWW2_Hannut 战役;
构建地图,旗帜修改完成:加入元素:;
若有Blender导出sm出错,尝试加上Bounding_Box并选Lod;
MB:Warband的模型需要在Blender里先0.05缩放;然后再"GeometryTemplate.scale 0.2/0.2/0.2"缩放;
(抑或是在Blender直接0.01缩放;且加上定义贴图 texture "texture/trench_wood01_t";)
组合模型的方式:
```
ObjectTemplate.create SimpleObject mb_block_house_out_m1
ObjectTemplate.geometry mb_block_house_out_m1
ObjectTemplate.setHasCollisionPhysics 1

ObjectTemplate.create Bundle mb_block_house
ObjectTemplate.geometry mb_block_house_in_m1
ObjectTemplate.setHasCollisionPhysics 1
ObjectTemplate.setHasResponsePhysics 1
ObjectTemplate.addTemplate mb_block_house_out_m1
```

引用地图rfa外载入图:"game.setLoadPicture ../../texture/load_img/XWW2_Hannut.tga"

不同地图的服装随机性和地图空间/人数的关系:没有关系,随机身体只能设置赋予一个阵营;

### 重新规划阵营/地图分配(Inspired by Moddb网友);
2.8版本还应该开发的地图(开发国内战场之前):
- 多布鲁克:南非/印度/新西兰 vs 意大利;(1942) (地图特点:原版战斧行动;) <FINISHED> 
- 卡累利阿地峡:芬兰/瑞典 vs 苏联;(1944) (地图特点:欧洲丛林;) <FINISHED>
- 入侵爪哇岛:荷兰 vs 日本;(1942) (地图特点:太平洋城市;) <FINISHED>
- 卡尔可夫:匈牙利/罗马利亚/保加利亚 vs 苏联;(1943) (地图特点:原版卡尔可夫;) Hungary/Romania/Bulgaria
- 入侵丹麦:丹麦 vs 德国;(1940) (地图特点:港口(Poure_Lemo);)  Denmark
- 入侵奥斯陆:挪威 vs 德国(伞兵);(1940) (地图特点:空降;) Norway
- 什切青:波兰 vs 德国;(1939) (地图特点:边境小镇;) Poland
- 贝尔格莱德:南斯拉夫 vs 德国;(1944) (地图特点:游击队/步战;) Yugoslavia

阵营武器:(RF:步枪/LMG:机枪/MP:冲锋枪/SG:手枪/GN:手雷/TANK:坦克/LP:装甲车/LV:侦察车/AT:火炮)
- 南非/印度/新西兰: (RF:NO4/LMG:Bren/MP:Thompson/SG:Webly/GN:Mills/TANK:Matilda_II/LP:M3GMC/LV:Lynx/AT:AT25)
- 芬兰/瑞典: (RF:Mosin-Nagant/LMG:Lahti-Saloranta-M26/MP:Suomi/SG:Webly/GN:GrenadeAxis/TANK:BT-42/LP:T-50/LV:CivTrck/AT:AT25)
- 荷兰: (RF:Geweer-M.95/LMG:Madsen/MP:MP28/SG:FN1922/GN:Mills/TANK:NONE/LP:L-181/LV:CivCpeRust/AT:SA37)
- 挪威: (RF:Krag–Jørgensen/LMG:Madsen/MP:NONE/SG:Colt/GN:Mills/TANK:L-120/LP:Ehrhardt/LV:CivTrck/AT:AT25)
- 丹麦: (RF:Krag–Jørgensen/LMG:Madsen/MP:NONE/SG:Webly/GN:Mills/TANK:Pan39/LP:BMW_DAN/LV:bicycle_albelt/AT:SA37)
- 波兰: (RF:WZ1929/LMG:WZ28/MP:Mors/SG:Webly/GN:Mills/TANK:7TP/LP:Ursus/LV:Horse/AT:Wz36)
- 匈牙利/罗马利亚/保加利亚: (RF:Mannlicher/LMG:ZB26/MP:Danuvia/SG:TT33/GN:Vecsey/AIR:Dew520/LP:TACAM-R1/LV:Horse/AT:Wz36)
- 南斯拉夫: (RF:NO4/LMG:Bereda/MP:MP40-STEN/SG:Webly/GN:AxisGrenade/TANK:NONE/LP:AS37/LV:Frz_Bus/AT:Kuk75er)

新建阵营时:注意不同原模板的模型.sm/骨骼.ske不相容;
若dds加载不上(灰色),尝试开一个已有的dds然后复制粘贴给它再保存后赋给模型;

给indian士兵加载背头盔:仿照背包的写法;

- PS中羽化边缘的方法:选取选区->右键羽化:设定值->反向选取->del即可;

有时候ED42添加的武器重生只在Conquest的脚本里记录,可以拷贝至单人模式;

(12月6日在芬兰独立日这一天,英国正式向芬兰宣战;)

- 地图调换阵营:
在ControlPointTemplates.con中改/在Init.con中改"game.assaultTeam 1";

- 改音频:声音长度一样是关键;(用同样思路解决了granadeX.wav偶尔无声音,将1/3的0.4s长改成了0.3s即可;)

- 精简模型:Blender修改器属性 --> 精简 --> 比率设置为0.2~0.3(回车);
- 合并模型:如果想合并这两个物体为一个物体,可以按住“shift”选中这两个物体,然后“ctrl+j”进行合并.
- 点全选:Alt+Z开半透明模式;

### XWW2_Kendari(查询wwii Dutch insignia)
Dchmun_rX.dds中上/下分别是:领章/肩章;
- Known Bugs:XWW2_Kendari征服模式会因为"ai.con"跳出;

### AWWII_TEST
构建一张Test Map;可以放置各种大/中/小实体,载具等等;

后五张地图需要做的工作Queue(分类工作法,当前进度条:"==>"):
- 军队定义:DenmarkSoldier;NorwaySoldier;YugoSoldier;PolandSoldier;HRBSoldier;DenKit;NorKit;HRBKit;PolKit;YugoKit; <Finished>
- 武器制作:Krag–Jørgensen;WZ1929;WZ28;Danuvia;Mannlicher;Vecsey; <Finished>
- 载具制作:L-120;Pan39;BMW_DAN;Dew520;TACAM-R1; <Finished>
- 军帽/服装制作:den_helmet;den_cap;den_officer_cap;nor_helmet;nor_cap;nor_officer_cap;ro_officer_cap;hun_cap;bu_helmet;
pol_helmet;pol_officer_cap;civ_cap;ammo_pack;HRB_uniforms;DEN_uniforms;NOR_uniforms;POL_uniforms;YUGO_uniforms; <Finished>
- 地图模型制作:XWW2_Aalborg;XWW2_Kharkov;XWW2_Danzig;XWW2_Fornebu;XWW2_Bihachi; <Finished>
- 旗帜载具贴图/语音真实化定义:HRB_sec;DEN_sec;NOR_sec;POL_sec;YUGO_sec;
- 地图制作:XWW2_Fornebu;XWW2_Aalborg;XWW2_Kharkov; ==> XWW2_Danzig;XWW2_Bihachi;

事实上应该让DenmarkSoldier,NorwaySoldier,YugoSoldier,PolandSoldier,HRBSoldier都定义在DutchSoldier上并重载DutchSoldier的贴图;
Krag–Jørgensen和WZ1929,Mannlicher只重载贴图;

- Danuvia绑定任意原版骨骼,弹夹在上部的问题:通过位移其mag.sm文件中的实体(向下)解决;

- 载具中添加座位的语句(Ha-Go_Browning_PCO1 的定义可以参考其他载具):
```
ObjectTemplate.addTemplate Ha-Go_Browning_PCO1
ObjectTemplate.setPosition -0.237/0.45/1.341
```
注意,注掉"PCO"注意注掉后面对应的"setPosition",否则会干扰!
轮胎的位置在Physics.con中修改,"0.5"大概是一个论坛的距离;
控制视角高度:
```
ObjectTemplate.addTemplate Pan39Camera
ObjectTemplate.setPosition 0.259/1.90/0.4 ../高/前
```
精简模型再导出.sm无效,但是先导出为.obj再导入,再以此导出.sm即可;
(精简模型会破坏贴图规则)

- 德国伞兵的定义; <Finished>
- 确定XWW2_Fornebu引用的地图; <Finished>

### 关于如何构造可移动的火炮
参考 XWW2 的 french75;是在Objects.con中的:
```
ObjectTemplate.hasMobilePhysics 1
...
ObjectTemplate.addTemplate SA37Entry
ObjectTemplate.setPosition 0/0.0/1.2
ObjectTemplate.addTemplate Artillery_Engine
...
```
出现了反复的颠簸动作并且无法移动;
在去除"ObjectTemplate.hasMobilePhysics 1"后不再颠簸(但无移动效果);
关键是这种震动是否是几何物理性地,即由于重心和碰撞的原因导致的;
只留下"ObjectTemplate.hasMobilePhysics 1"注释掉添加Engine的语句:仍然颤动;

### Soldier的定义
次序是非常重要的,总结地说:
"addTemplate在前,creat在后;头/身/手的顺序定义;否则会缺胳膊少腿;"

- 令迫击炮弹生效的命令定义:
```
ObjectTemplate.material 237
ObjectTemplate.material2 206
ObjectTemplate.radius 30
```

- 解决贴图问题的方法仍然是找合适大小的"已有效贴图"粘贴无效贴图上去(模型会按比例去找贴图部分);
- 导出MB模型可以用合并导出,此时同样材质的部分会自动合一,那么顺序也会改变(但全局顺序仍和OpenBRF里一致),但是可以先贴图再Tool打开查看修改;

### 涞源(XWW2_Laiyuan 1939/10/25)
一九三九年十月,鉴于华北北部共产党武装已严重地威胁到日军的占领,日军华北方面军决定开始第三期“治安肃正”作战;
阿部规秀率领他的部队自张家口南下,二十五日赶到河北西部的涞源,与驻扎在涞源县城的堤鸠大队会合.然后,日军兵分三路从涞源、满城、唐县和定县出发,
开始了寻找和扫荡八路军主力的作战行动.

### 尚未引入,将在2021/11/10后引入的国家
在这之前,还需补充:伪满洲国/伪蒙古国;
地图:中国远征军/血洗纳粹冲锋队/日本226事变;
尚未补充的:
- 同盟国:希腊/东北军/西北军;
- 轴心国:斯洛伐克/克罗地亚/维希法国/土耳其(师);

- 修正CivTrck,CivCpeRust的不可击毁问题;

- 枪体加弹夹时候的位置控制语句:
```
ObjectTemplate.setPosition 0/0.1/0.2 //左(-)右/上(+)下/前(+)后
```

### 坦克/装甲车添加附着物
可以看到苏联坦克后面或者侧面绑木头,美军坦克的前方放沙袋,德军坦克的裙板等等...;
控制语句:
```
0.0/0.84/0.41  // //左(-)右/上(+)下/前(+)后;
```

- Blender中"封面":假设有一个由边集S构成的空洞,那么选择这几个边后,按F即可完成封面;

添加乘员位置(搭便车的步兵):
```
rem *** XXX_Passenger_PCO1 ***
ObjectTemplate.create PlayerControlObject XXX_Passenger_PCO1
ObjectTemplate.NameTagOffset -1/-1/0
ObjectTemplate.setNetworkableInfo XXX_BodyInfo
ObjectTemplate.aiTemplate StuGIIIEPassenger1
ObjectTemplate.setPcoId XXX
rem -------------------------------------
ObjectTemplate.addTemplate StuGIIIEPassengerSeat
ObjectTemplate.addTemplate StuGIIIEPassengerCamera
ObjectTemplate.addTemplate StuGIIIEEntry
ObjectTemplate.setPosition -0.7/0/-2.6
rem -------------------------------------
ObjectTemplate.GUIIndex 21
ObjectTemplate.setVehicleIcon "Vehicle/Icon_XXX.tga"
ObjectTemplate.setVehicleIconPos 51/53
ObjectTemplate.setSoldierExitLocation -0.5/0/0 -0.5/0/0
ObjectTemplate.setVehicleCategory VCLand
ObjectTemplate.setVehicleType VTArtillery
ObjectTemplate.setToolTipType TTArtillery
ObjectTemplate.hasRestrictedExit 1
```
再在"ObjectTemplate.addTemplate XXX_Turret"后面添加:
```
ObjectTemplate.addTemplate XXX_Passenger_PCO1
ObjectTemplate.setPosition -0.7/1.5/-2.6
ObjectTemplate.setRotation 180/0/0
```
注意"ObjectTemplate.setNetworkableInfo"一定要准确否则会跳出!


### 真实感强化元素
- 加入坦克上的旗子; <Finished>
- 加入大衣; <Finished>
大衣是战争中普遍存在的,考虑将其作为Pack类型的KitPart加入;
- 能移动的大炮; <Finished>
思路:不加Engine,而是直接复制75mm炮然后改Gunbase:
1. 复制一份french75然后删的只剩下objects.con;
2. 删掉一系列的无用的定义;
3. 在Complex处改"ObjectTemplate.geometry SA37_Shield",并且注意添加的Gunbase的位置;
4. 改对应的Camera,未涵盖在Gunbase里的注意是不是在Complex定义里,否则会使用跳出;
- 地图元素: <Finished>
1. 港口的民用船只;
2. 东线的东正教城堡;
3. 村庄模型;
- 加入Owen式冲锋枪; <Finished>

- 添加衣服的写法(正看人物)(至少将Rotation调对,否则很困难):
另外注意区分 backpack/HipPack;
```
ObjectTemplate.addTemplate mb_french_coat_m1
ObjectTemplate.setRotation 90/0/0  // 竖轴/横轴/来轴
ObjectTemplate.setPosition 1.0/0.5/-2 // 左右(+)/前(+)后/上下(-)
```

### 跑步持枪动作的更新
我们用FX里FG42对应的1P/3P的.baf来替换XWWII里的M1Carbine对应的Run/Walk动作:可行,只是对应动作时候枪的位置有些错位;
并且我发现:
```
AnimationStateMachine.copyState Mauser1889 v_arg1 No4 1.0 K98 1.0 // 意思是Mauser1889第一人称动作仿K98,第3人称动作仿No4;
```
冲锋枪/步枪套用FG42动作时是否存在不同:是的;

- 奔跑时手榴弹是拿手上,可否套用给机枪?:不行,甩动幅度太大,但是似乎可以套用给手枪;

### 接下来的地图

- 226兵变:1936年2月26日发生于日本东京的一次失败兵变;二二六事件推动了日本法西斯主义的蔓延,也彻底使日本走向了二战;日本的政治家都认为二二六事件标志着日本法西斯主义运动第二阶段成熟期结束;

- 部分mb建筑导出的问题:
obj时有部分面缺失;先转stl,再转obj,在blender内正常,但是转sm仍然缺失面;

剩余的工作:叛军军服修改(Kit)/Ha-go纹理修改;
修改太平洋美军脸部为<<重返狼穴2>>的;
春田的第一人称跑步动作;(第一人称的No.4);

- 当前需要做的地图:自由法国参加的解放战争:XWW2_Alsace;

- 头部.sm的Blender导入之后再导出存在问题:缺失面;

Puma的炮弹(因为误将 75mmProj 改成了 75mm_Field_gun 居然真的打出来一门炮);Wake岛美军炮(增大 SA37 的 fireingForce);
枪战斗狠地图:工厂战;

## XWW2_Ihantala
- 地图可见度/雾浓度调节:没有找到合适的语句;

## XWW2_Barbarossa
Operation Barbarossa:Biawestock,July 12,1941

- 控制地图地面纹理材质的语句在Terrian.con内:指向地图目录的的Textures文件夹;

- 解决Pr2018音频失效:https://www.jb51.net/softjc/733332.html;

- 地图纹理吻合,但是低清的原因:
原来由"bf1942\levels\XWW2_Zitadelle\Textures\Detail.dds"控制,事实上所有的Tx00i.dds都只是着色,
近处加载的都是Detail.dds;那么是否可以自制一个很高分辨率的Detail.dds,然后提高细节?

- 修正Panzer-III和Stug-IIIE在东线的涂装; <Finished>
- 修正比利时军队炮镜; <Finished>
- 修正XWW2_Barbarossa诸多建筑高度; <Finished>

猜想:ED42中改地形只能默认刷子大小改;


## XWW2_Seelow_Heights 人民冲锋队(Volkssturm)出场
人民冲锋队只需要重载 FMGermanSoldier,然后定义一个Kit即可:GVolKit ---- GVOL_i;

## XWW2_Saipan 太平洋植被增强

- 制作植被的方法:COL去掉;设置贴图Alpha通道;最后用几个平面拼接即可;

- ps根据颜色建立选取:菜单栏上方,点击“选择”,然后点击“色彩范围”...

加装伪装植被的日军(Camouflage):Hippack;

## XWW2_Bougainville
相当密集的植被覆盖

## XWW2_New_Britain
河谷战斗:排序index会决定kit的dds是否能显示出来;
- 构造大面积植被模型:首先必须查看blender中如何复制模型(反复导入是个可行的方法);dod_big_grass;
- 用dd2的日军死亡语音替换bf1942的:用GoldWave再转存的,才能在游戏里生效;

## 特效
- 蚊子:midgecloud;
- 海鸥:seagull1;
但是声音的定义没有找到(grep -i "error" 忽略大小写区分):
只能注销掉"ObjectTemplate.addTemplate midgesound1",看有没有声音;
(我在中途岛地图下找到了,还是11kHz的!) jungle_tree10_m1 buildingsmokeidledark

- 构造新的飞行鸟类:猫头鹰(hooted_owl1),以海鸥.con为模板;

## XWW2_Arden_Mountains
Yellow Plan;Arden Mountains,May 14,1940:XWWII-FB 11/10发布前的最后一张地图;

## bf1942地图的 static_object 的"场效应"
当一个kit_XX出现在一个被放大的static_object处时,它也会被按那个比例放大;

- b1bis坦克的主炮声音/同轴机枪子弹类型存在问题;

## 地图 XWW2_Zitadelle 的跳出(选兵种前):
当设置时:
```
game.setTeamSkin 1 GermanSoldier
game.setKit 1 0 MSS_0
game.setKit 1 1 ESS_1
game.setKit 1 2 MSS_2SP
game.setKit 1 3 MSS_3SP
game.setKit 1 4 ESS_4SP
```
(或者SP更少时,但是仅有一个非SP时不会有异常;)
事实上 Kit具备的ID声明在(NCO是对应1):
```
ObjectTemplate.setKitIcon 1 "Kits/Ger-SS-E_NCO.tga"
ObjectTemplate.setKitName 1 "NCO"
ObjectTemplate.setKitActiveName 1 "Active NCOs"
```

## horse_cart 贴图无效问题
确认并非dds的问题;不合并horse和cart单独导出的话,是贴图无误的;
但是在Blender中Ctrl+J合并导出 它就贴图无效
看来只能想办法在Geometries.con里组合;(组合成功 但是cart部分的Col属性无效)

---------------------------------------------------------------------
# 分地图测试阶段:
- XWW2_Aachen: 党卫军的帽子多样化(蒙布的帽子);(ger_ss_helmet;GerOfficerCap) <FINISHED>
- 载具Logo; 高清Menu的合并; M3Stuart的瞄准; <FINISHED>
- XWW2_Arden_Mountains:载入图;加一些花;(mb_euro_flower)德军早期装甲兵帽;(ger_ss_panzer_cap;PanzerNCO) <FINISHED>
- XWW2_Bloody_Ridge:里面的Grass可以利用一下(elephant_grass1); <FINISHED>
- XWW2_Bocage:Officer应该戴officer_cap;士兵戴蒙布的帽子; <FINISHED>
- XWW2_Caen: "XWW2 Coming Soon to BF2"的横幅替换; <FINISHED>
- XWW2_Coral_Sea: 改成海军Kits图; <FINISHED>
- XWW2_Coventry: 飞行员改成有降落伞的;载入图; <HANG-UP> 
- XWW2_Danzig: NCO修为德军早期装甲兵帽拿MP38的; <FINISHED>
- XWW2_Der_Untergang: 更换载入图; <FINISHED>
- XWW2_Dog_Green_Sector: 旅馆更换为Trench; <FINISHED>
- XWW2_El_Alamein: 增加德军非洲防晒帽(ger_africa_cap;ger_africa_glass); <FINISHED>
- XWW2_Fornebu: 挪威海报的修正(再增加一些);LS120瞄具替换;  <FINISHED>
- XWW2_Hannut: T13坦克坦克驾驶位机枪子弹logo去除(其换瞄准镜的方法?); <FINISHED>
- XWW2_Hochwald_Forest: 是否改成加拿大车辆涂装; <FINISHED>
- XWW2_Juno_Nan_Green_Sector: MG42/MG34准星收缩速度;MP40子弹类型强化; <FINISHED>
- XWW2_Kamenets_Podolskiy: T34/76的旗帜去除;使其仅仅出现在XWW2_Kharkov; <FINISHED>
- XWW2_Kharkov: T34/76的旗帜仅仅出现在XWW2_Kharkov; <FINISHED>
- XWW2_Laiyuan: 号角的替换(jinfly_weapons.brf中)(vuvuzela); 
- XWW2_Nomonhan: 蒙军军官帽/布尼琼帽/满军军帽适当往后; <FINISHED>
- XWW2_Salamaua: 更换日军装甲运兵车; <FINISHED>
- XWW2_Songhu_Campaign: 国军Madsen换为ZB26;汉阳造的枪声更换; <FINISHED>
- XWW2_Stalingrad: 苏军PPSH41/43弹鼓数量=8;去掉挡住他们行动的那个废墟; <FINISHED>
- XWW2_Tinian: 添加XWW2_Midway的飞蚊在河道处植被位置(midgecloud); <FINISHED>
- XWW2_Tokyo226: 地面细节更换为城市类型;Type38的瞄准加上标尺; <FINISHED>
- XWW2_Wake: 枪械击中烟雾的维持时长+; <FINISHED>
- XWW2_Zitadelle: 仍然存在跳出(人数少时不会跳出/但是我确定每个兵种都有覆盖); <FINISHED>


- PS如何选择建立不透明区域选区:
m1:按住CTRL+鼠标左键,点击图层缩略图;
m2:右键缩略图,点击选择像素;


### 套用另一个载具的瞄具:
比如要套用"M3StuartCockpitInternal"即可:
```
ObjectTemplate.addTemplate M3StuartCockpitInternal
ObjectTemplate.setPosition 0.94/0.08/0.2259
```
控制语句:
```
0.0/0.84/0.41  // //左(-)右/上(+)下/前(+)后;
```

- HeightMap.raw 的存储要在修改Height下save才会更新;

### 特效程度的时间序列控制

下列代码的含义:time=0,程度0;time=15,程度0.2;...time=100,程度1;
```
ObjectTemplate.sizeOverTime 0/0|15/0.2|45/0.5|75/0.8|100/1
```

---------------------------------------------------------------------
## 最终测试阶段问题队列:

- No5的带标尺瞄准:Iron_No5; <FINISHED>
- XWW2_New_Britain 的物件悬空问题; <FINISHED>
- 人物集中烟雾的改进: 利用已有烟雾; <FINISHED>
- 增大所有子弹击中效果Lod距离; <HANG-UP>
- 所有装备手榴弹的工兵,装备遥控炸弹,反坦克地雷,工兵修理钳;  <FINISHED>
- 减小手雷震颤距离和伤害; <FINISHED>
- Danuvia 的机械瞄准(Iron_Danuvia),Vecsey 的对应icon(Icon_vecsey); <FINISHED>
- 遥控炸药包的模型更新(),以及对应的icon(); <HANG-UP>
- 一些离谱的Kit_XXX替换:比利时工程兵; <PROCESSING>
- 喷火兵背罐制作(flame_thrower_pack),喷火器杀伤力上调(setHealth ...); <FINISHED>
- 硫磺岛的黑沙,修改(XWW2_Iwo_Jima); <FINISHED>
- 南部手枪,100式冲锋枪的机械瞄准(Iron_Nambu,Iron_Type100); <FINISHED>
- Mauser1889的机械瞄准(Iron_Mauser1889);  

----------------------------------------------------------------------
### 将已做好的 Iron_Sight 近视模糊化的方法:
到Alpha通道 选中(Crtl+单击)轮廓 ---> 滤镜库-模糊-光圈模糊 ---> 调整光圈和四个小点;

### 调整固定机枪的视角:
```
ObjectTemplate.setCrossHairType CHTNone
... ...
ObjectTemplate.addTemplate StationaryVickersCamera
ObjectTemplate.setPosition 0/0.1/-0.3 ../+高/-后
```
地图固定物体的放置:
```
Object.absolutePosition 419.181/65.1194/613.372 .../上下/前后
```

### unpack 语句
```
rfaunpack.exe  D:/BF1942/Mods/XWWII/Patch_from_XWWIIX/Archives/objects.rfa D:\BF1942\Rebuild_XWWII\Enhanced_XWWII_________RES/
rfaunpack.exe  D:/BF1942/Mods/XWWII/Patch_from_XWWIIX/Archives/texture.rfa D:\BF1942\Rebuild_XWWII\Enhanced_XWWII_________RES/
rfaunpack.exe  D:/BF1942/Mods/XWWII/Patch_from_XWWIIX/Archives/standardmesh.rfa D:\BF1942\Rebuild_XWWII\Enhanced_XWWII_________RES/
rfaunpack.exe  D:/BF1942/Mods/XWWII/Patch_from_XWWIIX/Archives/menu.rfa D:\BF1942\Rebuild_XWWII\Enhanced_XWWII_________RES/
```

### 接下来最希望新增的地图/阵营/元素;
- 元素:
    i)战马改造计划:加枪;
    ii)带动作的动物等;(参考 soccer mod 里的 willy);
    iii)火车轨道大炮;

免费模型下载:
http://www.modxz.com/show-274-6267-1.html;
https://free3d.com/zh/3d-models/;
https://en.eagle.cool/blog/post/best-websites-to-download-free-3d-model-with-high-quality;

### 带动作的动物 (Animal_Tiger)
本质是带初速度的 PlayerControlObject:并且修改其 Engine:"ObjectTemplate.setEngineType c_ETRocket";
并且通过"ObjectTemplate.setNoPropellerEffectAtSpeed 2"控制速度;
关于动作问题:调整对应 RotationalBundle 下的 "setContinousRotationSpeed";
而周期性的运动则是依靠嵌套地定义 RotationalBundle (每一层是反向的速度) 来实现的(非常巧妙);
Animal 的 Matrial ID:45;

怎样使得它不被Bot使用:"ObjectTemplate.aiTemplate NoOne";

贴图后模型预览白色的问题:是图dds的问题,那么只需要合并另一张有效的dds即可;

Blender文档:https://docs.blender.org/manual/zh-hans/dev/modeling/modifiers/generate/decimate.html

- 精简模型不生效:再次导入未被精简的.sm文件再精简导出(无效,即使关闭Blender);
可否精简后转成.obj再转.sm?(可以,并且贴图有效)

- 调整动物死尸位置:Dead_Animal_Tiger/DeadhorseWhite/Deadhorse;


## 模板计划(将可重复的模式抽象出来)

- 构造以下模板:阵营人物/武器模板(步枪/冲锋枪/固定机枪)/载具(装甲车/坦克/自行火炮/卡车/吉普/固定大炮/动物)/地图建筑;

### 先做3个新地图玩玩助助兴

- 圣康坦之路(XWW2_Saint_Quentin 1940):(德国国防军 VS 法国)新增元素:欧式建筑物*3(mb_euro_french_building_1,mb_euro_french_building_2,mb_euro_french_building_3)/战壕(mb_wwii_trench_curve,mb_wwii_trench_shelter);
- 科科达小径(XWW2_Kokoda_Trail 1942):(澳大利亚 VS 日本)新增元素:植被/毛驴(animal_donkey(Donkeybody,DonkeyLegs,Dead_Animal_Donkey),AnimalDonkeyEngine)/太平洋建筑*2;
- 关岛(XWW2_Guam 1941):(美国陆军 VS 日本)新增元素:植被/海鸥(seagull1)/太平洋建筑*2(dod_pacific_shed,dod_pacific_hut);


机瞄(BF5):https://www.bilibili.com/video/BV1ut411y7t7/?spm_id_from=333.788.recommend_more_video.-1

- 修改法国/意大利士兵脸部(Frz_Face1,Frz_Face2,Frz_Face3/FrFace01,FrFace02,FrFace03);不可随意更换头部,必须和 .skn 身子一起换(3个随机脸加1个Head,只须改 Geometries.con);

- 旗帜贴图:GENERAL_FRANCE/GENERAL_AUSTRALIA;

## 模板计划(实现)

- 验证Animations文件是否可以分布在多个.rfa文件夹:Zhongzheng;(不能!!!!)

```
// singleShotWeaponsMod.inc
AnimationStateMachine.copyState Zhongzheng v_arg1 No4 1.0 K98 1.0
// 3pAnimationsTweakingMod.con
AnimationStateMachine.set3pAnimationSpeed Ub_StandReloadZhongzheng 0.52
AnimationStateMachine.set3pAnimationSpeed Ub_LieReloadZhongzheng 0.52
// 1pAnimationsTweakingMod.con
AnimationStateMachine.set1pAnimationSpeed Ub_StandReloadZhongzheng 0.5
AnimationStateMachine.set1pAnimationSpeed Ub_LieReloadZhongzheng 0.5
// AnimationStatesShoot.con
AnimationStateMachine.setActiveState Ub_FireZhongzheng
AnimationStateMachine.addTransitionWhenDone Ub_StandReloadZhongzheng
AnimationStateMachine.setActiveState Ub_LieFireZhongzheng
AnimationStateMachine.addTransitionWhenDone Ub_LieReloadZhongzheng
```

归档每个模板到独立文件夹:阵营人物(X)/装备模板(X)/武器模板(步枪(X)/冲锋枪/固定机枪)/载具(装甲车/坦克/自行火炮/卡车/吉普/固定大炮/动物(X)/坐骑(X))/地图建筑;

- WWIIReality 右键机械瞄准的实现,调整以下参数:
```
ObjectTemplate.soldierZoomFov 1
ObjectTemplate.soldierZoomPosition -0.072/0.044/-0.2
ObjectTemplate.soldierCameraPosition -0.01/-0.04/0.09 //(原版)
枪体相对于人的移动                  -(更加靠左)/+(更加靠下)/-(更加靠前)
ObjectTemplate.soldierZoomPosition -0.075/0.047/-0.1
```
躺下的持枪姿势可能和站立时一样;
- 如果固定 soldierCameraPosition,同样的 soldierZoomPosition 会不会(几乎)是同样的效果??

慢化手持武器的动作(快速抖动):
```
AnimationStateMachine.set1pAnimationSpeed Ub_StandFireBeretta3842 0.03
AnimationStateMachine.set1pAnimationSpeed Ub_StandBeretta3842 0.03
AnimationStateMachine.set1pAnimationSpeed Ub_TurnBeretta3842 1.01
AnimationStateMachine.set1pAnimationSpeed Ub_StandAimBeretta3842 0.03
AnimationStateMachine.set1pAnimationSpeed Ub_LieFireBeretta3842 0.03
AnimationStateMachine.set1pAnimationSpeed Ub_LieBeretta3842 0.03
AnimationStateMachine.set1pAnimationSpeed Ub_IdleBeretta38421 0.005
AnimationStateMachine.set1pAnimationSpeed Ub_IdleBeretta38422 0.005
AnimationStateMachine.set1pAnimationSpeed Ub_IdleBeretta38423 0.005
```

调整机械瞄准技巧(本质上是在移动看枪的视角):
先距离(Z)(-脑袋前移,+脑袋后移);再左右(X)(-脑袋移到右边,+脑袋移到左边);最后上下(Y)(-脑袋移到上边,+脑袋移到下边);
实验:-0.08/0.023/0.1 --> -0.08/0.013/0.1 --> -0.18/0.013/0.1 --> -0.08/0.013/-0.05 --> -0.08/0.013/-0.18
实验s:-0.092/0.02/-0.18 --> -0.092/0.017/-0.18 --> -0.09/0.017/-0.18 --> -0.086/0.017/-0.18

固定 soldierZoomPosition = -0.09/0.017/-0.18 ,开始左移"soldierCameraPosition"是否有效:无效;
"soldierCameraPosition"只控制机瞄前的;

调整 "ObjectTemplate.addTemplate CarcanoComplex" 的位置有用吗?
令"ObjectTemplate.setPosition 0.2/0.0/0.0"(X轴+右-左):无效;

尝试旋转枪体,是否有效:可行;
```
ObjectTemplate.addTemplate ThompsonLod
ObjectTemplate.setPosition 0.0027/0.017/0.0 // 枪体向右(+)/枪体向上(+)/; 
ObjectTemplate.setRotation 0.31/1.6/0 // 枪托向左(+)/枪托向上(+)/枪托逆时针转动(+);
(枪托确定位置之后,准星相对机械准星的最终偏移已经确定)
-0.12/0.011/0.1
距离(Z)(-脑袋前移,+脑袋后移);
左右(X)(-脑袋移到右边,+脑袋移到左边);
上下(Y)(-脑袋移到上边,+脑袋移到下边);
视角正常后(3点1线),准星仍偏离机械准星,往那边偏,枪托就往反方向移动;
ObjectTemplate.setPosition 0.00/0.00/0.00
ObjectTemplate.setRotation 0.00/0.00/0.00
```

调整机械瞄准无误后是否还可以使用放大(ObjectTemplate.soldierZoomFov):虽然不改变中心,但是没有放缩远处的效果,只是拉近和枪的距离;

调整机械瞄准无误后是否还可以使用放大(ObjectTemplate.zoomFov):可以;

使用 grep 对比两个文件的不同:
```
grep -vwf D:\BF1942\Rebuild_XWWII\WWIIReality___________RES\animations\AnimationStatesLie.con D:\BF1942\Rebuild_XWWII\bf1942___RES\animations\AnimationStatesLie.con
```

刚才改 ZB26 的机瞄,右键一直无效(动作不变);原来必须加上"zoomFov,soldierZoomFov"在.con里;

- 一个可以尝试的Trick:做一个细长圆柱C穿过Garand的瞄准线路,然后在游戏里对齐细长圆柱C,
那么每次只需要将新的枪体NewGun对齐C,再套用Garand的位置(soldierZoomPosition/setPosition/setRotation); <不可行>

-----------------------------------------------------------------
我知道战地1942的3D引擎总体来说不适合机械瞄准 但是我还是尝试了3D-坐标对齐的机械瞄准 
如果是你 你选择哪种机械瞄准??
左侧两个"真机械瞄准"(通过3D模型对坐标实现)和右侧两个"伪机械瞄准"(通过贴图实现)

-----------------------------------------------------------------
### 机械瞄准采样视频
https://www.bilibili.com/video/BV14s41157uq;
https://www.bilibili.com/video/BV1ut411y7t7;
https://www.bilibili.com/video/av23463144;
https://www.bilibili.com/video/BV1Es411u74A;
https://www.bilibili.com/video/BV1Y64y1Y7Cj;
https://www.bilibili.com/video/BV1c4411C7ai;
https://www.bilibili.com/video/BV1oW41157kb;

- 机械瞄准的边缘虚化方法:
仍然选择Alpha通道选区,然后选择反向,
然后羽化,值设定为5,然后选择反向-Del,
背景色选择为白色;(如若背景色=黑色,在左侧工具栏倒数第三个选项修改(前景色背景色对换)(摁一个左/下箭头符号))
还有一种方法:先模糊,然后选区实体,再转到Alpha通道上Del(以达到边缘模糊的效果);
最后,在实体上选对应区建立Beta通道,再复制对应区域粘贴到最终Alpha通道上(避免枪体透明化);

- 下一个版本:XWW2-FB-0.1-beta;(不增加新阵营,但是会扩充地图/建筑物/载具/武器/优化原有贴图)

---------------------------------------------------------------------
### 继续制作新地图:

- XWW2_Russell_Islands;
- XWW2_Kasserine_Pass:无Conquest模式却用ED42打开的方法:加一任意地图的 materialmap.raw;
- XWW2_Halfaya_Pass(1941年6月15日,Northwest Egypt):;

- 给 XWW2_TRAIN_MOV 增加烟雾:(配对 railroad_no_collision_m1 设置 ObjectTemplate.setHasCollisionPhysics 0)
在 Objects.con(写一个大于他最大生命值的设定值):
```
ObjectTemplate.addArmorEffect 550 e_ExplGas 0/6.0/34     // 被忽略;
ObjectTemplate.addArmorEffect 540 e_WillyDamage 0/6.1/33 // 被忽略;
ObjectTemplate.addArmorEffect 530 e_PanzDamage 0/6.1/30
```
最终生效方法:
```
ObjectTemplate.addArmorEffect 550 e_WillyDamage 0/6.4/35
ObjectTemplate.addArmorEffect 550 e_WillyDamage 0/6.1/30
```

- bullet_vis_m1:仿照巴祖卡火箭弹写法,最终可见(真.星球大战);

xww2_ruin_building1:搭配 BuildingSmokeIdleDark 使用;
xww2_ruin_building2:;
mb_china_roof_tiles:纹理标记法:红/黄/蓝/绿/黑/紫/橘/白;
```
texture "texture/mark_black";
texture "texture/mark_green";
texture "texture/mark_white";
texture "texture/mark_pink";
texture "texture/mark_blue";
texture "texture/mark_purple";
texture "texture/mark_orange";
texture "texture/mark_yellow";
texture "texture/xww2_public_metal_4";
```
mb_china_corridor_curve:;
mb_china_street_yard:超大的院子;

- 士兵中弹特效:可能还需深色化;
- PR1942中的可破坏油桶研究:;
- 材质:装甲车 ID=45/坦克 ID=50;
b
替换文件 CON_FILE 中的 re_EFFECT_STR 模式的字符串为 CON_SCRIPT_STRING:编写Python脚本解决;
- 6in26cwt 的材质用尽办法无反应:重做所有Geo ID=45仍然无反应;

火炮的空中观测镜出现的原因:因为它以为你是侦察兵(在sdkfz232上观察位下来)!
找到十字位置(CHTCrossHair ):(mdt说defined in menu files);当前Cock:;
```
ObjectTemplate.crossHairIcon "IronSights/Iron_Tank.tga"
```
"as mentioned above, place transform node on first splitNode(and first transform) in InGame file;"
(四个参数分别是(HUD左上角X,HUD左上角Y,HUD长,HUD宽))

- ED42中放置物品小技巧:选中物体后:右键摁住移动,滚鼠上下移动;
- Blender复制粘贴的技巧:在编辑模式下选择一部分物体,"shift+d"移动鼠标,就可以复制并移动出要复制部分;
(鉴于外部模型的高精度,修改已有.sm/.obj模型是不错的思路;)
- OBJ用Blender导出缺少面的问题:;Jap_ScoutHelm;
- animal_elephant:模仿 FragMod 里的油桶(去掉Entry和Engine);Animal_Elephant;elephant_roar.wav;ElephantBody/ElephantHead/Dead_Animal_Elephant;;
(动物声音宜套用 HoHaTurret.ssc);
- mb_earphone:德军装甲兵耳机;
- dod_tank_camouflage:坦克伪装植被;
```
rem --------------- **** tankcamouflage **** -------------------
ObjectTemplate.addTemplate dod_tank_camouflage
ObjectTemplate.setPosition 0.9/0.4/1.9
ObjectTemplate.setRotation 3/-47/13
ObjectTemplate.addTemplate dod_tank_camouflage
ObjectTemplate.setPosition -0.9/0.4/-1.9
ObjectTemplate.setRotation 13/47/23
ObjectTemplate.addTemplate dod_tank_camouflage
ObjectTemplate.setPosition 0.9/0.4/-1.9
ObjectTemplate.setRotation 13/47/23
ObjectTemplate.addTemplate dod_tank_camouflage
ObjectTemplate.setPosition -0.9/0.4/1.9
ObjectTemplate.setRotation -3/-47/-13
ObjectTemplate.addTemplate dod_tank_camouflage
ObjectTemplate.setPosition 0.0/0.4/-2.1
rem -------------------------------------
```

- 新增 SVT40:原来EXWWII里有模型和定义,XWWII里有机瞄贴图;
- 修正苏联早期夏季冬季(ERAWIN_i)/晚期夏季冬季装备(MRAWIN_i)/苏联黑海海军:cccp_we_cap/cccp_wc_cap/cccp_init_cap/cccp_food_parcel/;
- Animal_Camel:CamelBody/CamelHead/Dead_Animal_Camel;texture "texture/Animal_Camel";
- 苏联黑海海军:;
- CivModCar:CivModCar_Hull_M1,1P_CivModCar_Hull_M1;
- 固定机枪 Stationary_Maxim:Maxim_Gun,Maxim_Gun_Main,;
- 移动火炮 MOV_PAK36(四件套:底座/炮筒/左右轮子):MOV_PAK36_Base,MOV_PAK36_Barrel,MOV_PAK36_RightWheel,MOV_PAK36_LeftWheel;
无法立足,现将 MOV_PAK36_Base 用原 french75 型(组合新炮的Sheild和ATT_Shield制作),轮子同大小:不可行;(这个问题可能来自于Geo声明失误)
无法立足,现将 MOV_PAK36_Base 用原 french75 型ATT_Shield(组合新炮的Sheild和Barrel制作MOV_PAK36_Barrel),轮子同大小:可行;

          ------ *** Deadly Dozen 2 Pacific Theater *** ------

- 可击落但是无法驾驶的飞机 fake_aircraft_ki21:fake_aircraft_engine/fake_aircraft_ki21_Hull/fake_aircraft_ki21_Inv;
(飞象可以飞的原因:他在地面已经具备了水平方向的初速度,再受到一个恒定的垂直方向的作用力)
最终的解决方法是非常简单的:令主体不可见,再加载旋转的飞机模型在主体上面即可;
- 可击沉但是无法驾驶的战舰 fake_warship_Poland_Danae:DefgunWreck/fake_warship_Poland_Danae_Hull/;
fake_warship_Poland_Grom:DefgunWreck/fake_warship_Poland_Grom_Hull/;
fake_warship_Poland_Orzel:DefgunWreck/fake_warship_Poland_Orzel_Hull/;


- Stationary_AAMaxim:Stationary_AAMaxim_Main/Maxim_Gun_AA/;
- Stationary_DHSK:Stationary_DHSK_Main/Stationary_DHSK_GUN/;
- Stationary_Hotchkiss:Stationary_Hotchkiss_Main/Stationary_Hotchkiss_GUN/;
- Stationary_Lewis:Stationary_Lewis_Main/Stationary_Lewis_GUN/;
- MOV_PAK36 更换炮弹类型也对KV1无效;

blender 消除"黑面":编辑模式下--->按a全选--->网格,法线,重新计算外侧;

Haining's miniworld

- dod脸的放缩倍数:0.00025;
- 人物模型制作:xww2_figure_hair_1/xww2_figure_head_1/xww2_figure_body_1/xww2_figure_body_dead_1/xww2_figure_hand_1/xww2_figure_legs_1/xww2_figure_bodyc_1;
- 可动人物 xww2_figure_chinaj_commander:xww2_figure_base;(创建成功)
- 创建人员(非参加战斗人员):护士(苏联)/地勤人员(日本)/指挥官(德军)/百姓(中国);
xww2_figure_nurse_1:xww2_figure_women_hair/xww2_figure_nurse_body_1/xww2_figure_nurse_head_1/xww2_figure_nurse_box;
xww2_figure_japnavy_1:xww2_figure_japnavy_head_1/xww2_figure_japnavy_body_1/xww2_figure_japnavy_body_1_M1;ger_africa_glass;

- 对各版本的AI文件归档:没有发现什么特别的,甚至XWW2的AI.con文件比FH还大;

- 开发的方向:优先模板化地开发(先多开发各种模板);
1.手持冷兵器模板 china_broadsword_mod:完成了,但是非常麻烦的baf复制工作,另外新建一个.con是可行的(但是记得run);
    (使用python构建了自动复制工作);
    mong_sabre:反复运行baf复制程序不会多出文件,只会覆盖以前的文件;
2.马上冷兵器模板 warhorse_with_spear_mod:只需加上weapons.con里定义的Turret即可;(参考中世纪mod);
    warhorse_with_polish_spear:cavalry_polish_spear/cavalry_polish_flag/;
3.马上枪械模板 warhorse_with_gun_mod:调整好Camera的过程让人崩溃(否则没有手的枪悬浮于空中);(参考bf1918);
    warhorse_with_type99:cavalry_type99;cavalry_mp18;
    warhorse_with_kar98k:cavalry_kar98k;kar98k_on_horse;
    warhorse_with_carcano:cavalry_carcano;carcano_on_horse;
    warhorse_with_mosin_nagant:cavalry_mosin_nagant;mosin_nagant_on_horse;
    重构"HorseWhite"使得马皮肤的重载更方便(HorseWhite/DeadhorseWhite/legs);
5.掷弹筒/枪榴弹模板 jap_projectile_launcher_mod:
    K98RifleGrenade:用py程序完成移植;
    jap_projectile_launcher_mod:日军掷弹筒;
    no4_projectile_launcher:no4_projectile_launcher_main(本有的模型贴图也具有特殊性);
6.反坦克手雷模板 HHL_AT:应当模仿"TNTProjectile";(相当于重做)
4.拖拽大炮模板 vehicle_towed_cannon_mod:;
- 一个重要的机制:当m3a1在mod和原版中同被定义且零件定义有差异时候,m3a1在原版中的零件就被忽略了;
7.固定的反坦克枪模板 stationary_atgun_mod:Icon_ptrd/;
```
ObjectTemplate.addTemplate e_MuzzHeavy
ObjectTemplate.startoneffects 1
ObjectTemplate.setPosition 0/0/0.95 // 最后一位+即往枪口方向移动;
```


下一步行动:
1.开发基于模板更多的武器;
    AT_jap_pole_mine:即使是TNT类型 也可以用k98的携带动作;
    ger_combined_grenade:可以摧毁装甲;
2.制作更多的地图建筑(包括改变天空/更多Figures);
    扒取各个模组的可使用建筑,统一导入(命名格式:mb_euro_bridge)也就是"来源_区域_物体名";

3.Reinforcement之前的地图(包括可玩性和AI的优化,载具的布置);
- XWW2_Aachen:加载具/建筑(其载具模板的单机模式引用的是:"run Conquest/ObjectSpawnTemplates");
- XWW2_Aalborg:可以把steel桥当作部件添加给当前的桥;
- XWW2_Alsace:地图里的旋转+是顺时针方向;
- XWW2_Arden_Mountains:添加了地堡,载具需要更正;
- XWW2_Barbarossa:建筑物的"组合"也是一种不影响AI路径的方法;(做地图机枪的一个技巧:套先用mg42(严格的小写"stationary_mg42");)
- XWW2_Battle_of_the_Bulge:新增"mb_single_soldier_trench";
- XWW2_Battleaxe:"Terrain.con"里指定了HeightMap,注意修改其路径以使得ED42改的地形生效;
- XWW2_Bihachi:为游击队装甲车添加旗帜;
- XWW2_Bloody_Ridge:新增鸟类"nightingale";
- XWW2_Bocage:增加"pega_oatfield_middle2";
- XWW2_Bougainville:去掉了挡住步兵和坦克的壕沟;
- XWW2_Coral_Sea:套用原版的地图,外加增加云朵(cloud_m1)/海鸥(seagull1);
- XWW2_Danzig:更正"mb_block_house"材质;
- XWW2_Fornebu:利用建筑物给桥添加装饰;
- XWW2_Hannut:新增一些建筑;(这张地图确实有扰乱Projetile的问题)
- XWW2_Ichi-go:修改建筑(更多中国建筑?);
- XWW2_Ihantala:需要修改AI积极进攻(Strategy.con确实是策略核心文件,但是最终是通过删除了那俩有问题的出生点解决的);
- XWW2_Iwo_Jima:在滩头添加两栖装甲车(LVT4的AI有问题,套用了M3A1的解决);
- XWW2_Kamenets_Podolskiy:Ferdinand AI修改,SU76 AI修改(但是AI仍然不使用);
- XWW2_Karelia:需要修改AI积极进攻(通过修改Strategy.con);
- XWW2_Kasserine_Pass:修改Trench使得不挡住AI;
- XWW2_Kendari:修改建筑;
- XWW2_Kharkov:给轴心国增加反坦克武器(可以用添加静态object的方式添加机枪!这个方法添加固定武器特别方便);
- XWW2_Kohima:大小写修改;
- XWW2_Kokoda_Trail:修改建筑,给澳军新增载具("mb_pacific_suspension_bridge"缩小2倍);
- XWW2_Laiyuan:给中国军队新增载具,修改建筑(更多堡垒);("mb_china_bridge_a1"缩小2倍);
- XWW2_Mentone:修改建筑;
- XWW2_Milne_Bay:更多植被(dod_high_grass);
- XWW2_New_Britain:修改建筑;
- XWW2_Nomonhan:更多载具(马匹),修正贴图;
- XWW2_Saint_Quentin:建筑不够丰富;
- XWW2_Salamaua:更多植被;
- XWW2_Seelow_Heights:需要修改AI积极进攻;
- XWW2_Stalingrad:增加坦克和反坦克武器/苏军AI/政委人物;
    xww2_figure_cccp_cpt_1:xww2_figure_cccp_cpt_head_1/xww2_figure_cccp_cpt_body_1/xww2_figure_cccp_cpt_body_1_M1;
- XWW2_Wake:更多植被;
- XWW2_Walcheren_Causeway:德军更多载具;(加入装甲列车)
- XWW2_Zitadelle:Ferdinand AI修改后加入;
- XWW2_Volga:加入 cruiser_cccp_red_ukraine;

### 添加准星
- 手持武器统一的 Iron_Handweapon_CrossHair.tga;
- 移植西部战争的 chuck_mod(cheval_horse_head):"renderer.beginGlobalCluster"的作用是将整个整体Geometry当作simpleObject引用;
- 冷门步枪统一的"Iron_Rifile.tga":;

### Equipements 强化:
- 加入掷弹筒到英/德/日步兵:K98RifleGrenade/no4_projectile_launcher/jap_projectile_launcher_mod(itemIndex = 6)(Icon_rifile_launcher/Icon_jap_projectile);
- 美军火焰喷射器装备特殊化:重建"ht130";
- 苏联黑海海军 RusMarineKit(CCCPM_1):cccp_marine_cap/cccp_helmet_36/cccp_cloak/cccp_marine_hippack/;
- 轨道大炮(wwii_tracked_artillery_mod)/装甲列车(wwii_amoured_train_mod/wwii_amoured_train_ger_turret):带Collision的铁轨(wwii_col_railroad_s/wwii_col_railroad_c);
    sounds:wwii_train_running/wwii_train_start;
    wwii_amoured_train_cccp:wwii_amoured_train_cccp_turret/wwii_amoured_train_cccp_carriage;
    长的轨道高台:wwii_railroad_long_noc/wwii_railroad_very_long_noc;(LOD和COL不一样时,贴图可能贴不上(先单独导出为sm再导入合并))
- 民用军车 civ_car_wgh:Civ_Car_WGH_Hull_M1/icon_civ_car_wgh;
    顺便测试能否令其无法转向(在"RotationalBundle Train_FrontWheelR"中改);
- Hippack 强化:英(British_hippack_m1/brit_Assult_Bacpac_m1)/德(German_hippack_m1/German_hippack_officer)/日(Jap_hippack_m1/BacpacBig_jap_m1(再在objects.con里加上"BacpacBig_jap"))/美(Us_hippack_officer/US_Assult_Bacpac_m1);
- 火箭筒威力修改:改为"75mm_Mk5_AProjectile";
- 将几种实现的Handweapons加到Kits里;
- mp18的长弹鼓型 mp18_with_drum,drum_of_mp18/鲁格手枪:LugerP08;(配给新kit:德军宪兵军官 GerMilitaryPolice/ger_ss_cap/ger_military_tag)
- 中型炮舰(驱逐舰级别) wwii_destroyer_mod:cruiser_cccp_red_ukraine(Fletcher_cannon,Fletcher_cannon_Front 必须都加上才能不在主PCO跳出);
- 固定堡垒 xww2_buncker_mod:mb_china_middle_square_bunker_a2_m1()//过多的 MAXIM_PCO_in_buncker 导致了选择后退出(游戏本来的限制?);
- 几种还需实现的载具: I号坦克(维修型)/PanzerI_maintenance/PanzerI_maintenance_hull_m1/PanzerI_maintenance_turret_m1/PanzerI_maintenance_carry_hull_m1/PanzerI_maintenance_carry(icon_PanzerIC.tga/icon_PanzerIC_mt.tga); 
- 马拖拽的可卸载大炮 wwii_horse_drag_drop_AT: ;
- 机械瞄准的重制:Breda/Mas36///;
- 士兵尸体:美军(usa_dead_soldiers/dod_usa_dead_soldiers_m1); 动物特效:
    奶牛:animal_cow/animal_cow_head/animal_cow_body(cow_roar);
    鳄鱼:animal_crocodile/animal_crocodile_head/animal_crocodile_body/animal_crocodile_hurt_effect;

### 最后的问题修正

- 尝试套用FHSW的步枪Reload动作:不可;
- 死亡动作的优化:已完成(消除了正反面中枪飞出去的死亡动作);

- 搜看MB下MODS看看还有没有什么可以添加的:
    1.苏军护士的衣服贴图:xww2_nurse_body_uniform;
    2.ppsh的弹夹型,ppd的弹鼓型,索米的弹夹型;
        ppsh41_clip/ppd_drum/suomi_clip;        
    3.将 KnifeAllies/KnifeAxis 分别换成 刺刀/工兵铲;
    4.m50_reising(替换太平洋的m3冲锋枪):Icon_m50_reising/US-L_engineer_m55.dds;
    
    5.W_wuqi_3 中一众武器:m1carbine_para(icon_m1carbine_para)/Carbine_para_ai/m1carbine_para_M1(US-airbne_anti_tank)/machinegun_bracket_close/machinegun_bracket_open(as SimpleObject)/Panzershreck(Ger-SS-M_anti_tank,带炮塔型luger:LugerP08_drum(icon_LugerP08_drum));
    (Kit 声明里 ObjectTemplate.addTemplate 最顶的武器是默认持有的);
    --- **注意setIcon的编号不能错!!!** --- 

### 逐地图问题测试
(逐个玩一轮,开64人模式;)
1.背景影像重制; ---<FINISHED>
2.XWW2_Aachen:铲子和刺刀的icon替换(icon_axisknife/icon_alliesknife)/CivCpeRust 的 closed 版本的后窗没封闭问题/CivCpeRust 处于地图范围外(bots不使用);刺刀过长; ---<FINISHED>
3.地图载具icon的替换; ---<FINISHED>
4.XWW2_Barbarossa:苏军早期工程兵/步枪兵加装早期头盔,指挥官加望远镜; ---<FINISHED>
5.XWW2_Battleaxe:在意军山下基地出现时易跳出; ---<FINISHED>
    (baseflag的声明不显式出现在.con里,须自行添加"baseflag_conp_XXX.dds";)
6.XWW2_Bocage:美军帽子改为"带扣型"(更有战场感); ---<FINISHED>
7.XWW2_Bougainville:Type92向下移动; ---<FINISHED>
8.对换"中枪指前"和"中枪跪地"动作(还调节了动作); ---<FINISHED>
9.还需改进的问题:荷兰陆军帽布/I-153的Iron/加入wgh的patch/加入Andre的patch; ---<FINISHED>
10.XWW2_New_Britain 高炮调整; ---<FINISHED>
12.新增:en_africa_hat(英军的非洲防晒帽)/Sculpture_Angel_M1(原版的雕塑); ---<FINISHED>
13.加入 Scherenfernrohr:修改Projetile; ---<FINISHED>
14.KMT hippack:.sm模型预览白色,贴图也没有问题时,先导入Blender再导出. ---<FINISHED>

11.XWW2_Battleaxe/XWW2_Halfaya_Pass/ 地图跳出问题:;

---------------------------------------------
### Announcing V0.1 stable version !!!

Hello friends, glad to announce that I released the stable version of "XWWII: Forgotten Battles" V0.1, as you known, it's the fixed version of the previous V0.1, but many new features had been included into the new version, so, don't download the previous one anymore; 

Change log:

0.Added 26 vehicles,15 handweapons,5 new singleplayer maps;
1.Some new crosshair icons;
2.Many ironsights remade(remain the textures);
3.23 maps had been remade;
4.Trains, Amoured trains, dragged artilleries added;
5.Soldiers hippacks and backpacks remade;
6.Die-hit animations improved;
7.Die-hit effect improved;
8.About 42 map buildings/vegetations added/fixed;
9.Some bugs fixed;
10.The AI in 2 Soviet-Finland war maps fixed;

free-download:https://bilibili.iiilab.com/

------------------------------------------------------------
### BG42 map patch
编写python程序扒取所有和地图实体相关的物体以可以轻松移植地图;

XWW2_Merderet_Bridge:桥中的实体有所缺失;
XWW2_Waldhambach:1944.12德国小镇攻防战;
XWW2_Sedan:1940.05德国闪击法国;(换天实验);
    如何更换天空:在SkyAndSun.con里套用对应语句即可;
XWW2_Ortona:找到 bg_clothesline_m1;

-------------------------------------------------------------
### 二战中国战场加强
不同军种:二十九军(西北军)/滇军/中央军/川军;
    ch_grass_cap/ch_adrian_helmet/ch_tonny_helmet/jap_sunny_helmet/ch_army_normal_cap/ch_ammo_hippack/ch_wb_backpack;
    ch_officer_hippack;ch_mg_gunner_shawl;

Blender UV贴图教程:(https://jingyan.baidu.com/article/363872ecf6367f2f4ba16f95.html)选择点面 --> 按U -->智能投射;

XWW2_Taierzhuang:修改天空的三个要点:SkyAndSun.con,Init.con开头,有时候需要重载"Textures"文件夹!
XWW2_Xifengkou:wwii_china_great_wall/xww2_aigle/

二十九军:ChinaXibeiKit/jap_early_cap/jap_early_winter_coat/ch_army_winter_cap/ch_army_normal_cap_glass/
ch_tommy1928:晋绥军产汤普森;
中国城市建筑:xww2_china_city_building_1/xww2_china_city_building_2/xww2_china_city_building_3/xww2_china_lugou_bridge/xww2_china_lugou_bridge_stele;

XWW2_Lugou_Bridge:;citymesh/stnwall/jap_early_guandong_helmet
xww2_china_billboard_1/xww2_china_billboard_2/xww2_china_billboard_3/xww2_china_billboard_4;
    日军装备加上 jap_katana 到 Jap_officer_hippack_m1;
    导入 katana 动作(CommandoKnife/ObjectTemplate.addTemplate Tati);

XWW2_Hukawng_Valley(中国远征军):kmt_cap_yellow/kmt_n1a_hippack/CHN1A_0/kmt_n1a_helmet/fake_aircraft_ki10;

双枪:参考 Western_War 的(MauserC96Double);动作套用失败,改用"Exppack"的动作;尝试后来还是原计划;
    Pistolaxis:"kits/cera_NCO_sp.tga"/"Weapon/Icon_dmc96.tga"/CERA_1_SP;
中国伪军:国籍是中国军队,但是重载伪军旗帜;ch_fake_gov_backpack/ch_fake_gov_cap/ch_fake_gov_nco_cap//;

XWW2_Qixian:(https://baijiahao.baidu.com/s?id=1660289558563621933) /mb_native_village_short_wall_m1//;
    需要新增 jap_early_french_helmet;
FHE 观测:wgh2000的抄袭是否存在;
    新增苏军30s装备:cccp_budyonny_hat_winter/cccp_budyonny_hat_closed/cccp_budyonny_hat_opened/cccp_backpack_complexed/cccp_helmet_36;
    新增意大利北非沙漠装备:italy_afr_helmet_glasses/italy_afr_officer_cap/italy_afr_hull_cap//;

XWW2_Kanchatzu:(3706-kanchatzu_incident);
XWW2_Songhu128:
    新增日军早期海军陆战队:jap_30s_snlf_helmet/jap_30s_snlf_cap/;
    新增十九路军装备(粤军):;

- 问题队列:
1. XWW2_Hukawng_Valley:存在环形堑壕凌空;    <FINISHED>
2. 医疗柜待有效化;    <FINISHED>
3. XWW2_Ortona 跳出:先去除所有载具(不会跳出)/stg44 iron调整;    <FINISHED>
    仅仅加上机枪和侦擦车辆,火炮:不会跳出;   <FINISHED>
4. XWW2_Nanking:标语/海报修改;   <FINISHED>
5. jap_early_winter_coat 的下部调整;

再次感谢网友的鼓励,扩展制作这个模组的初心是2008年夏地震在家时第一次玩的震撼;
做这个模组的原则是"伤其十指,不如断其一指":我会集中90%的精力专注于"复现被遗忘的二战战役和阵营";
其他元素诸如可玩性、画面精细程度、载具丰富程度、扩展到其他版本等都不是我在意的事情;
做模组就像写文章,每篇文章有自己的文眼和主旨思想,不可能是大杂烩,如果这也想要那也想要,最后必然什么都做不好!
每个模组都有自己的优缺点,精力有限,我只能忽略大部分缺点,把它的优点部分做到极致;
我强调的是深度,不是广度;

"有太多的信息,知道这些信息反而对你不好.现在有information overload problem,因为太多的信息会confine your imagination,因为每个信息都像是事实,非常肯定的说我发现了这个、我发现了那个,所以读了一大堆paper,你什么事情也做不成,你什么事情也不敢做,因为你的思路都被限制了;"
    ---- 蒲慕明所长在中科院神经所2010年会上的讲话;

距离下一个版本上传还剩下:阿比西尼亚,菲律宾,希腊;
https://tanks-encyclopedia.com/

### AbyssiniaSoldier

AbyssiniaKit:AbySoldierCap,AbyOfficierCap;ABYSS_3;abyss_engineer.tga;abyss_support.tga;abyss_NCO.tga;abyss_officer.tga;abyss_rifleman.tga;
武器:弓箭(bow_and_arrow);lebel_rifile(勒贝尔步枪);bow_and_arrow_backpack;ArrowProjectile

XWW2_Fall_Of_Axum:(Oct 15,1935)

中国战场室内物件:dating_china_08;dating_desks_05;dating_desks_1;dating_desks_2;dating_desks_3;dating_light_04;;;;

### XWWII:Forgotten Battles v0.11 enhanced version;

This is a re-fixed version based on the "XWW2:Forgotten Battles v0.1 Stable Version";

Some maps from BG42 has been re-made and added into this version, and I've asked for the modding rights to the maps authors by emails; If which map failed to obtain your permission, please let me know and I'll delete that;

Have fun!!

------------------------------------------------------------------------
### XWW2-地图包-20220828
主要新增一些近战地图(以及原版地图);

1.XWW2_Battleaxe(修复跳出):是 m3gmc 导致(换为 Lynx);
2.XWW2_Guadalcanal:ED42的树种植工具很好用,它会自动考虑贴合地面/我修改了树(Jungle_tree11_M1 等等)的阴影显示问题,增大了Lod距离(字符串替换,在 Geometries.con 里);
3.XWW2_Vilnius(八路军那张图的原版):加入了一些堡垒;
4.XWW2_Manila(原版 Berlin 修改/加入一些 BG42 工厂):1945年2月10日;Deadly Dozen:Manila;
    - Flag的问题:即使在Init.con里修改也是苏德:因为"./SinglePlayer/ControlPointTemplates.con:ObjectTemplate.setTeamGeometry 1 flagge_m1";
5.XWW2_Saipan(原版奥马哈海滩):(1944.06.15)(植物组:Jungle_tree9_M1/Pacific_Palm_large_2_M1/Jungle_plant16_M1/Jungle_plant11_M1/Jungle_tree7_M1);
6.XWW2_Arras(5月22日/原版波卡基):(Way to Dunkirk)
    - 快捷键旋转物体(ED42):左下角RotateObj选项选中即可!
    - 以 Static Obj 形式放入地图的武器会在第二局被清空;
7.XWW2_Kursk(更换天空/地面为波卡基):;
8.XWW2_Rabaul(原Neringa那张图):
 - ObjectTemplate.setTeamGeometry 1 flagjp_m1
 - ObjectTemplate.setTeamGeometry 2 flagau_m1
9.XWW2_Vistula_River:跳出原因:3D文件资源路径仍含原地图名,窗口模式不报错跳出;

### 涉及枪弹击中地面特效的远视化
可见特效:Em_richoSand1(Emitter)/e_richoSand(EffectBundle)/e_richoGround(EffectBundle);

--------------------------------------------------------
### Release Mappack

How to install this mappack:

1.unzip the file xww2_mappack_20220828.zip;

2.put "xww2_mappack_20220828/archives/objects.rfa" into "BF1942/Mods/XWWII/archives" to replace the existing file "objects.rfa";

3.put map files(.rfa files) in the "xww2_mappack_20220828/archives/bf1942/levels" into "BF1942/Mods/XWWII/archives/bf1942/levels";

-----------------------------------------------------------
### 更多的调整
- 设置AI攻击视野:AI.con的"aiSettings.setViewDistance 40";
- PPSH大小调整(手移动到弹夹之后):PPSh41/PPSh41_drum;
- EHeer_1_ppsh:德军在斯大林格勒喜欢使用ppsh;Ger-Herr-E_NCO_ppsh.dds;
- 盟国多军服的脸部与德军脱离:AlliesFace1/AlliesFace2/AlliesFace3;FMAlliesComplexHead1/FMAlliesComplexHead2/FMAlliesComplexHead3;AlliesHead;FMAlliesHead;
- FG42(Gewehr42)的FOV倍数修改;
- 欧洲城墙套装:mb_native_citywall/mb_native_citywall_de/mb_native_citywall_stairs;
- 多种载具和武器的mod(模板)(只需改模型,轮子什么的动力装置自动对齐):
    ♞轻型坦克mod(wwii_light_tank_mod):英国MKI轻型坦克(100行内代码实现!!);
        "Ha-Go_GunBase"太靠里会导致炮弹打在炮塔内部;
        ObjectTemplate.setPosition 0.0/0.920/-0.250 左(-)/下(-)/后(-)(炮塔)
        对机枪和炮塔,左右控制似乎是反着的;
        再造一辆"somuas35":somuas35_hull_m1/somuas35_turret_m1;"Icon_MG_PCO.tga";(Reticule)"Iron_Tank_Eng.dds";
    ♞中型坦克mod(wwii_medium_tank_mod):;
    ♞重型坦克mod(wwii_heavy_tank_mod):;
    ♞卡车mod(wwii_truck_mod):需要综合考虑两轮/三轮的情况(基础是 Katyusha);
        实为 Bedford:wwii_truck_mod_M1;
        考虑两轮/三轮的情况:另找四轮卡车,欧宝的:OpelBlitzEngine;
        - AI驾驶 wwii_truck_mod 时的跳出问题:换回 Katyusha_Engine 仍然跳出;
            更换 aiTemplate 为 M3A1:可行,猜想结论是:当不同类型的载具AI混用时就会报错跳出(猜测M3GMC的跳出也是因此);
    ♞半履带车mod(wwii_halftrack_mod):实为ZIS22;
        如若 Conquest 模式也不报错跳出,可能是addTemplate的内容不存在或者加错了位置:如"lod_wwii_halftrack_mod_Cockpit";
        新增"sdkfz7_tractor":sdkfz7_tractor_hull_M1;
    ♞机枪堡垒mod(wwii_machinegun_buncker_mod):
        bg42_japanese_mg_pillbox_M1:基础类型是防空火炮;
        再造一个堡垒"wwii_soviet_buncker":wwii_soviet_buncker_hull_m1;
        wwii_machinegun_buncker_ug:需要升高模型位置;增添2个 MAXIM_PCO_in_buncker 在侧面;
    ♞战斗机mod(wwii_aircraft_mod):二战法国 MS406 战斗机;
        wwii_aircraft_mod_m1;Engine添加位置或者其他部件对飞行有决定影响:不能省略,只能适当调整位置;
        由于尾翼位置不好调整,我已经将其3个组成部件设置为"不可见"类型的Wing;
        意大利雷电战斗机(MacchiC202):"__Flaps__"即机翼上的副翼;
    ♞轰炸机mod(wwii_bomber_mod):实为FH的"Icon_lancaster.dds"(Lancaster);
        wwii_bomber_mod_Hull_M1:;
    ♞战舰mod(wwii_warship_mod):实为 Bismarck 战列舰;
        wwii_warship_mod_main_m1;制作填充战舰比较空旷的甲板的"xww2_warship_sundries_m1";
    ♞潜艇mod(wwii_submarine_mod):实为FHSW的"icon_Sub14";
        wwii_submarine_mod_Hull_M1;
        法国潜艇 french_wwii_submarine:french_wwii_submarine_Hull_M1;Sub_Mod_SoldierSpawn;
    ♞自行火炮mod(wwii_spgun_mod):;
    ♞多联高射机枪(wwii_multiple_mg_mod):实为 icon_FlaMG131Zwilling;wwii_multiple_mg_mod_base_m1(公用的多联机枪底座);
        公共金属材质贴图:"xww2_public_metal_material.dds";
        Stationary_triple_m1919a4s(三联 m1919a4s):;
    可开动的电车(使用BG42的Tram_m1):wwii_amoured_train_city;


------------------------------------------------------------------------
### XWW2-地图包-20220901
主要是来自BG42,罗马之路,WarFront,各种原版Mappack等对地图模型支持好的地图(预计12张):

- XWW2_Cassino_Hill(1944年5月11日):波兰军队(英军装备) VS 绿色魔鬼伞兵师;Cass_1_M1-Cass_12_M1 贴图缺失;新增Kits:POL_EN_i;
POL_EN_engineer/POL_EN_NCO/POL_EN_officer/POL_EN_rifleman/POL_EN_support;
globalAmbientColor...接下来的四行对整个地图的明暗程度有巨大影响;
    3月15日早上8点,盟军制定的代号“狄更斯”行动拉开了三战卡西诺的序幕.盟军集中了所有前线的炮火和500多架来自英国、北非、西西里的盟军重型轰炸机向卡西诺战区德军防线狂轰乱炸,德军见势不妙及时布放烟雾,炸起的烟雾和德国人刻意施放的烟火笼罩了整个卡西诺地区；后边飞来的轰炸机看不见就胡乱投弹,悲剧开始了:远离战区的新西兰27机枪营被炸,几乎全部伤亡；法国摩洛哥战地医院被炸,炮兵阵地被炸.甚至于一枚炸弹准确无误的投进了英军第8集团军里斯中将的帐篷里,幸好他跑出去了没被炸死.前线准备出击的部队被这胡轰乱炸搞得晕头转向,有的官兵甚至怀疑是德军的飞机并向其开火.广大盟军前线官兵愤然的说:这些混蛋就想早早的把炸弹扔了飞回安乐窝里去鬼混;而德军在这恐怖的轰炸中静静的等待着,他们早已对此是见惯不惊了.

- XWW2_Eindhoven(地狱公路 Hell Road):FHSW内含许多类型"Germov_r";
- XWW2_Crimea(1944年5月9日,Main Direction of Attack):铁路缺失/Detail.dds还需调亮/增加装甲列车和碉堡;
    Germov_r/britt1_r/Japsen_r/Ryssov_r/Amerov_Z;
    "textureManager.alternativePath"越靠前优先级越高;
- XWW2_Brest_Fortress:互换阵营(ED42的SWAP无效)在Strategies.con里调整积极性;
- XWW2_Zitadelle:跳出问题:似乎是由 vehicle_towed_cannon_mod 引起;
    vehicle_towed_cannon_mod:;

---------------------------------------------------------------------------
### AI 不适配带来的跳出问题

M3GMC 的实验:将"M3GMCGunnerPCO1"的AI设置为"WespeCannon","M3GMCSPPassengerPCO0"的AI设置为"WillyPassenger",AI不会去使用,难道同一载具的 aiTemplate 之间存在约束关系?
    - 改"M3A1TopMG"为"HanomagTopMG":Bot仍然会使用...(约束关系猜想不成立);
    - 确定"M3GMCPassengerPCO0"为"WillyPassengerPCO2"后ai会用;但"WespeCannon"仍然不生效;
        经我测试:Wespe为单一座位载具,可能和这个有关(XWW2里重写了Wespe);
        在XWW2里重新添加了WespeCannon 的 AITemplate定义:但是载入地图后马上跳出;
        另外若该位置是FireArms,那么它的aiTemplate也最好是和PCO配对的(比如都是PCO的);
        最终添加完全WespeCannon对应的"addPlugIn"元素后,不再跳出,Bot会使用火炮并且开火攻击敌人;

新增冲锋枪战马系列:warhorse_with_ppsh41_drum;warhorse_with_ppsh41_clip;
    roundOfFire:越大越快;warhorse_with_ppsh41_drum:cavalry_ppsh41_drum;
    构造新的骑兵准星:Iron_Cavalry;
    warhorse_with_ppsh41_clip:cavalry_ppsh41_clip;ppsh41_clip_on_horse;
    当前目标:使bot会使用战马武器向敌人开火:套用Ha-Go,不会开火;
        当我添加武器为"LS120_Tower",AI为Ha-Go时,AI会开火并打死了敌人;
        当我添加武器为"ppsh41_drum_Pivot",AI为Ha-Go时,AI会开火并打死了敌人(但是此时的FireArms为"Vickers");
        当我添加武器为"ppsh41_drum_Pivot",AI为Ha-Go时,AI不会开火;(若不行,则是Weapon AI的问题)
        当我添加武器为"ppsh41_drum_Pivot",AI为Ha-Go时,AI会开火并打死了敌人;(Weapon AI是Vickers)
    cossack_cavalry:cossack_hat;cossack_hat_sp(宽型);cossack_cape(披风);cossack_sword(武器);cossack_sword_eq(装备);
    德军哥萨克(Cossack)需复制苏联军队独立为Soldier阵营(CossackSoldier,COSSACK_GER_0);苏军的哥萨克重载苏军即可;
    COSSACK_GER_i装备:Cossack_axis_engineer/Cossack_axis_rifleman/Cossack_axis_NCO/Cossack_axis_support/Cossack_axis_officer;Icon_cossack_sword;

- Swordfish仍然会导致跳出:删去...后期再加;

- 将含有"debree_dirt1A"的特效替换为烟雾特效:沙子的是"Em_richoSand1",替换为新的烟雾"Em_richoGround_Basic_smoke"(e_muz1_I.dds);
    时长控制:如何使特效持续的更久;使用"ObjectTemplate.timeToLive CRD_UNIFORM/5/7/0",特效会5-7秒才消失;
    但是这样一来,枪声事件会被覆盖,会失去枪声(参考"https://bfmods.com/mdt/scripting/CRD.html");
    timeToLive 太长会覆盖,"CRD_UNIFORM/3/5/0"时枪声正常;

- XWW2_Sisak(1944年3月29日-锡萨克):ED42有时会在保存瞬间报错闪退,有可能是地图的有的文件名和规定不一样(比如"StaticObjects.con"为"SPStaticObjects.con"),需要检查;
    skyttevern2_m1 无贴图;

- grep 匹配任意字段(可以匹配出"AABBCC"):
    ```grep -ri "AA.*CC" ./;```

- 实时的.con读取生成过程:在构造 wwii_aircraft_mod 时,wwii_aircraft_mod在地图中再生时也有出错提示,说明在其再生时也有读取定义文件的过程;

替换所有载具的"ObjectTemplate.setCrossHairType CHTCrossHair":用Python程序;

苏芬战争mod这两天更新了 相当于是单人bot补丁 但是是独立的mod包 依赖原来的苏芬战争mod
https://www.moddb.com/mods/finnwars-singleplayer
其rfa总是解压出错,后换BGA.exe解压不再出错;

苏芬战争地图包:In a nutshell: Finnwars is Winter War + Continuation War + Lapland war;
- 载入图:
    XWW2_FINNWAR_39(1939-1940):The Winter War Between Finland and USSR;
    XWW2_FINNWAR_44(1941—1944):The Continuation War Between Finland and USSR;
- XWW2_Battle_of_Ladoga:(Behind_the_enemy_lines);
- XWW2_Kollaa:(First_to_Fight)缺失 kkpesake,lumikasa2,jhauta_ps;
- 芬兰军队冬季战争装备:FinKitWinter:(FinWin_i);fin_winter_cap;头罩(fin_winter_head_cover);
    finw_engineer;finw_NCO;finw_officer;finw_rifleman;finw_support;
- XWW2_Olonets_Karelia(Olonets_Karelia):sb-2_autofly 更新为 fake_aircraft_ki21;
    fake_aircraft_bomb:自动丢下的航空炸弹 fake_bomb_engine(kkpesake2);
- XWW2_Raatteentie(Raatteentie):;
- XWW2_Ilomantsi(Storm_Over_Ilomantsi):;
- XWW2_Kota_Bharu:(1941.12.8,Malaysia,Kota Bharu)日军闪击马来亚;

#### 单人地图制作教程
苏芬战争单人版作者spisska推荐给我的教程:
https://cajunwolf.com/tutorials.html
https://cajunwolf.com/pathmapping_with_ed42.html

spisska(Creator):"Hi, in short, it consisted in two parts - pathfinding and coding. Coding is not that hard since you can take a look at other maps and just put coordinates and flags of your map. Pathfinding is harder, but here is good tutorial about how to make it: Cajunwolf.com"

### ➢ XWW2-FB-Version-0.12:

☑ 修正所有带枪战马:warhorse_with_gun_mod/warhorse_with_kar98k/warhorse_with_carcano/warhorse_with_mosin_nagant/warhorse_with_type99;
☑ 将新增的载具加入到maps:wwii_aircraft_mod的准星有问题;
☑ 新增"苏军哥萨克/冬季意大利"及地图"XWW2_Kharkov_Winter":ita_win_helmet;
☑ 西线海战地图"XWW2_North_Sea":俾斯麦号上换成YamatoDriverSoldierSpawn/YamatoSoldierSpawn后出生为德军不再是英军;
    ☸德国海军装备(GerNavyKit):navy_life_jacket_ger(GerNavy_i);
    ☸英国海军装备(BritNavyKit):navy_life_jacket_en(BritNavy_i);
    在 wwii_submarine_mod 前加一挺双联MG34(Stationary_triple_mg34/wwii_sub_mod_MG34_PCO);
☑ BG42 移植武器的操作姿势:
    "Kuk75erSeat"替换为"french75seat"(站姿);
    "B4howitzer_GunnerSeat"替换为"Pak40_Seat"(坐姿);
    "6in26cwtGunnerSeat"替换为"french75seat"(站姿);
    (Frz_Bus)"Frz_BusSeat"替换为"Pak40_Seat"(坐姿);
☑ 加入更多的反坦克武器:燃烧瓶/德军反坦克枪/苏军反坦克枪/盟军反坦克枪;Iron_ATGUN_ALL;
    burnning_bottel:```RfaPack.exe D:/BF1942/cache/bf1942 bf1942 D:/BF1942/Mods/XWWII/Archives/bf1942/game.rfa -u```;
    从"20mm_KwK_30_L55"(352)探索枪弹的有效性:直接从已有的"76mm_M1A1.con"复制改写有效;
    atgun_ger_pzb39:SPKIT_GER_ANTITANK_1/ICON_pzb39/SPKIT_GER_ANTITANK_1;
    atgun_so_ptrs:SPKIT_SO_ANTITANK_1/ICON_ptrs/SPKIT_SO_ANTITANK_1;
    atgun_en_boyes:SPKIT_ALLIES_ANTITANK_1/Icon_boyes/SPKIT_ALLIES_ANTITANK_1/FrE_ANTITANK(FrE_ANTITANK_1);
☑ 挡住AI的地图建筑/悬空地图建筑调整:XWW2_Battleaxe/XWW2_Bocage/XWW2_Hochwald_Forest/XWW2_Karelia_Night/XWW2_Songhu128/XWW2_Arras;
☑ 制作更多的模板扩展载具并加入地图:不要是已有mod中的;
    ☑ BG42的火车头可以开 wwii_amoured_train_transport(locomotive):可输运坦克;
        载具PCO在切换视角时跳出:可能是因为PCO的载具类型和原载具不对应;
        载具PCO使用瞬间跳出:可能是PCO编码混乱,直接不要编码(注掉"addPcoPosId");
        setVehicleType和主载具一样也不行(设作"Apc");
    ☑ FHSW柏林的小电车:wwii_city_tram(wwii_city_tram_M1)rail_tram_m1;
    ☑ 新的欧洲小轿车2款:CivModCar_MercedesSS1928;CivModCar_Cadillac1931;
    ☑ 运输船(可输运坦克):wwii_landing_ship(wwii_landing_ship_M1)No101Class_Landing_Ship_hull_m1;wwii_landing_ship_Ramp;
        载具的重量是关键参数(ObjectTemplate.mass),直接影响载具间的作用;
    ☑ 三号坦克/三突子裙板型号:StuGIIIG(StuGIIIG_Hull_M1);Panzer_III_Skirts(Panzer_III_M);
    ☑ 更正新加各种载具的Icon缩略图:Icon_landing_ship/Icon_Bismarck/Icon_MG_PCO;
☑ 背景音乐重制:
```
PS D:\BF1942\Rebuild_XWWII\RADVideo> .\bink.exe .\Stalingrad-1993-map.wav vehicle4.bik
PS D:\BF1942\Rebuild_XWWII\RADVideo> .\bink.exe .\Stalingrad-1993-menu.wav menu.bik
```
☑ 逐地图测试:"XWW2_Arden_Mountains"偶然的跳出;;;;
    给"bicycle_albelt"增加包裹,开始震动,质量增加十倍后震动减弱,但是还是存在;包裹作为"bicycle_pack"添加时不会震动;
    新增"Hungarian","Norwegian"语言;来自重返狼穴2的"BeingHit.wav"经GoldWave转化后(单16bit/44khz)有生效的;
☑ 大炮拖车(修改 vehicle_towed_cannon_mod):
    c7p_tractor:c7p_tractor_m1;
☑ 士兵携带的机枪和迫击炮(参考"30calkit"的"30calDeploy"生成"Deployed_M1919a4"-"M1919a4_Body_M1"-"M1919a4S_in_Hands"):
    ✍ MortarKit(美军的):"MortarDeploy"生成"Mortar"-"Mortar_in_Hands";
    ✍ ATAirMG34Kit:"ATAirMG34Deploy"生成"ATAirMG34"-"ATAirMG34_in_Hands",ATGUN_Public_Base_M1(icon_spkit_box.dds);
☑ 更多的Kit:德军冬装皮帽:ger_east_furcap;
    各种胡子:soldier_beard_1/soldier_beard_2(修改器-镜像(选轴)-再在修改器里点应用);
    同盟国通用背包(主要是早期盟军阵营):wwii_allies_backpack;
    将一些GameFront的贴图资源整合到mod中;
☑ 该版本最后一张新地图(XWW2_Bzura_River):1939年9月9日至同月19日;POL_AT_KIT_1;
☑ 制作武器展示图(类似FHWWII):更正各种最新添加武器的Icon缩略图;

Auf der Heide blüht ein kleines Blümelein
Und das heißt Erika.
Heiß von hunderttausend kleinen Bienelein wird umschwärmt Erika
denn ihr Herz ist voller Süßigkeit,
zarter Duft entströmt dem Blütenkleid.
小小的花儿开在荒野上,她的名字叫做艾莉卡
成千上万个小蜜蜂竞相飞向那艾莉卡
只因花芯中饱含着甜蜜 花瓣上散发着迷人的芬芳

☑ 小调整:调整"wz36_MOV"等移动火炮的移动速度("ATTEngine"更快);

---------------------------------------------
This is a new full-version, mainly improved:

- 14 new maps(Including the 8 maps mappack updated);

- About 30+ new weapons/vehicles added;

- Some effects/sounds/AI improved;

- Some known maps/weapons/vehicles bugs fixed;

----------------------------------------------
### 新地图

- XWW2_Linyee_Defence:第59军奉命驰援,1938年3月12日到达临沂北郊的沂河西岸,协同第40军实施反击,激战5昼夜,重创日军,迫其向莒县撤退;
    移植"苏芬战争mod"的固定反坦克枪到 XWW2:l39_crouch/stationary_l39;
- 手持旗帜:Tomahawk;(其Lod距离问题未解决:创建"HandFlagLodSelector");

制作IronSight的最佳方法(关键是用到复制时的"羽化功能"):
    1. 用圈型选区+左上角羽化=5~7复制中心的瞄具区域;
    2. 模糊其他区域;
    3. 制作Alpha通道,这样出来的效果不会有边沿的亮区;



- 摩托车:模仿BG42里的 Harley 摩托;BMW_R35:;

--------------------------------------------
### 联机方法
在 https://www.gametracker.com/search/bf1942/?sort=0&order=ASC&searchipp=50#search 查看living的服务器及其IP和端口号信息 然后在对应mod里找Add Server把IP和端口号输入 点Join就能进去了

-------------------------------------
### FHE Used Kits Names

game.setMapId "FHE"
game.setServerInfoIcon serverInfoFHR.dds

- 德军晚期:
game.setTeamSkin 1 FMGermanSoldier
game.setKit 1 0 German_AssaultSg44
game.setKit 1 1 German_GrenadierK98
game.setKit 1 2 German_GrenadierK98Faust100
game.setKit 1 3 German_GrenadierG43
game.setKit 1 4 4German_GrenadierK98Faust100

- 苏军晚期:
game.setTeamSkin 2 RussianSummerSoldier
game.setKit 2 0 Rus_CloseQuartersPPSorPPsh
game.setKit 2 1 2Rus_AssaultSVT40
game.setKit 2 2 3Rus_ATPTRS
game.setKit 2 3 4Rus_SupportDP1928
game.setKit 2 4 5Rus_EngineerNagant

- 美军:
game.setTeamSkin 2 USSoldier
game.setKit 2 0 Us_ClosequartersThompsonCS
game.setKit 2 1 Us_AssaultGarandCS
game.setKit 2 2 Us_ATBazookaCS
game.setKit 2 3 US_SupportBarCS
game.setKit 2 4 US_EngineerM1CarabineBangaloreCS

- 英军:
game.setTeamSkin 2 BritishSoldier
game.setKit 2 0 GB_SquadLeaderStenMk2Thompson
game.setKit 2 1 GB_Rifleman_No4
game.setKit 2 2 GB_ATPiat
game.setKit 2 3 GB_SupportBren
game.setKit 2 4 GB_EngineerWirecutters

- 日军:
game.setTeamSkin 1 JapaneseSoldier
game.setKit 1 0 Jap_Seaman
game.setKit 1 1 Jap_Seaman
game.setKit 1 2 2Jap_SeamanBou
game.setKit 1 3 3Jap_SeamanBou
game.setKit 1 4 4Jap_SeamanBou

--------------------------------------------------
### Talk 2022/12/25 Lv's Annual Conference

Minzhong Luo,Institute of Information Engineering,Chinese Academy of Sciences
Extend on BF1942:Techlonogy about Programming on WWII History
History and Programming,you must think I'm crazy... ...In the last talk,I've shared some developement expirience when I improved a WWII mod of BF1942,including the 3D modeling,scripts programming,textures making,and sounds editing,but I'll shared more new techlonogies and details for this.
I am a PhD from State Key Laboratory of Information Security, my major is Algorithmic Problems in Computing Algebraic Geometry.

https://www.moddb.com/mods/expirience-world-war-iiforgotten-battles/downloads/xww2forgotten-battles-v012

- 模板化的载具开发思想及其实践;
- 指令集化的AI(aiTemplate->aiTemplatePlugIn->ControlParameters);
- 自动化的载具生成程序;
- 景深感的机械瞄准及其实现;

----------------------------------------------
FHE singleplayers mappack

you should install bf1942 v1.61, FH v0.7, FHE v0.88 at first(make sure the origin version of BF1942 is already fully patched):
download FH at: https://www.moddb.com/mods/forgotten-hope-secret-weapon/downloads/forgotten-hope-1
download FHE at: https://www.bf-games.net/downloads/1852/fh-extended-client-088.html
How to use this mappack: take the map files into your "BF1942\Mods\FHE\archives\bf1942\levels";

战地1942模组开发教程的另一个镜像:http://85.214.226.169/mappingteam/index.html;
日语下载:ダウンロード;

应广大网友的强烈要求,现在释出可运行Bot地图的战国模组下载地址:https://pan.baidu.com/s/10Q0kFiYsLTpY40F7zLFnng 
提取码是本届世界杯梅西和C罗的进球数:0501

-------------------------------------------------
### more bg42/Finnwars maps(30)

- XWW2_Khalkin:蒙古vs日本,12th May 1939;马圈的重复问题,xww2的和bg42的不一样(horsebarn_m1);贴图缺失:Bunker_tarnnetz;

30岁、博士毕业、迷茫和顿悟并存;
知识和科研、爱和快乐、理想和现实都是相互矛盾的;
任何仪式、关系、头衔的改变都不能解决问题,问题还是存在的;
没人值得你一辈子依靠,除了你自己的 Logical mind + Persistence + Humility;

-----------------------------------------------------------
- 枪械开火烟雾的优化:更加喷射状(e_MuzzRifle/e_MuzzGun)新增 em_MuzzRifle;
    其中出现的问题,烟雾特效次数过多:通过以下数值的配合来调整,其中 intensity 的次数不要超过 timeToLive CRD_UNIFORM 的最长周期;"destBlendMode"控制了显示模式:透明或者其他;
```
ObjectTemplate.timeToLive CRD_UNIFORM/0.5/1/0
ObjectTemplate.intensity CRD_NONE/1/0/0
```

### 装甲列车(轻型)计划
- 调整铁轨的高度:不如调整火车"轮子Engine"的高度更高,因为铁轨过高太假;
    还是调整铁轨的高度,因为"轮子Engine"的高度低一点就会翻车,另外铁轨底座稍许不连贯都会导致车抖动,因此设一个光滑的长底座为Col;
- Light_Armoured_Train_Mod(修改自 BF1918 的 Icon_ArmouredTrainGunCar):Light_Armoured_Train_Mod_Body_M1;
    加了 Ehrhardt 的几个机枪位 Ehrhardt_SideMG3(Coop模式下无报错跳出:可修改"aiTemplate"和"setVehicleType"来修正);
- 在 XWW2_Manila 中替代铁路的简单高台公路模型:wwii_streetroad_very_long;
- 录一个"战地1942-哥萨克手中的波波沙冲锋枪"的视频:修改 ppsh41fire.wav,ppsh41firemono.wav;
    本次视频展示了哥萨克骑兵和装甲列车,视频里的机枪装甲列车是我从战地1918拿的模型(战地1918里的这款列车不可移动),然后通过100行代码实现的,这么少的代码量主要是因为我引用了之前写的火车Engine代码和其他载具的机枪位;
    接下来的计划开展的开发内容如下:
    1.更多各式各样的重型/轻型装甲列车,均在有Bot的地图;
    2.更多各式各样的堡垒/可摧毁建筑,均在有Bot的地图;
    3.可能引入西欧荷兰战役、西班牙内战、魏玛德国冲突、第一次苏波战争、意希战争等内容;

- 奇怪的问题:ED42失效了无法打开,卡死在了读取Objects那里,问题暂时还没找到;
    2023/02/01(Discussed with Songyaru):通过对比实验和Log文件是某个3D.SM文件的问题(是"wwii_railroad_very_long_noc.rs"文本混乱导致的);

战地1942的模组下经常有这种问题:"直接玩战地1/战地5不好吗?";不好,因为战地1942不是一款FPS游戏,而是一款编程游戏,丰富的Conscript语言接口,可以很方便地编写Python脚本进行二次开发,通过离散数学的知识构造复杂实时的战场机制、或者自行优化AI算法来改进Bots路径等等,自己制作模型/动作/贴图也可以极大程度自动化;总而言之,"被赐予快乐"和"自己创造快乐"的感觉是不一样的;

### 新殭屍先生(XWW2扩展地图之僵尸模式)

服饰模型(zombie_sir):zombie_qing_clothe_1/zombie_qing_clothe_2/zombie_qing_hat_1/zombie_qing_hat_2;
武器即爪子(zombie_hands):zombie_hands_lhs/zombie_hands_rhs;

阵营(ZombieSoldier):face_zombie1_h/face_zombie2_h/face_zombie3_h/Zombiemun_r/Zombiemov_r;还需补全身体部位的贴图(zombie_hand/zombiemouth/zombieeye)☑;

其他元素:贴黄纸(zombie_paper)☑/特色陵墓建筑/修正爪子的声音(zombie_hands.wav)☑/僵尸语音☑/尸王(载具,zombie_king(zombie_king_main/zombie_king_head,尸王"瓜尔佳.守寿")☑/ZombieEngine/人体材质=41)/飞行的蝙蝠(hooted_bats/hooted_bats1/hooted_bats_m1)☑;Light_Armoured_Train_China(train_sandbags_m1);

地图(XWW2_Tsing_East_Tomb,1928/07/12):(直鲁联军第三十五师,不久又扩编为第十四军,孙殿英任军长);<<世载堂杂忆>>整个盗墓行动历时八天,"自是年四月十五日至二十二日,以火药轰开陵道石门,搜获宝物而去".其中给这位连长印象最深的是挖掘慈禧的陵寝:"当时将棺盖揭开,见霞光满棺,兵士每人执一大电筒,光为之夺,众皆骇异.俯视棺中,西太后面貌如生,手指长白毛寸余."有几个士兵大喊起来,把枪架在棺材上瞄准慈禧的遗体,"防僵尸起而伤人";
    装备"zombie_kits":ZOMBIE_KIT_1;Icon_zombie_hands.dds/zombie_kit.dds;box_treasure;
    视频(BV1ie4y1N7Ez);

- zombie_mod 里单机bots路径正常可玩的地图:zomb_bridge/zomb_carrefour/zomb_labo_beta/zomb_Metro(地铁)/zomb_ruines/zomb_village_beta;

- 侧位机枪的火车厢(Light_Armoured_Train_Cart):引用"traincart_m1"
- 自动启动地图尝试:
    ```D:\BF1942\BF1942.exe +game XWWII +joinServer 127.0.0.1:14567```

带载具进入动作的FH衍生mod:https://www.moddb.com/mods/fhrmod/downloads/fhr-v018;

XWW2_Prome:反攻缅甸卑谬(Myanmar,May 2nd,1945).

- 实现新的载具之间的连接器 XWW2_SP_Puller:参考BF1918的"TrainPuller_Spawner"
    实现"CivModCar_Tractor":轿车拖拽大炮;发现并不能简单实现 除非给被拖拽载具另加 Engine;
    而如果按照原有的写法,被拖拽的大炮必须本身是可移动的那种才可以被拖走;

- 荷兰欧洲战场:军服(DCH_NAT_1)/轻坦(Tank_CTLS_4TAC)/有轨装甲车(Light_Armoured_Train_Holland);
    dch_native_support/dch_AT_NCO/dch_native_rifleman/dch_native_engineer(军服重载:GENERAL_DUTCH_NAT);钢盔:Dutch_Nat_Helmet;dutch_nat_cap;
    Tank_CTLS_4TAC:Tank_CTLS_4TAC_Hull_M1;Tank_CTLS_4TAC_Turret_M1;
    Light_Armoured_Train_Holland:Light_Armoured_Train_Holland_M1;Light_Armoured_Train_Wheels_M1;
        给"AWW2_TEST"增加火车测试轨道;
        Coop模式下使用机枪位无报错跳出:aiTemplate 的问题,换成"Stationary_Vickers";
    light_amoured_train_mod_Engine(轻轨装甲车引擎,隐形的):引用了"HorseBackSpringR"...;
    XWW2_Grebbeberg:人数一上去,相当卡的问题还是没解决(确定是人数的问题,40人时不再卡)(Invasion of Holland,1940);
    无paint纹理的小内存地图2张(修改自波卡基):
        XWW2_Eastern_Hebei:冀东区1942年春季反扫荡战役,在兴隆东北歼灭伪蒙骑兵20多人;

- 中国士兵语音部分替换☑;毛瑟手枪(单持/双持/连发)音效替换:c96gun.wav,c96gunmono.wav;

----------------------------------------------------------------
指标(8月/Luo负责的部分):
    1.在F2域上多变元二次方程组量子求解算法研究方面,完成MQ-to-SAT转化方法的初步实现;☑
    2.完成现有主流SAT求解器采用技术的复现;☑
    3.在F2域上多变元二次方程组量子求解算法研究方面,结合MQ问题实例,优化MQ-to-SAT转化方法,转换效率接近Bard-Courtois-Jefferson 2007中的结果;☑
    4.完成新型SAT求解器的经典环节设计,并初步完成强化学习技术的加入;☑

"瘦身计划"(减少一些重用地图里的材质细节图以减少内存占用):处理前,levels占用3.06GB;
    Textures套用已有地图,删ObjectLightmap文件夹内容;
    XWW2_Arras,XWW2_Battle_of_the_Bulge,XWW2_Battleaxe,XWW2_Coventry,XWW2_Der_Untergang,XWW2_Eindhoven,XWW2_El_Alamein,XWW2_Guadalcanal,XWW2_Iwo_Jima,XWW2_Kharkov,XWW2_Kursk,XWW2_Manila,XWW2_Nomonhan,XWW2_Saipan,XWW2_Stalingrad,XWW2_Taierzhuang,XWW2_Vilnius,XWW2_Wake;☑处理后,levels占用2.65GB;
    XWW2_Liberation_of_Caen;

- 加拿大载具涂装重载:Roundel/Markings;
- WWII中国战场:从满洲到华北武装的各种皮帽:
    - 中东路冲突:
        - 8月16日,苏军步兵两连、骑兵一连由苏境阿巴该图向扎兰诺尔中国阵地射击,双方战斗2小时,互有伤亡.午后2时30分,苏军步、骑、炮约一师兵力,由阿巴该图越境,向扎兰诺尔站进攻,炮击东北军阵地,双方激战5小时,苏军始退.根据当时胪膑县县长齐肇豫电称:"俄军此次越境,据闻意在破坏扎站铁桥、断绝交通".
        - 8月19日,苏军攻陷绥滨县城.8月20日早6时,苏军用铁甲列车运兵200余名,向梁忠甲部骑兵十团进攻,战斗1小时左右苏军退去.8月23日发生密山战斗.8月25日,苏军步骑兵四百余名,在扎贲诺尔驻军四十三团阵地右前沿约千米处构筑工事.
    - 20年代的苏军(Russian20s):SOVIET20S_i;SOVIET20S_Coat(GENERAL_Russian20s/Russian-E20s_officer.tga);
    - 东北军(ChinaENA):CHINAENA_i;CHINAENA_Hat_furo;CHINAENA_Hat_furc;CHINAENA_Hat_furn(wb_broad_caps_b);
        (CHINAENA_officer/CHINAENA_NCO/CHINAENA_rifleman/CHINAENA_engineer)
    - XWW2_Suibing(XWW2_Battle_of_Ladoga):Kit_mp18_with_drum;xww2_gun_tape;厕所 BAs_Boomer(须平整地面否则会移动);重载脸部:吴京/邓超/郑恺;
    - XWW2_Lubin:BG42中的塔叫"o_pagoda_m1";(suburbhouse_3_closed_m1->xww2_china_city_building_2_m1)(citymesh1_closed_m1->mb_china_house_s3_m1)(eu_fence_m1->mb_native_village_short_wall_m1);
       cccp_budyonny_hat_opened/cccp_budyonny_hat_closed(对比 piippalakki) 改小;新增 SOVIET20S_Hat;

### Blender UV 贴图

- 流程:新建贴图,选图像,模型点面对到图像区域即可,导出后再手动.rs里填图像即可;
    mp18_band:由"xww2_gun_tape"修改;


### 伪蒙战役

- XWW2_Hongertu:1936年8月2至4日西北蒙汉防共自治军司令王道一部从商都出发攻打红格尔图,王道一部发动几次进攻均未攻下村庄.4日下午,傅作义赴集宁,命彭毓斌部增援,反击向红格尔图、土牧尔台进犯的西北蒙汉防共自治军王道一部2000余人,歼灭过半.王道一逃回商都大本营,被日军枪毙.
    MengjiangSoldier:MENGJ_i;MENGJ_Hat_Uni;MENGJ_Hat_Peo;MENGJ_Hat_Ofc;GNERAL_MENGJ;(黄渤/孙红雷/陈凯歌)
    "他们喊的不是"乌拉",而是уралан(乌德拉),卡尔梅语(蒙古族的一支)前进的意思."乌拉"是ура."
    (mengj_officer/mengj_rifile/mengj_support)

- 手持旗帜的骑兵 warhorse_with_flag:(cavalry_flag_mengj)手部的姿势语句:
    ```
    ObjectTemplate.addSkeletonIK Bip01_R_Hand 0.045/0.1/0.025 0/180/90
    ObjectTemplate.AddSkeletonIK string x(+:靠后)/y(+:没有变化)/z(+:向右) x/y/z
    argument 1:Bip01_L_Foot, Bip01_L_Hand, Bip01_R_Foot, Bip01_R_Hand
    argument 2:-0.033/0.573/-0.174, -0.05/0.0/-0.95,...
    argument 3:-30/80/90, -30/90/90, -80/-60/50, -80/-90/0,...
    ```

### 地图裁剪工作
继续做地图的size裁剪,引用公有的Texures:XWW2_Aachen/XWW2_Arden_Mountains/XWW2_Bloody_Ridge/XWW2_Bocage/XWW2_Fornebu/XWW2_Grebbeberg/XWW2_Hannut/XWW2_Ichi-go/XWW2_Juno_Nan_Green_Sector/XWW2_Kamenets_Podolskiy/XWW2_Khalkin/XWW2_Market_Garden/XWW2_Raatteentie/XWW2_Rostov/XWW2_Sisak/XWW2_Songhu128/XWW2_Tokyo226/XWW2_Villers_Bocage/XWW2_Zitadelle/XWW2_Nanking/XWW2_Vistula_River/XWW2_Barbarossa/XWW2_Crimea/XWW2_Milne_Bay/XWW2_Dog_Green_Sector/XWW2_Salamaua/XWW2_Bzura_River/XWW2_Volga/XWW2_Volturno/XWW2_St_Mere_Eglise/XWW2_Ortona/XWW2_Caen/XWW2_Linyee_Defence/XWW2_Kanchatzu/XWW2_Pegasus_Bridge/XWW2_Rabaul/XWW2_Waldhambach/XWW2_Kendari/XWW2_Coral_Sea/XWW2_Olonets_Karelia;
common_tx = "texture\Market_Garden_Textures\Tx";

### 苏波战争(华沙战役)

- PolKit20s:PolKit20s_i;PolKit20s_hat_sq;PolKit20s_hat_win;PolKit20s_helmet;ChauchatM1915(自制:ChauchatM1915_main/ChauchatM1915_mag/Iron_ChauchatM1915/Icon_ChauchatM1915/Chauchat_mono);
    PolKit20s_helmet:PolKit20s_Eagle_logo;(PolKit20s_officer/PolKit20s_support/PolKit20s_rifile)
    - Charron的机枪口调整(加了Ehrhardt的封闭机枪窗口);
XWW2_Leoncin(1920/08/10):wwii_streetroad_very_long 平坦化修正;

- XWW2_Jiangqiao(1931年11月7日,江桥抗战):;

- 苏军蒙古族狙击手(SPKIT_SO_Mong_sniper):"SPKIT_SO_Mong_sniper.dds";Russ_ScoutHelm_cover(sniper_cover);"Iron_sniper.tga";

### 新阵营:希腊
 
GreeceSoldier:GreeceKit/Greek_i(GENERAL_GREECE);Greek_helmet;Greek_officer_hat;Greek_nco_hat;
    Greek_officer/Greek_support/Greek_rifile;
武器:Stationary_MGANON(Stationary_MGANON_main/Stationary_MGANON_Gun)/smg_ANON(Icon_smg_ANON)/grenade_ANON;
坦克:VickersMkETB:VickersMkETB_Hull_M1(50)/VickersMkETB_Turret_M1(50);
火炮:pindus_ANON(pindus_ANON_gun_m1->pindus_ANON_cannon);

- XWW2_Kalamas_Line:XWW2加入希腊后,高频反馈是BG42已经有希腊了,为啥还要步人后尘?事实上XWW2的希腊模块相对于BG42增加了更多的希腊军帽、希腊的维克斯MKE-B型改装坦克、希腊的帕帕多斯机枪、希腊的索普斯冲锋枪、希腊的尤尼西亚步兵炮以及西塔隆手雷;
- XWW2_Thermopylae:反坦克兵"Greek_1_AT"("GREEK_AT_KIT_1.dds");

### 新阵营:斯洛伐克

SlovakSoldier:https://www.ww2-weapons.com/slovak-armed-forces;
SlovakKit:Slovak_i(GENERAL_SLOVAK);Slovak_helmet;Slovak_officer_hat;Slovak_nco_hat;
    Slovak_officer/Slovak_support/Slovak_rifile/Slovak_AT;
坦克:LTVz40:LTVz40_Hull_M1(50)/LTVz40_Turret_M1(50);

- XWW2_Cieszyn:1939年斯洛伐克武装夺回波兰切欣地区(icon_flag_slovak);

- 八路军冬季帽子(era_winter_cap):Karvalakki_rus/Karvalakki_rus_off;CERA_4_win;
- Stationary_Maxim_NOG(精细的马克沁/俯卧姿势):Stationary_Maxim_NOG_main;模仿"Deployed_M1919a4",先构造枪体"Stationary_Maxim_NOG_Sd"(模仿"M1919a4Sd");枪声:"Stationary_Maxim_NOG.wav";

### Pick from FXKR

- CivModCar_Coupe/CivModCar_Buick1926:;
- wwii_MG_Bunker_dsim(简易双机枪地堡):lod_wwii_MG_Bunker_dsim_Cockpit 的添加部分决定了"内视框"是否随着上下左右摆动而相对活动;
    堡垒内机枪音效若隐若现的问题:移植FX的"Coaxial_DT",解决;