# ANSYS / Fluent 工程交接手册（执行版）

> 软件基线：ANSYS Workbench / SpaceClaim / Fluent 2021 R1  
> 适用对象：第一次接手本项目、需要直接继续工程计算的人  
> 交接原则：**先看状态机，再动软件；一次只推进一个关口；每个关口都有验收条件。**

---

# 0. 先看这两页：项目不是一条线，而是 A/B 两条线汇合

## 0.1 为什么要拆成 A/B 两条线

2026-08-17，正式几何在 Fluent Meshing 的 Share Topology 阶段长期失败。与此同时，工作人员当时首先要求确认新 FLUKA 数据能否进入 Fluent/UDF，而不是等待完整模型可用后再做数据接口。

因此工程被明确拆成两条互不阻塞的路线：

| 路线 | 任务 | 当前状态 | 下一关 |
|---|---|---|---|
| **A 线：数据导入** | 新 FLUKA 热沉积数据 → Fluent UDF | **A1–A3 已闭环** | A4：正式 CAD/FLUKA 三维坐标映射 |
| **B 线：模型导入** | 新 CAD → Fluent Meshing → 流体域 → 体网格 | **Share 主阻塞已突破** | 重新识别端面 → Capping → Region → Volume Mesh |

两条线不是两个独立项目，而是在下面这个节点重新汇合：

```text
A线：fort.30 → RAW30_ENERGY_SOURCE ─────┐
                                       ├→ 新铜体 Cell Zone → 坐标标定 → 热源积分 → Solver
B线：CAD → Surface → Share → Region → Volume Mesh ─┘
```

**关键依赖关系：A4 必须等待 B 线给出稳定、可识别的新 Cell Zone。**

所以接手者现在不应重新研究 fort.30 文件格式，也不应先调热源；应先把 B 线推进到 Volume Mesh，再恢复 A4。

## 0.2 当前工程停点

实习结束时，B 线最难的阻塞——Share Topology——已经通过 TUI 定位和删除可疑管路的 A/B 试验获得强证据并实质通过。当前不是“继续修 Share”，而是：

```text
【现在从这里开始】
重新识别长管端面
→ 重建 Capping
→ Create / Update Regions
→ 检查 fluid / solid / dead / void
→ Volume Mesh
→ 进入 Solver
→ 识别新版铜质 Cell Zone
→ 恢复 A4：CAD ↔ FLUKA 坐标映射
→ 挂 RAW30_ENERGY_SOURCE
→ 功率积分与热斑位置验证
→ 正式求解
```

如果只记住一句话：

> **A 线的数据已经等模型；B 线刚刚越过 Share，当前任务是把几何真正变成可求解的体网格，然后让 A、B 两线汇合。**

---

# 1. 接手后的第一小时：不要“理解项目”，直接按状态机核验

## 1.1 打开工程后先做四件事

1. 确认使用的是 ANSYS / Fluent 2021 R1 环境，不在原工程上直接升级版本。
2. 打开当前交付的正式几何 / Workbench 工程，确认当前 Fluent Meshing 工作流为 **Watertight Geometry**。
3. 不点击 `Update All`，不重新生成所有网格。
4. 先执行：

```text
/boundary/manage/list
```

这一步只读。目的是确认**当前 Face Zone 名称和 ID**，因为每次重新 Surface Mesh / Share 后 Zone 都可能重新编号。

## 1.2 第一小时的成功标准

你必须回答清楚四个问题：

- 当前长细管对应哪些 Face Zone？
- 两个真实开口端面是否是独立 Face Zone？
- 当前 Share 之后 Region 状态是什么？
- 当前是否仍有 `topology corrupted / SIGSEGV / unresolved non-manifold`？

如果这四件事还没搞清楚，不要进入 Volume Mesh，也不要碰 UDF。

---

# 2. A 线：新 FLUKA 数据导入——已经做到哪里

## 2.1 A 线不是旧 `.29 → C 数组` 路线

旧模型的 `.29 → heat_deposition.c/.h → ENERGY_PLAN` 链路已用于建立方法基线和验证 UDF 机制，但**新正式模型的主数据路线已经升级**。

新路线是：

```text
FLUKA 原始 target_4collimator001_fort.30
→ Fortran sequential record 解析
→ 34,560,000 个 float32
→ Fluent UDF static memory
→ 5 mA 单位归一化
→ CAD/FLUKA 坐标映射
→ DEFINE_SOURCE: RAW30_ENERGY_SOURCE
```

不要把旧 `.29` 工况的 20×20×28 数据当成新模型正式输入。

## 2.2 A1：大文件进入 Fluent UDF 内存——完成

曾先用约 178 MiB 的 `.30.lis` 做纯加载测试，验证：

- 整文件可被 UDF 读取；
- static memory 跨 On-Demand 调用保持；
- Hash 二次检查一致；
- 内存可正常释放。

这一步的意义是证明：**Fluent/UDF 能承载该量级的数据，模型失败与数据读取可以解耦。**

## 2.3 A2：正式数据源从 `.lis` 改为原始 `fort.30`——完成

最终确认 `.30.lis` 只有 `14,786,930` 个完整数值，只覆盖理论矩阵的 **42.786256%**，且与原始矩阵前缀逐项一致，因此它只是被截断的 ASCII 输出，不能用于正式热源。

原始 `target_4collimator001_fort.30` 已验证：

- 文件大小：`138,240,238 bytes`；
- little-endian；
- 4-byte record marker；
- 共 3 个 Fortran sequential record；
- 第 3 个 record payload：`138,240,000 bytes`；
- 恰好等于 `300 × 300 × 384 × 4 bytes`；
- 总数据量：`34,560,000` 个 float32；
- Python 与 Fluent UDF 的 count / sum / max / index / hash 一致。

正式数据网格：

```text
X: -15 ~ +15 cm, 300 bins
Y: -15 ~ +15 cm, 300 bins
Z: 25 ~ 63.4 cm, 384 bins
Voxel: 1 mm × 1 mm × 1 mm
```

## 2.4 A3：5 mA 归一化与全域功率——完成

采用项目既有换算：

```text
q''' [W/m³] = FLUKA raw × 5×10^12
```

Fluent 内已验证：

```text
RAW Sum             = 6.207064450995
Integrated power    = 31,035.322255 W = 31.035322255 kW
Peak RAW            = 7.168727734097e-06
Peak source         = 3.584363867049e+07 W/m³
Peak index          = (131,159,12)  [0-based]
Peak voxel center   = (-1.85, +0.95, 26.25) cm  [FLUKA]
```

这些数值是后续 A4 联调时的**硬回归锚点**。

## 2.5 A4：正式 CAD ↔ FLUKA 三维坐标变换——等待 B 线

已知线索：

- CAD 束流轴为全局 `+X`；
- FLUKA 束流轴为 `+Z`；
- 曾建立轴向工作假设：`CAD +X → FLUKA +Z`；
- FLUKA 轴向范围 250–634 mm，中点 442 mm，因此候选关系为：

```text
Z_FLUKA(mm) = X_CAD(mm) + 442
```

但横向 `CAD Y/Z ↔ FLUKA X/Y` 的交换关系和正负号**尚未最终锁定**。

因此禁止把“同轴直接映射”写死成生产版本。A4 必须在新版体网格生成后，通过几何特征、峰值体素位置和功率回收联合验证。

---

# 3. B 线：新模型导入——为什么耗时、已经解决到哪

## 3.1 B 线的“导入成功”不是打开 CAD 文件

对于本项目，B 线真正的成功标准是：

```text
CAD 能打开
≠ Fluent 能生成 Surface Mesh
≠ Share Topology 正确
≠ 流体域可封闭
≠ Volume Mesh 可生成
```

只有能够得到物理身份明确、无致命拓扑错误的流体/固体 Region 并生成体网格，才算模型真正进入可求解状态。

## 3.2 主要故障链

新 STEP / `.x_t` 几何在 Share Topology 阶段曾长期出现：

```text
non-manifold configuration
Dihedral limit violations or self-intersections
node insertion failed
Mesh topology corrupted
SIGSEGV
```

早期曾尝试：

- 18° → 12°；
- Minimum Size 1 mm → 0.5 mm；
- Gap Distance 调整；
- Join Only / Join and Intersect；
- 局部强加密。

结论：**继续加密不是主解法，0.5 mm 局部加密反而使失败扩散。**

## 3.3 CAD 根因

SpaceClaim 横截面、测量和 Boolean 试验确认部分冷却管与铜体存在真实体积穿模。

管径参数：

```text
OD = 15 mm
ID = 12 mm
wall = 1.5 mm
```

单管修复形成“两刀法”：

```text
第一刀：删除 Cu ∩ pipe wall
第二刀：删除 Cu ∩ pipe lumen
```

目的：

- 铜与钢管壁不能占同一体积；
- Ø12 mm 冷却水通道必须贯通；
- 管外壁—铜槽形成可识别的真实接触界面。

进一步还发现部分三维螺旋管被错误并入同一个连续 Solid，说明机械 CAD 不能直接等价为 CFD 几何。

## 3.4 TUI 证据：问题是局部接口，不是全局网格

新版模型中曾测得：

```text
主体 ↔ wall.5  ≈ 79,829 inter-zone intersecting faces
主体 ↔ wall.6  ≈ 69,515 inter-zone intersecting faces
主体 ↔ wall.7  = 0
self-intersection = 0
duplicate faces   = 0
```

这意味着 `wall.5 / wall.6` 自己并没有折叠坏掉；问题集中在它们与主体之间的几何关系。

## 3.5 8 月 27 日 A/B 验证：Share 主阻塞被突破

删除已定位的可疑管路，其他工作流尽量保持不变后重新生成 Surface Mesh / Share：

- Share 能继续完成 Intersect / region computation；
- 不再触发此前稳定复现的 `Mesh topology corrupted / SIGSEGV`。

这不能证明被删管路是唯一故障源，但已构成很强的因果证据：**该管—主体接口至少是主导故障源之一。**

至此，B 线工作重点从 Share 根因诊断转移到 Capping / Region。

---

# 4. 现在就做：B 线执行卡 B5——Capping → Region → Volume Mesh

> 本节是当前真正的接手起点。一次只做一小步，得到正常结果再继续。

## B5-1：重新列出当前 Face Zone

Fluent Meshing 控制台：

```text
/boundary/manage/list
```

属性：**只读**。

正常结果：列出当前所有 face zones、ID、type、face count。

你要做的事：记录与两根长细管、入口/出口端面有关的当前 Zone ID。

异常：如果仍沿用旧名称/旧 ID 做选择，后续 Capping 很可能再次失败。

## B5-2：逐个显示疑似长管 Zone

GUI：

```text
显示 → 网格 → 面
```

一次只选一个 zone，确认：

- 长管主体是否从准直器一直延伸到远端；
- 是否只是显示/Zone 分割导致“看起来被截断”；
- 开口圆面是否独立可选。

历史证据：Surface Mesh Bounding Box 曾仍保留约 `z_min = -2.713 m`，说明长管并未在 CAD/Surface Mesh 阶段真正消失。

## B5-3：重建入口/出口 Capping

不要复用旧 `velo-inlet_1` / Capping 保存的 zone 选择。

原因：删除实体、重新 Surface Mesh、Share 后，Face Zone 已重新编号/分裂。

操作：

1. 删除或重设旧 Capping 任务的失效选择；
2. 重新选择当前真实开口端面；
3. 分别建立 inlet / outlet cap；
4. 立即单独显示新 cap，确认它只封住真实开口，不横切长管。

如果端面没有独立成 zone，需要回 Surface Mesh 的 zone separation 处理，而不是硬选整根管壁。

## B5-4：Create / Update Regions

完成 Capping 后创建/更新 Region。

验收必须逐项检查：

- 冷却水域是连续 fluid region；
- 铜体、钢管等仍为 solid；
- 没有把实际流体变成 dead；
- 没有数量异常的 void/dead region；
- inlet/outlet 与目标 fluid region 相连。

如果 Region 身份不符合物理直觉，**停止，不生成 Volume Mesh**。

## B5-5：Volume Mesh

只有 B5-4 通过后才生成 Volume Mesh。

成功标准不是“任务图标变绿”，而是：

- 无 `Mesh topology corrupted`；
- 无 unresolved non-manifold；
- water region 连通；
- 长管腔体贯通；
- 铜体与管壁不存在体积穿模；
- Cell Zone 数量与材料结构相符。

完成后保存一个明确命名的检查点，再进入 Solver。

---

# 5. B 线完成后立即恢复 A4：两线汇合执行卡

## A4-1：进入 Solver 后先做 Cell Zone 身份核验

第一件事不是初始化，也不是迭代。

确认：

- water fluid Cell Zone；
- copper collimator Cell Zone；
- steel pipe Cell Zone；
- 其他固体结构；
- inlet / outlet；
- 流固接口。

**禁止沿用旧模型 `zone 10 = source` 的假设。**

## A4-2：加载新数据路线，不回退到旧 `.29` 主路线

新模型应围绕：

```text
target_4collimator001_fort.30
→ RAW30_ENERGY_SOURCE
```

旧 `ENERGY_PLAN` / `.29 → C` 链只作为旧模型回归参照。

## A4-3：锁定三维坐标变换

建议按照“一个候选变换 → 三个证据”验证：

1. **轴向范围证据**：CAD 束流轴 `+X` 应映射 FLUKA `+Z`；
2. **热斑位置证据**：FLUKA 峰值 voxel center = `(-1.85,+0.95,26.25) cm`；
3. **功率证据**：完整 scoring box 的 5 mA 总沉积功率 = `31.035322255 kW`。

不要只凭“热斑看起来在铜体里”接受坐标关系。

## A4-4：挂接 Source 后做功率积分

先积分：

```text
Σ(q''' × cell volume)
```

然后检查：

- 热源是否只挂目标铜体；
- 热斑是否位于物理合理位置；
- 实际几何截取后的功率与 31.035 kW 的差异能否由几何覆盖解释；
- 是否存在明显坐标轴/正负号错误。

通过后才进入正式温度场求解。

---

# 6. 当前推荐网格与 Share 基线

Surface Mesh 历史稳定基线：

```text
Face Size                 = 0.001 m   [核心局部]
Minimum Size              = 0.001 m
Growth Rate               = 1.2
Size Function             = Curvature & Proximity
Curvature Normal Angle    = 12°（历史最好）
Cells Per Gap             = 1
Feature Angle             = 40°
Check Self Intersections  = yes
Quality Improve           = yes
```

Share 历史有效基线：

```text
Maximum Gap Distance             = 0
Join Normal Angle                = 40°
Initial Relative Join Tolerance  = 0.1
Join Attempts                    = 3
Tolerance Increment              = 0.05
Method                           = Join and Intersect
```

不要优先重复：

- 全局/局部 0.5 mm 强加密；
- 0.25 mm；
- Force Share 全局硬顶；
- 在 topology corrupted 的内存状态继续修。

---

# 7. Fluent Meshing 诊断命令：看什么、会不会改网格

| 目的 | 命令 | 风险 |
|---|---|---|
| 提高日志详细度 | `/report/verbosity 2` | 安全 |
| 列出 Zone | `/boundary/manage/list` | 只读 |
| 清除标记 | `/boundary/clear-marked-faces` | 只清标记 |
| 查两个 Zone 的真实三角面相交 | `/boundary/mark-face-intersection` | 只标记 |
| 统计 marked faces | `(tgapi-util-count-marked-faces '(ID1 ID2))` | 只读 |
| 查 self-intersection | `(tgapi-util-mark-self-intersecting-faces '(ID1 ID2) #t)` | 只标记 |
| 查 duplicate | `(tgapi-util-mark-duplicate-faces '(ID1 ID2))` | 只标记 |
| 预览 Join 候选 | `/boundary/remesh/mark-join-faces` | 只标记 |
| 真正 Join / Remesh | Join / Remesh 操作 | **修改网格** |

遇到下列链条时停止调 Fluent，回 CAD：

```text
数万级 inter-zone intersection
→ non-manifold
→ node insertion failed
→ Mesh topology corrupted / SIGSEGV
```

---

# 8. 旧模型 `.29 → C → ENERGY_PLAN` 应该怎样使用

旧链并没有废弃，它的角色是**方法和求解回归基线**，不是新模型正式数据输入。

旧模型已完成：

```text
.29
→ heat_deposition.c/.h
→ ENERGY_PLAN
→ libudf1
→ copper source zone
→ 功率积分
→ 稳态求解
```

历史回归量：

```text
FLUKA full-box power       ≈ 46.799777 kW
zones 8–11 diagnostic map ≈ 38.178315 kW
old copper source load    ≈ 37.243157 kW
source Tmax               ≈ 209.99 °C
fluid Tmax                ≈ 24.90 °C
```

18.422% 功率缺口已证明主要来自规则 voxel 与 Fluent 实际几何覆盖差异及 cell-centroid 映射欠/过填充，不是简单“漏了 18% 单元”。

**新模型不要强行回归到这些功率数值。**

---

# 9. Solver 正式求解前验收表

只有以下内容全部通过，才开始正式迭代：

- [ ] B 线：Capping 正确；
- [ ] B 线：fluid region 连通；
- [ ] B 线：Volume Mesh 完成且无致命拓扑错误；
- [ ] Cell Zone 身份明确；
- [ ] 材料分配正确；
- [ ] Energy = On；
- [ ] inlet / outlet 设置正确；
- [ ] A4 三维坐标变换有独立证据；
- [ ] RAW30_ENERGY_SOURCE 只挂目标铜体；
- [ ] 功率积分结果可解释；
- [ ] 热斑空间位置合理；
- [ ] 保存进入正式 Solver 前检查点。

旧模型参考设置（仅回归，不自动照搬）：

- Pressure-Based；
- Steady；
- Realizable k-ε；
- Scalable Wall Function；
- 冷却水入口约 9 m/s、20 ℃；
- hydraulic diameter 12 mm；
- solid: copper / steel / aluminum；
- fluid: water-liquid。

---

# 10. 常见错误 → 应去哪个层级修

| 现象 | 优先层级 | 第一动作 |
|---|---|---|
| `.x_t` 打不开 | CAD 兼容 | 核对 Parasolid 版本，不先怪 Fluent |
| Surface Mesh 大量 self-intersection | CAD / Surface | 查小面、残余 Body、旧 Share |
| 两 Zone inter-zone intersection 数万 | CAD 接口 | 查实体穿模 / 共面重合 |
| `non-manifold` + `node insertion failed` | CAD 拓扑 | 停止继续加密 |
| `Mesh topology corrupted / SIGSEGV` | 当前网格已破坏 | 恢复基线，不继续诊断 |
| Capping 找不到原 Zone | Workflow 身份变化 | `/boundary/manage/list` 重新识别 |
| 长管看似被截断 | Face Zone / 显示 | 先单独显示 zone 与 bounding box |
| UDF 编译 GBK/Unicode 错误 | UDF 源码 | 源码改纯 ASCII，清旧 libudf |
| 热源能挂但功率不对 | A4 坐标/覆盖 | 先积分和热斑定位，不先调 Solver |
| 温度场异常 | 数据/边界/Case-Data | 先核验身份与输入，不用收敛掩盖错误 |

---

# 11. 与 AI 协作：让它像工程副手，而不是泛化教程

推荐每轮只给一个主问题：

```text
当前软件：Fluent Meshing 2021 R1
当前路线：B 线
当前关口：B5-2 长管 Face Zone 识别
上一动作：/boundary/manage/list
当前输出：粘贴完整终端 + 截图
本轮目标：只确认哪两个 zone 是长管/端面

要求：
1. 一次只给一个主操作；
2. 每条 TUI 注明只读/标记/修改网格；
3. 不改变已验证基线；
4. 若根因属于 CAD，明确停止 Fluent 调参；
5. 按“看到什么 → 输入什么 → 正常 → 异常”回答。
```

关键原则：**把 A/B 路线、当前关口、上一动作写在提问开头。**

---

# 12. GitHub 中怎么找证据

优先阅读：

```text
01-daily-log/2026-08-17.md  # A/B 正式拆线；A1-A3 闭环
01-daily-log/2026-08-18.md  # B线 CAD 穿模与两刀法
01-daily-log/2026-08-20.md  # Local Join / TUI 深度诊断
01-daily-log/2026-08-27.md  # 删除问题管 A/B 验证；Share 通过；Capping 新停点
01-daily-log/2026-07-22.md  # 旧 .29/UDF/Solver 回归链
01-daily-log/2026-07-27.md  # 旧模型功率/voxel 诊断
```

代码/数据入口：

```text
fluka_to_c_translation/
10-handoff/ansys-fluent/programs/
10-handoff/ansys-fluent/data/
```

当前执行入口：

```text
10-handoff/ansys-fluent/EXECUTION_RUNBOOK.md
10-handoff/ansys-fluent/NEXT_STEPS_CHECKLIST.md
10-handoff/ansys-fluent/TUI_QUICK_REFERENCE.md
```

---

# 13. 最终交接：接手者下一次坐到工作机前应该做什么

只执行下面这一串，不扩展任务：

```text
1. 打开当前 Share 后 Fluent Meshing 状态
2. /boundary/manage/list
3. 逐个显示长管候选 Face Zone
4. 确认真正 inlet / outlet 开口面
5. 重建 Capping
6. Create / Update Regions
7. 验收 water fluid region 连通
8. 生成 Volume Mesh
9. 保存检查点
10. 进入 Solver，重新识别 copper Cell Zone
11. 恢复 A4 坐标标定
12. 加载 RAW30_ENERGY_SOURCE
13. 功率积分 + 热斑位置验证
14. 通过后才开始正式迭代
```

> **不要再从 `.lis`、旧 `.29`、0.5 mm 网格加密、全局 Force Share 这些已经走完或否定的路线重新开始。**
