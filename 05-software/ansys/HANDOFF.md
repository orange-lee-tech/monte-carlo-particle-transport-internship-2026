# ANSYS / Fluent 工程交接手册

> **适用对象：** 第一次接手本项目、对现有 ANSYS/Fluent 文件关系不熟悉的新人。  
> **软件基线：** ANSYS Workbench / Fluent 2021 R1。  
> **交接目标：** 让接手者不需要重新“考古”，能够在 30–60 分钟内知道项目在做什么、现在做到哪、哪些东西已经验证、哪些坑不要重复踩，以及下一步应该从哪里继续。  
> **当前交接状态：** 实习现场工作已结束；正式几何的 Share Topology 主导故障已经定位到局部问题管路/接口，并通过删除问题管后的 A/B 验证使 Share 能够继续完成。当前下一技术节点是重新识别长管端面、修复 Capping/流体 Region，随后完成 Volume Mesh，并在新版 Cell Zone 上恢复既有 FLUKA→Fluent UDF 热源加载链。

---

# 0. 先看这一页：新人 30 分钟快速入门

如果你是第一次接手，不要一上来重算，也不要先改 Fluent 参数。

按下面顺序：

1. **先读本文件。**
2. 再读：
   - `01-daily-log/2026-08-20.md`
   - `01-daily-log/2026-08-27.md`
   - `01-daily-log/2026-07-22.md`
   - `01-daily-log/2026-07-27.md`
3. 看代码目录：
   - `fluka_to_c_translation/`
4. 看旧 ANSYS 算例说明：
   - `06-cases/ansys-cases/package-run-record.md`
5. 确认你手里的正式几何/Workbench 工程是不是最新版本。
6. **不要默认沿用旧 zone 编号。**
7. 当前优先任务不是重做 FLUKA 数据，而是：
   ```text
   修复/确认 Capping
   → 创建正确流体 Region
   → Volume Mesh
   → 进入 Solver
   → 重新识别铜质热源 Cell Zone
   → 加载既有 UDF
   → 做功率积分
   → 再开始正式求解
   ```

如果你只记住一句话：

> **这个项目已经不是“学 Fluent”阶段，而是“维护一条 FLUKA → Fluent 的工程计算链”；任何改动都必须先分清它属于 CAD、Surface Mesh、Share、Region、Volume Mesh、Solver 还是 UDF 数据层。**

---

# 1. 项目到底在做什么

本项目服务于高功率准直器/靶相关热工计算。

上游通过 FLUKA 得到空间能量沉积分布，下游使用 Fluent 计算体积热源作用下的温度场，再进一步可向 Mechanical 传递温度做热应力分析。

主链条：

```text
FLUKA 粒子输运
→ 空间能量沉积 .29
→ Python 转换
→ C 三维数组 .c/.h
→ Fluent UDF
→ 铜质准直器体积热源
→ 流固耦合换热
→ 温度场
→ Mechanical 热应力（后续）
```

项目有两条长期主线：

### A 线：数据接口

```text
FLUKA .29
→ C 数组
→ UDF
→ Fluent source term
```

这条线已经基本跑通，并做过功率积分、坐标映射、逐体素诊断。

### B 线：正式几何与流体域

```text
正式 CAD
→ Surface Mesh
→ Share Topology
→ Capping / Fluid Region
→ Volume Mesh
→ Solver
```

这条线是实习结束时尚未彻底收尾的部分。

---

# 2. 已经完成到什么程度

## 2.1 已经真正跑通过的内容

旧模型中已经完成过完整闭环：

```text
FLUKA .29
→ heat_deposition.c / .h
→ beam_1mrad_offset_2mm_source_udf.c
→ 编译 libudf1
→ Fluent 识别 ENERGY_PLAN
→ 挂接到铜质 source 区
→ 功率积分
→ 稳态迭代
→ 温度场
```

旧模型曾得到可复现的工程基线，说明**数据链和 UDF 链不是当前主要风险点**。

## 2.2 当前正式几何的最新状态

正式几何经过多轮 CAD/Share 排障后：

- 旧版复杂几何长期在 Share Topology 处失败；
- 通过 TUI 诊断将问题定位到局部管—主体接口；
- 新版几何中：
  - `wall.5` 与主体约有 7.98 万个 inter-zone intersecting faces；
  - `wall.6` 与主体约有 6.95 万个；
  - `wall.7` 与主体为 0；
  - self-intersection = 0；
  - duplicate faces = 0；
- 删除可疑问题管后，Share 能够继续完成 Join/Intersect 和 region computation；
- 不再出现此前稳定复现的：
  - `Mesh topology corrupted`
  - `SIGSEGV`

因此：

> **当前 CAD/Share 的主导故障已经得到较强 A/B 验证。**

但 Share 通过后又暴露：

```text
Capping 中旧 zone 选择失效
→ 长细管端面无法被旧任务自动重新识别
→ 视觉上像“长管被截断/端口封死”
```

所以当前工作点在 Capping/Region，不在 FLUKA 数据层。

---

# 3. 软件环境和最基本约束

## 3.1 软件版本

核心环境：

- ANSYS Workbench 2021
- Fluent 2021 R1
- SpaceClaim 2021 R1
- Fluent Meshing：Watertight Geometry Workflow

本项目历史工作基于这一代版本完成。

**不要在不留备份的情况下直接用新版本升级原工程。**

## 3.2 Fluent 模式

历史有效工作中使用：

- 3D
- Double Precision
- 并行运行

UDF 也已经按并行环境做过诊断适配。

## 3.3 文件管理原则

不要把工作文件随意塞回 Workbench 自动管理目录。

历史上曾因为 case/data 文件名和路径管理不当导致：

```text
case 读取成功
data 未匹配
→ 温度结果异常
```

建议：

```text
独立工作目录
+ 简单英文文件名
+ case/data 基础名一致
+ 不使用多个额外点号
+ 不覆盖正确检查点
```

---

# 4. 仓库里最重要的资料在哪里

## 4.1 日志

`01-daily-log/`

重点：

- `2026-07-21.md`：FLUKA .29 → C 数组重构
- `2026-07-22.md`：第一次跑通 UDF → Fluent 闭环
- `2026-07-23 .md`：UDF 编译/加载与模型验证过程
- `2026-07-27.md`：功率恢复率、逐体素诊断、18.422% 缺口解释
- `2026-08-20.md`：正式几何 Share Topology 深度排障
- `2026-08-27.md`：新版 x_t、问题管定位、删除后 Share 通过

## 4.2 FLUKA → C → UDF

`fluka_to_c_translation/`

这里是活跃代码资产，不是普通笔记目录。

关键内容：

```text
input/
  beam_1mrad_offset_2mm.29
  beam_2mrad_offset_1p4mm.29

output/
  *_heat_deposition.c
  *_heat_deposition.h

udf/
  UDF 相关源码与说明
```

## 4.3 ANSYS 历史算例记录

`06-cases/ansys-cases/`

重点：

- `package-run-record.md`
- `fluent-2026-07-09-settings.md`

它们用于理解师姐/课题组旧模型是什么，不代表当前正式几何的所有参数都应该原样照搬。

## 4.4 ANSYS 学习与交接

`05-software/ansys/`

本文件应作为后续 ANSYS 接手的主入口。

---

# 5. 旧模型的物理与求解设置基线

旧 case 中确认过：

- Pressure-Based
- Steady
- Energy = On
- Gravity = On
- Realizable k-ε
- Scalable Wall Function
- 冷却水入口：
  - 速度约 `9 m/s`
  - 温度约 `20 ℃`
  - 水力直径 `12 mm`
- 固体材料涉及：
  - copper
  - steel
  - aluminum
- 流体：
  - water-liquid

注意：

> 这些是**旧模型的回归锚点**，不是新版正式几何的自动真值。

尤其是 zone 名称、zone ID、接口数量必须重新确认。

---

# 6. Fluent Meshing：当前推荐基线

正式几何在 Surface Mesh 阶段，历史上相对稳定的参数组合为：

```text
Face Size                 = 0.001 m
Minimum Size              = 0.001 m
Growth Rate               = 1.2
Size Function             = Curvature & Proximity
Curvature Normal Angle    = 12°
Cells Per Gap             = 1
Feature Angle             = 40°
Check Self Intersections  = yes
Quality Improve           = yes
```

Share Topology 历史推荐基线：

```text
Maximum Gap Distance             = 0
Join Normal Angle                = 40°
Initial Relative Join Tolerance  = 0.1
Join Attempts                    = 3
Tolerance Increment              = 0.05
Method                           = Join and Intersect
```

## 6.1 明确已经证明“不值得继续试”的东西

不要再优先尝试：

- `0.5 mm` 全局/局部强加密；
- `0.25 mm`；
- Force Share 全局硬顶；
- 整模型反复 Share 碰运气；
- 用更密网格掩盖 CAD 拓扑问题。

历史结果已经证明：

> **更细不等于更稳；复杂接触区加密后反而更容易触发 Join/Remesh 冲突。**

---

# 7. Share Topology 出错时怎么诊断

不要只看 GUI 的“失败”。

先判断失败属于哪一层。

## 7.1 第一步：列出 zone

```text
/boundary/manage/list
```

用途：

- 获得 zone ID；
- 中文/乱码名称时不要手输横杠名字；
- 后续统一使用 ID。

只读，不修改网格。

## 7.2 查两个 zone 是否真正相交

```text
/boundary/clear-marked-faces
/boundary/mark-face-intersection
```

输入：

```text
(ID1 ID2)
```

然后统计：

```scheme
(tgapi-util-count-marked-faces '(ID1 ID2))
(tgapi-util-count-marked-faces '(ID1))
(tgapi-util-count-marked-faces '(ID2))
```

用途：

> 判断两个独立表面之间是否存在大面积真实 inter-zone intersection。

## 7.3 查单体表面自己有没有坏

```scheme
(tgapi-util-mark-self-intersecting-faces '(ID1 ID2) #t)
(tgapi-util-count-marked-faces '(ID1 ID2))
```

如果为 0：

> 不能把问题归咎于 Surface Mesh 自己折叠。

## 7.4 查重复面

```scheme
(tgapi-util-mark-duplicate-faces '(ID1 ID2))
(tgapi-util-count-marked-faces '(ID1 ID2))
```

## 7.5 看 Fluent 准备 Join 哪些面

```text
/boundary/remesh/mark-join-faces
```

按提示分别输入两个 zone。

这个命令是 Mark/Preview，**不要误当成真正 Join。**

## 7.6 图形化高亮

```text
/display/set/colors/highlight-color
red

/display/set-grid/marked? yes
```

再在 GUI：

```text
显示 → 网格 → 面
```

只选目标两个 zone。

这样可以直接看：

- 是整条长接触带；
- 端部；
- 环形接触；
- 随机坏点；
- 还是三体交线。

---

# 8. 怎么解释 Share 的典型报错

## 8.1 `Dihedral limit violations or self-intersections found, undoing join`

含义：

> Fluent 尝试 Join 后发现局部重构会产生不接受的角度/自交，因此撤销。

这不等于原始 Surface Mesh 一定有 self-intersection。

## 8.2 `non-manifold configuration`

这是更严重的拓扑信号。

常见来源：

- CAD 实体穿模；
- 多个面/体在一条线或一个点形成非法连接；
- 共面/重叠接口处理后形成多重邻接；
- 极小薄片面；
- 管端和主体交界过于复杂。

## 8.3 `node insertion failed`

通常已经不是普通参数问题。

如果继续发展到：

```text
Mesh topology corrupted
SIGSEGV
```

应该立刻停止。

> **不要继续在当前已被破坏的内存网格上诊断。恢复 Share 前基线。**

---

# 9. 当前已定位过的问题管逻辑

新版几何中曾得到：

```text
主体 ↔ wall.5   ≈ 79829 intersecting faces
主体 ↔ wall.6   ≈ 69515 intersecting faces
主体 ↔ wall.7   = 0
```

并且：

```text
self-intersection = 0
duplicate faces   = 0
```

因此推断：

> 问题属于特定 CAD 接口，不是全局 Surface Mesh 参数。

之后删除可疑问题管，再跑 Share：

- 能够继续 Join/Intersect；
- 能够 computing regions；
- 不再出现此前硬崩溃。

这是目前最强的工程证据。

---

# 10. SpaceClaim / CAD 层应该怎样检查

如果 Share 再次出现局部几万级 intersection，不要先调 Fluent。

优先回 CAD。

## 10.1 最值得查的几何问题

- 实体互穿 / volumetric interference；
- 共面重合但未形成公共拓扑；
- 管子与铜主体 Boolean 合并错误；
- 多根管意外属于同一个连续 Solid；
- 极短边；
- 极小面；
- 管端环形面；
- 三体交线；
- 螺旋管贴槽处局部穿透。

## 10.2 SolidWorks 可以做的预检查

如果原 CAD 在 SolidWorks：

先跑：

```text
Evaluate → Interference Detection
```

建议两轮：

1. 不把 coincidence 当 interference；
2. 把 coincidence 当 interference。

这样可以区分：

- 真正体积穿模；
- 纯共面重合。

再跑：

```text
Evaluate → Check
```

重点看：

- invalid face；
- invalid edge；
- short edge。

## 10.3 SpaceClaim 的历史教训

如果一根管已经和主体 Boolean 成同一个 Solid：

> 原本的内部接触面可能已经被 Boolean 吃掉。

这时普通 Detach 并不能凭空恢复内部面。

曾经验证过一种独立管重建方法：

```text
选择管腔内壁 Ri = 6 mm
→ Copy Faces
→ Thicken 1.5 mm
→ No Merge
→ 得到独立空心管 Solid
```

尺寸：

```text
Ri = 6.0 mm
Ro = 7.5 mm
t  = 1.5 mm
```

这种方法适合三维螺旋管，因为直接继承原内壁轨迹，不需要重新画中心线。

---

# 11. 当前 Capping / 长细管问题

Share 通过后，长细管在显示上看起来：

- 被截断；
- 端口被封死。

但 Surface Mesh 的 Bounding Box 仍然保留约：

```text
z_min ≈ -2.713 m
```

说明长管在 CAD/Surface Mesh 阶段并没有真正丢失。

真正的错误提示是：

```text
Enclose Fluid Regions (Capping):
The previously selected zones (...) could not be detected using bounding box information.
```

当前判断：

> 修改 CAD、重新 Surface Mesh、重新 Share 后，原 Capping 任务保存的旧 Face Zone 已失效。

因此下一步不要重新画长管，先：

1. `/boundary/manage/list`
2. 找出当前长管真实 Face Zone；
3. 单独显示验证；
4. 重新选 inlet / outlet 端面；
5. 重新建立 Capping。

如果重新 Surface Mesh，建议在高级选项考虑：

```text
Invoke Zone Separation by Angle? = yes
```

因为 Fluent 已提示模型较大，未自动为 capping 分离 zone。

---

# 12. Volume Mesh 前的验收标准

只有下面条件满足，才应该进入 Volume Mesh：

- Share 已完成；
- 不再有 `Mesh topology corrupted`；
- 不再有 unresolved non-manifold 硬错误；
- inlet/outlet 端面可明确识别；
- 流体区域是连续的；
- 创建 Region 后，流体/固体数量符合物理直觉；
- 没有明显多出来的 dead region；
- 长管路径完整；
- 管腔没有被错误封死；
- 铜体和管壁没有体积穿模。

不要因为 Workflow 图标变绿就跳过几何检查。

---

# 13. 进入 Solver 后第一件事不是迭代

正式几何第一次进入 Solver 时，先做“身份核验”。

至少核对：

- Cell Zone 数量；
- 哪个是水；
- 哪个是铜准直器；
- 哪个是钢管；
- 是否还有铝结构；
- inlet/outlet 类型；
- 流固接口；
- 材料；
- Energy 是否开启。

**绝对不要默认新版模型仍然是：**

```text
zone 10 = source
```

旧编号只属于旧模型。

---

# 14. FLUKA → Fluent 数据加载链

这条线已经做过，接手者不要重新从零写。

## 14.1 数据网格

当前主要工况：

```text
beam_1mrad_offset_2mm
```

FLUKA scoring mesh：

```text
X: -10 cm ~ 10 cm, 20 bins
Y: -10 cm ~ 10 cm, 20 bins
Z: -14 cm ~ 14 cm, 28 bins
Total = 11200 voxels
Voxel = 1 cm³
```

数组顺序：

```text
X fastest
Y second
Z slowest
```

C 数组：

```c
heat_deposition[ix][iy][iz]
```

## 14.2 Python 转换做什么

Python 只负责：

- 从 `.29` 数据区读取；
- 检查数量；
- 重排为三维数组；
- 生成 `.c/.h`。

它**不做束流电流归一化**。

## 14.3 UDF 做什么

主 UDF：

```text
beam_1mrad_offset_2mm_source_udf.c
```

逻辑：

```text
读取 Fluent cell centroid
→ m 转 cm
→ 判断是否在 FLUKA scoring box
→ 计算 ix / iy / iz
→ 读取 heat_deposition
→ 乘物理换算系数
→ 返回 W/m³
```

正式函数名历史上使用：

```text
ENERGY_PLAN
```

## 14.4 5 mA 归一化

历史 UDF 中使用：

```c
#define BEAM_CURRENT_A 5.0e-3
#define M_TO_CM 100.0
#define FLUKA_TO_W_M3 (BEAM_CURRENT_A * 1.0e15)
```

但交接者必须知道：

> 5 mA 与 FLUKA 输出单位来源属于需要可追溯记录的物理输入，不应该仅仅因为代码里写了就永远默认正确。

---

# 15. UDF 编译注意事项

Fluent 2021 环境曾遇到：

```text
UnicodeDecodeError: 'gbk' codec can't decode byte ...
```

根因：

> UDF C 源码包含 UTF-8 中文注释，Fluent 构建脚本按 GBK 读取。

解决方法：

- UDF 源码尽量纯 ASCII；
- 不写中文注释；
- 删除失败构建产生的旧 libudf 目录；
- 重新 Build / Load。

旧链已经证明：

```text
数组 .c/.h
+ source_udf.c
→ Fluent 内置 clang
→ libudf.dll
→ Load
```

可成功。

---

# 16. UDF 挂接以后必须做功率诊断

“能加载函数”不等于“物理正确”。

每次换正式几何后，必须重新积分：

```text
q''' [W/m³] × cell volume [m³]
```

得到实际加载功率。

旧模型中历史诊断值：

```text
FLUKA full-box power       ≈ 46.799777 kW
zones 8–11 diagnostic map ≈ 38.178315 kW
old copper source load    ≈ 37.243157 kW
```

这些只用于回归，不是新版模型目标值。

---

# 17. 18.422% 功率缺口的正确解释

旧模型曾发现：

```text
FLUKA full-box             46.799777 kW
Fluent mapped zones 8–11  38.178315 kW
gap                         8.621462 kW
gap fraction               18.422014%
```

这个 18.422% **不是简单漏掉 18% 单元**。

zone 10 曾达到：

```text
Mapped cell fraction   ≈ 99.997847%
Mapped volume fraction ≈ 99.999962%
```

逐体素诊断显示：

- 1370 empty voxels；
- 7508 underfilled voxels；
- 2466 overfilled voxels；
- empty voxel power 只占约 0.0615%。

真正原因：

> FLUKA 规则体素与 Fluent 实际几何覆盖不完全一致，同时“按 Fluent 单元质心把整个 cell 归到一个体素”的算法会产生欠填充和过填充。

所以：

> **不要用一个全局补偿系数强行把功率拉回 46.8 kW。**

新版几何必须重新算自己的功率平衡。

---

# 18. Solver 阶段的旧模型参考

旧模型曾运行到约 610 iter。

得到过：

```text
source Tmax ≈ 209.99 °C
fluid Tmax  ≈ 24.90 °C
```

质量流量：

```text
inlet + outlet ≈ 0
```

能量残差可稳定到很低，但 continuity 并没有达到特别严格的数值收敛标准。

因此旧结果的正确定位：

> **工程基线，不是最终物理真值。**

---

# 19. 不要重复踩的坑

## 19.1 不要把“计算能跑”当“物理正确”

必须分别验证：

- 单位；
- 坐标；
- 束流电流；
- 热源位置；
- 功率；
- 流量；
- 材料；
- 边界；
- 结果。

## 19.2 不要看见 marked faces 就说是坏三角形

`mark-face-intersection` 的 marked faces 可能是两个 zone 之间正常/异常的几何相交关系。

要配合：

- self-intersection；
- duplicate faces；
- 图形位置；
- A/B 对照。

## 19.3 不要在已经 topology corrupted 的内存状态继续修

恢复到 Share 前 mesh。

## 19.4 不要因为 GUI 参数相同就认为网格完全等价

Fluent Guided Workflow 的内部状态和局部离散可能变化。

要看：

- nodes；
- faces；
- zones；
- Share 结果。

## 19.5 不要一开始就局部加到 0.5 mm

历史验证是负收益。

## 19.6 不要默认中文 zone 名可稳定追踪

导入后经常乱码、横杠化。

关键诊断统一用 zone ID。

---

# 20. 新人推荐工作方法：一次只解决一个层级

如果出现问题，先问：

```text
这是 CAD 问题？
Surface Mesh 问题？
Share 问题？
Region/Capping 问题？
Volume Mesh 问题？
Solver 问题？
UDF/数据问题？
```

只在一个层级内做 A/B。

推荐模式：

```text
保留 baseline
→ 改一个变量
→ 运行
→ 记录量化结果
→ 判断
→ 再决定下一步
```

不要同时：

- 换 CAD；
- 改网格；
- 改 Share；
- 改边界；
- 改 UDF。

否则无法知道是谁起作用。

---

# 21. 和 AI 协作：怎样问最有效

本项目非常适合用 AI 做“第二导师/排障助手”，但前提是提问信息完整。

## 21.1 最好的提问格式

每次尽量给：

1. **你现在在哪个软件/模块**
2. **你想完成什么**
3. **你刚刚做了什么**
4. **出现什么输出/报错**
5. **附截图**
6. **附终端完整输出**
7. **明确希望 AI 一次只给一个动作**

推荐模板：

```text
当前软件：Fluent Meshing 2021 R1
当前阶段：Share Topology 前 Surface Mesh 已完成
当前目标：定位 A 与 B 为什么 Join 失败

我刚做了：
1. ...
2. ...

终端输出见附件。
截图见附件。

要求：
- 一次只给我一个或一组连续的安全操作；
- 每个 TUI 指令注明“只读/标记/会修改网格”；
- 不要先让我全局重算；
- 如果判断需要回 CAD，请明确证据和停止条件。
```

## 21.2 Fluent 排障时特别要求 AI 区分

让 AI 明确标注：

```text
只读
仅标记
改变显示
修改网格
破坏性操作
需要备份
```

这非常重要。

## 21.3 截图怎么发

最好一张截图包含：

- 左侧 Workflow；
- 当前参数面板；
- 几何窗口；
- 控制台最后 20–50 行。

这样 AI 不需要反复猜你在哪一步。

## 21.4 终端输出怎么发

不要只发最后一句报错。

Share / UDF 编译时建议保存完整输出 TXT。

因为真正根因通常出现在报错前几十行。

## 21.5 不确定时让 AI 先查日志

推荐直接说：

```text
先查 GitHub 中 8.20、8.27 日志和现有 ANSYS 交接，不要凭通用经验覆盖我们的历史验证结果。
```

这会显著减少重复试错。

## 21.6 AI 说法和实际界面不一致怎么办

优先相信你自己的软件界面。

直接反馈：

```text
我这里没有你说的按钮/zone/菜单。
这是当前截图。
不要继续假设，基于当前版本重新给路径。
```

---

# 22. GitHub 怎么管理

仓库：

```text
monte-carlo-particle-transport-internship-2026
```

## 22.1 什么写入 GitHub

应该长期保存：

- 终版日志；
- UDF 源码；
- Python 转换脚本；
- 参数基线；
- 关键 TUI；
- A/B 验证结果；
- 交接；
- 可复现结论。

不建议直接长期堆：

- 临时截图；
- 几 GB Workbench 自动文件；
- 临时 mesh；
- 用户账号/服务器/VPN 信息。

## 22.2 推荐路径

```text
01-daily-log/
    日志

05-software/ansys/
    软件方法、交接、操作规范

06-cases/ansys-cases/
    特定算例的设置和运行记录

fluka_to_c_translation/
    可执行代码和数据接口
```

## 22.3 Commit 建议

每次只提交一个主题。

例如：

```text
docs: add Fluent handoff guide
fix: correct UDF coordinate mapping
docs: record Share Topology A/B test
feat: add voxel power diagnostic
```

不要一个 commit 同时混：

- 日志；
- 大量代码；
- 文档重构；
- 删除文件。

## 22.4 不覆盖历史证据

终版日志原则上只读。

新的理解写：

- 新日志；
- 新交接；
- 新技术说明。

不要为了“现在看起来更整洁”而回头改掉历史过程。

---

# 23. 新对话交接模板

如果 AI 对话过长，要新开对话，推荐：

```text
这是新的阶段对话。请先基于以下交接摘要继续工作：

1. 当前主线：
2. 已完成：
3. 仓库已更新：
4. 当前待办：
5. 禁止修改：
6. 本轮目标：

要求：
- 先阅读最近日志和 ANSYS 交接；
- 不重复已验证失败路线；
- 一次只推进一个技术分叉。
```

---

# 24. 后续战略规划

## 阶段 A：先把正式几何变成可求解模型

目标：

```text
正确 Capping
→ 正确 fluid region
→ Volume Mesh
```

验收：

- 长管完整；
- inlet/outlet 正确；
- water region 连通；
- no fatal topology issue；
- volume mesh 可生成。

这是当前第一优先级。

## 阶段 B：恢复 FLUKA 热源

目标：

```text
识别新版铜 Cell Zone
→ 编译/加载 ENERGY_PLAN
→ 功率积分
→ 检查空间映射
```

验收：

- 热源只挂目标铜体；
- 功率积分合理；
- 不盲目追旧 37.243 kW；
- 新几何自己的 power balance 能解释。

## 阶段 C：建立正式热工基线

目标：

- 稳态求解；
- 质量守恒；
- 能量残差；
- 温度平台；
- 最大温度位置；
- 冷却性能；
- 与论文/旧模型做回归，不做“调参贴结果”。

## 阶段 D：Mechanical（后续）

只有 Fluent 热工结果可信后：

```text
Fluent temperature
→ Imported Body Temperature
→ Static Structural
→ stress / deformation
```

---

# 25. 当前下一步，精确到操作层

接手者现在不要先动 UDF。

当前最小下一步：

```text
1. 打开 Share 已通过的 Fluent Meshing 状态
2. 执行 /boundary/manage/list
3. 找出两根长细管的当前 Face Zone
4. 单独显示
5. 确认它们是否完整存在
6. 删除/更新旧 Capping 任务中的失效 zone
7. 重新选择真实 inlet / outlet 端面
8. 创建 fluid region
9. 检查 region 数量与物理身份
10. 再生成 Volume Mesh
```

做到第 9 步前，不需要碰 FLUKA UDF。

---

# 26. 给接手者的最后提醒

这个项目最危险的不是某个按钮不会点，而是：

> **软件链长、历史文件多、每一层都能“看起来算成功”，但物理意义可能已经错了。**

最可靠的方法始终是：

```text
先确定当前层级
→ 保存基线
→ 单变量试验
→ 用数量/功率/zone ID 做证据
→ 再进入下一层
```

如果遇到新问题，优先留下：

- 截图；
- 完整终端输出；
- 当前参数；
- mesh/zone 统计；
- 操作前后差异。

这样无论是人接手，还是 AI 接手，都能继续推进，而不用重新猜。

---

# 27. 一句话交接

> **当前工程已经完成 FLUKA→Fluent UDF 数据链验证，也基本定位并绕过了正式几何 Share Topology 的主导故障；下一位接手者应从“重新识别长管端面并修复 Capping/流体 Region”开始，完成 Volume Mesh 后，再把现成的 ENERGY_PLAN 热源链重新挂到新版铜质 Cell Zone 上，并重新做功率守恒验证。**
