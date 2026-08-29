# ANSYS / Fluent 现场执行手册

> 用途：接手者坐到工作机前直接照做。  
> 当前总策略：**先 B 线完成体网格，再恢复 A4 数据-模型联调。**

# -1. P0：资产预检

开始执行前先确认：

1. 当前 Share 后的 CAD / Workbench / Fluent Meshing 工程检查点存在；
2. `target_4collimator001_fort.30` 存在；
3. 已验证的新 RAW30 UDF C 源码存在，且包含 `RAW30_ENERGY_SOURCE`。

当前 GitHub 保存了验证结论和旧回归资产，但**不包含正式 fort.30 / 当前大型工程文件，且仓库审计未找到新 RAW30 UDF C 源码**。

处理原则：

- 大型工程与原始数据：从单位工程存储 / 工作机恢复；
- RAW30 UDF：优先找回原实现并进入版本管理；
- 不根据交接 Markdown 临时重写一份再视为“原代码”；
- 不用旧 `.29 → ENERGY_PLAN` 替代新正式 A 线。

# 0. 总状态机

```text
A线（已完成 A1-A3）
fort.30 → 34.56M float32 → 5 mA → UDF memory
                                   │
                                   └── A4 等待：CAD/FLUKA 坐标标定

B线（当前执行）
CAD → Surface Mesh → Share → Capping → Region → Volume Mesh
                         ↑已突破      ↑现在从这里继续

汇合
Volume Mesh → copper Cell Zone → A4 → RAW30_ENERGY_SOURCE
→ 功率积分 → 热斑位置检查 → Solver
```

# 1. B5-1：确认当前 Face Zone

**操作**

```text
/boundary/manage/list
```

**风险**：只读。

**你要记录**

- 两根长细管相关 Face Zone ID；
- 入口/出口圆形端面 Face Zone ID；
- 当前 wall / zone 数量。

**正常**：能列出所有 zone。  
**异常**：仍想用旧 zone 名或旧 ID —— 停止，先重新识别。

# 2. B5-2：确认长管真的还在

GUI：`显示 → 网格 → 面`。

一次只显示一个候选 zone。

**正常**

- 长管从准直器延伸到远端；
- 开口端面可定位；
- 只是 zone 分裂导致视觉上像截断。

**证据锚点**：历史 Surface Mesh bounding box 仍到约 `z_min=-2.713 m`。

**异常**

- 真正缺失整段几何：回 CAD/导入文件；
- 仅端面无法单独选择：处理 zone separation，不重画整根管。

# 3. B5-3：重建 Capping

旧 Capping / `velo-inlet_1` 保存的 face-zone 身份已经失效，**不要复用旧选择**。

操作：

1. 清除旧 Capping 的失效选择；
2. 选当前真实入口端面；
3. 建 inlet cap；
4. 选真实出口端面；
5. 建 outlet cap；
6. 分别单独显示新 cap。

**正常**：cap 只封开口。  
**异常**：cap 横切管壁/整根管被选中 —— 停止，重新做端面 zone separation。

# 4. B5-4：Create / Update Regions

**必须确认**

- water = 连续 fluid region；
- copper / steel = solid；
- inlet/outlet 连到同一目标 fluid region；
- dead / void 数量符合物理直觉。

如果任何一项不对，**不要生成 Volume Mesh**。

# 5. B5-5：Volume Mesh

只有 Region 验收通过才做。

**通过标准**

- 无 `Mesh topology corrupted`；
- 无 unresolved `non-manifold`；
- 水域连续；
- 管腔贯通；
- Cell Zone 数量合理。

通过后立即保存检查点。

# 6. A4-1：进入 Solver 后识别新版 Cell Zone

第一件事不是初始化。

确认：water / copper / steel / 其他 solid / inlet / outlet / interfaces。

**禁止**直接沿用旧 `zone 10 = source`。

# 7. A4-2：恢复新正式热源路线

```text
target_4collimator001_fort.30
→ RAW30_ENERGY_SOURCE
```

不要把旧 `.29 → ENERGY_PLAN` 当新模型正式输入。

上游固定锚点：

```text
300×300×384
34,560,000 float32
voxel = 1 mm³
5 mA full-box power = 31.035322255 kW
peak source = 3.584363867049e+07 W/m³
peak voxel center = (-1.85,+0.95,26.25) cm
```

# 8. A4-3：坐标标定

已知：

```text
CAD beam axis: +X
FLUKA beam axis: +Z
候选轴向关系：Z_FLUKA(mm) = X_CAD(mm) + 442
```

横向交换/符号尚未锁定。

每个候选坐标变换必须同时通过：

1. 几何轴向范围；
2. 峰值位置；
3. 功率积分。

只看温度图“像不像”不能作为坐标正确证据。

# 9. A4-4：挂 Source 后先积分，不先迭代

计算：

```text
Σ(q''' × cell volume)
```

检查：

- source 只在 copper；
- 热斑位置合理；
- 实际几何功率与 31.035 kW 的差异可由几何截取解释。

三项通过后才进入 Solver 正式迭代。

# 10. 出现这些现象就停

| 现象 | 动作 |
|---|---|
| 数万级 inter-zone intersection | 回 CAD 查穿模/重合 |
| `non-manifold` + `node insertion failed` | 不加密，回几何 |
| `Mesh topology corrupted` / `SIGSEGV` | 恢复基线 |
| Capping 找不到 zone | 重列 `/boundary/manage/list` |
| Region 身份错误 | 停在 Region，不做 Volume Mesh |
| 热斑方向明显错误 | 回 A4 坐标变换 |
| 功率明显不合理 | 先查挂接区/坐标/单位，不调收敛 |

# 11. 已经走过、不要重新试的路

- `.30.lis` 作为正式数据源；
- 0.5 mm / 0.25 mm 盲目加密；
- 全局 Force Share 硬顶；
- topology corrupted 后继续诊断；
- 新模型复用旧 zone ID；
- 用旧 `.29` 功率强行校准新模型。
