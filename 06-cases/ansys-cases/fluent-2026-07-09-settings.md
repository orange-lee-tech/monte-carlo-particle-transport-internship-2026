# Fluent 设置与复现记录（2026-07-09）

## 1. 对象

师姐 Ansys Workbench 文件包中的 A 系统 `Fluid Flow (Fluent)`。

阶段目标：读取已有 case/data，识别模型设置，核对已有结果，补齐 UDF 后完成短迭代复现。

## 2. 读取情况

Fluent 读取已有文件时，反复出现过如下 journal / report 设置警告：

```text
Error: state/object/set-state:Rules not found for object type path: /Report/RunInformationSettings
Error Object: ()
```

当前判断：该问题更像是 Fluent 恢复报告/运行信息设置时的兼容或旧环境残留问题。判断 case/data 是否成功读入时，不以该红字为唯一依据，而以 `source` 区域最大温度能否恢复到约 `131 ℃` 为准。

## 3. General / Models

| 项目 | 内容 |
|---|---|
| Solver Type | Pressure-Based |
| Velocity Formulation | Absolute |
| Time | Steady |
| Gravity | On；X=0，Y=-9.81 m/s²，Z=0 |
| Multiphase | Off |
| Energy | On |
| Viscous | Realizable k-epsilon，Scalable Wall Function |
| Radiation | Off |
| Heat Exchanger | Off |
| Species | Off |
| Discrete Phase | Off |
| Solidification & Melting | Off |

当前判断：该 Fluent 案例不是 VOF 两相瞬态模型，而是稳态单相冷却换热 + 固体导热 + 流固界面传热模型。

## 4. Materials

| 材料 | 类型 | Density | Cp | Thermal Conductivity | Viscosity |
|---|---|---:|---:|---:|---:|
| water-liquid | fluid | 998.2 kg/m³ | 4182 J/(kg·K) | 0.6 W/(m·K) | 未完整读取 |
| copper | solid | 8940 kg/m³ | 381 J/(kg·K) | 387.6 W/(m·K) | - |

其余材料包括 `air`、`aluminum`、`steel`。

## 5. Boundary Conditions

| 边界 | 类型 | 关键设置 |
|---|---|---|
| inlet | velocity-inlet | 速度 9 m/s；入口温度 20 ℃；湍流强度 3.76%；水力直径 12 mm；初始表压 0 Pa |
| outlet | outflow | Flow Rate Weighting = 1 |
| interface | 多个 interface / mesh interface | 用于不同区域之间数据传递或流固/固固接触换热 |
| wall | 存在 | 详细壁面设置后续需要按结构方案继续检查 |

## 6. Cell Zone Conditions

| Zone | Type | Material | Source Terms | 当前判断 |
|---|---|---|---|---|
| fluid | fluid | water-liquid | 未作为热源区 | 冷却水流体区域 |
| solid | solid | steel | 未勾选 | 结构/冷却管或支撑相关固体区域 |
| source | solid | copper | 已勾选 | 铜准直器主体或主要受热区 |
| pbk | solid | aluminum | 未勾选 | 可能为屏蔽块/辅助结构，需结合几何命名确认 |

## 7. UDF 热源项

`source` 区域中确认存在能量体热源项：

| 项目 | 内容 |
|---|---|
| Cell Zone | `source` |
| Type | solid |
| Material | copper |
| Number of Energy sources | 1 |
| 能量源项单位 | W/m³ |
| 原 case 中观察到的 UDF | `ENERGY_FLUH::libudf1` / 后续报错与加载中出现 `ENERGY_PIAN::libudf1` |
| 后续有效函数 | `ENERGY_PIAN` |

### 7.1 UDF 问题与解决

短迭代初期出现过：

```text
Error: chip-exec: function "ENERGY_PIAN::libudf1" not found.
```

控制台还出现过原始 UDF 路径信息：

```text
/LustreData5/home/shuaiwenwen/sww/heat_source_matrix_32.c
```

说明原始算例依赖师姐环境中的 UDF 源码或编译库。后续师姐补充了：

```text
heat_source_matrix_0_1e6.c
pro.inp
```

将其放入 Fluent 工作目录，并在 Fluent Launcher 中勾选 UDF 编译环境后，Fluent 成功识别并加载：

```text
Found "libudf1" library
Opening library ...
ENERGY_PIAN
Done.
```

补齐 UDF 后，`ENERGY_PIAN::libudf1 not found` 报错消失。

## 8. 温度结果核对

使用 Fluent 控制台或 `Reports → Volume Integrals` 对 `source` cell zone 计算 `Temperature → Static Temperature` 的最大值与最小值。

| 状态 | 区域 | 变量 | 最大值 | 最小值 | 备注 |
|---|---|---|---:|---:|---|
| 读取已有 data | source | Static Temperature | 131.0263 ℃ / 131.02633 ℃ | 35.76516 ℃ | 与 Mechanical 导入温度载荷 3 对应 |
| UDF 缺失时继续迭代后 | source | Static Temperature | 约 26.49236 ℃ | 未记录 | 热源失效，不作为物理结果 |
| 补齐 UDF 后 10 步短迭代 | source | Static Temperature | 132.40909 ℃ | 未记录 | 控制台无 UDF 报错，短迭代复现通过 |

该结果与 Mechanical 中 `Imported Body Temperature 3` 的 CFD 载荷摘要高度一致：

| 来源 | 最大温度 | 最小温度 |
|---|---:|---:|
| Fluent source zone / Volume Integrals | 131.0263 ℃ | 35.76516 ℃ |
| Mechanical Imported Body Temperature 3 / CFD summary | 131.01 ℃ | 35.807 ℃ |

当前判断：`Imported Body Temperature 3` 基本可确认为 Fluent 中 `source` 铜热源区温度场映射到 Mechanical 后的温度载荷。

## 9. 冷却水侧结果

使用 `Surface Integrals` 对入口与出口 surface 计算温度、压力、质量流量和速度。

| 项目 | inlet | outlet | 备注 |
|---|---:|---:|---|
| Area-Weighted Average Static Temperature | 19.99999 ℃ | 20.97516 ℃ | 温升 0.97517 ℃ |
| Area-Weighted Average Static Pressure | 46258.35 Pa | -37528.33 Pa | 静压差约 83.79 kPa |
| Mass Flow Rate | 7.966878 kg/s | -7.966878 kg/s | 出口负号来自面法向方向 |
| Area-Weighted Average Velocity Magnitude | 9 m/s | 9.26229 m/s | 与入口边界一致 |

冷却水温升：

```text
ΔT = 20.97516 - 19.99999 = 0.97517 ℃
```

按模型中 `water-liquid` 的 `Cp = 4182 J/(kg·K)` 估算冷却水带走热量：

```text
Q = m_dot * cp * ΔT
  = 7.966878 * 4182 * 0.97517
  ≈ 32.48 kW
```

当前判断：该水侧能量闭合结果与 32 kW 工况高度一致。

压降按入口平均静压减出口平均静压计算：

```text
Δp = 46258.35 - (-37528.33)
   = 83786.68 Pa
   ≈ 83.79 kPa
```

注意：当前出口边界类型为 `outflow`，不是 `pressure-outlet`。该压降可作为当前结果场中的入口/出口静压差记录；若用于泵选型或论文严谨对比，应确认压力参考位置、边界类型和静压/总压口径。

## 10. 体积积分补充结果

| 区域 | 项目 | 数值 |
|---|---|---:|
| source | Volume | 0.006997188 m³ |
| source | Volume-Weighted Average Static Temperature | 61.03741 ℃ |
| fluid | Maximum Static Temperature | 23.93453 ℃ |
| fluid | Volume-Weighted Average Static Temperature | 20.57065 ℃ |

尝试查找 `Energy Source` 体积积分时，未在 Volume Integrals 可选变量中找到直接可用项。

## 11. 残差与迭代设置

残差监视器中各方程收敛判据均设置为：

```text
continuity：1e-06
x-velocity：1e-06
y-velocity：1e-06
z-velocity：1e-06
energy：1e-06
k：1e-06
epsilon：1e-06
```

运行计算面板曾显示：

```text
迭代次数：500
报告间隔：1
Profile 数据更新间隔：1
伪瞬态设置：Automatic
```

复现测试时将迭代次数改为 10，完成短迭代后控制台无 UDF 函数缺失报错。

## 12. 后处理对象问题

尝试使用已有 `contour-1` / `contour-2` 时，Fluent 提示部分 surface id 已失效：

```text
Following surface ids no longer exists:
48,47,51,50
They must have been deactivated/deleted.
```

以及在选择部分 interface 时出现：

```text
zone-surface: cannot create surface from sliding interface zone.
Creating empty surface.
```

当前处理策略：不依赖旧 contour 对象；优先使用 Volume Integrals / Surface Integrals 或控制台 TUI 获取数值结果，后续如需云图则重新选择有效 wall 或创建新的切面。

## 13. 与论文/任务的对应

- 当前工况应为正常工况，不是偏移工况；判断依据为入口速度 9 m/s、入口温度 20 ℃、32 kW 热源文件/结果，以及未观察到 offset 命名或偏移边界设置。
- 但 UDF 内部热源矩阵是否完全等同于正常工况，需要结合 `heat_source_matrix_0_1e6.c` 和 `pro.inp` 内容进一步确认。
- 当前文件与论文第 4 章 9 m/s 冷却水热分析工况高度对应。
- Fluent 到 Mechanical 的主链路为：

```text
UDF ENERGY_PIAN 体积热源
        ↓
Fluent source 铜区域温度场
        ↓
SYS-1.1 (1).dat
        ↓
Mechanical Imported Body Temperature 3
        ↓
Static Structural
        ↓
Equivalent Stress = 126.82 MPa
Total Deformation = 0.17117 mm
```

## 14. 阶段结论

本阶段已通过老师验收。可表述为：

```text
已完成师姐 Fluent-Mechanical 文件包的读取、关键参数识别、已有结果核对，并在补齐 UDF 源码/输入文件后完成短迭代复现。
```

不宜夸大为“完整复现全部论文数据”，因为完整复现还应包括长步数收敛、重新导入 Mechanical 并复核应力/变形等。

后续工作不再沿此算例继续长算，而是转入缪子束流踢坏区 / 高功率准直吸收结构的热工设计、文献阅读与热应力计算。
